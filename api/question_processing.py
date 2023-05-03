import os
import gc
import gzip
import tempfile
import json
import xml.etree.ElementTree as ET
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chains import load_chain
from langchain.document_loaders import SeleniumURLLoader, UnstructuredURLLoader
from config import EMBEDDINGS_MODEL, LANGCHAIN_MODEL

class CustomTextSplitter(CharacterTextSplitter):
    def __init__(self, separators, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.separators = separators

    def split_text(self, text):
        import re
        chunks = []
        pattern = '|'.join(map(re.escape, self.separators))
        splits = re.split(pattern, text)
        return self._merge_splits(splits, self.separators[0])

def process_question(query, data_folder,reindex=False):

    chain_path = os.path.join(data_folder, 'chain.json')
    docsearch_path = os.path.join(data_folder, 'docsearch')
    url_file = os.path.join(data_folder, 'urls.txt')
    compressed_raw_text_file = os.path.join(data_folder, 'temporary_cached_data.gz')
    add_docsearch_file = os.path.join(data_folder, 'add_docsearch.json')


    if os.path.exists(compressed_raw_text_file):
        os.remove(compressed_raw_text_file)

    if not os.path.exists(url_file):
        with open(url_file, 'w') as f:
            f.write('https://blackscreen.app')

    if not os.path.exists(chain_path) or reindex:
        with gzip.open(compressed_raw_text_file, 'wt', encoding='utf-8') as f:
            for root, _, files in os.walk(data_folder):
                for file in files:
                    if file.endswith('.pdf'):
                        pdf_path = os.path.join(root, file)
                        print("Parsing" + pdf_path)
                        reader = PdfReader(pdf_path)
                        for i, page in enumerate(reader.pages):
                            text = page.extract_text()
                            if text:
                                f.write(text)
                        # Release memory after processing each PDF
                        del reader
                        gc.collect()
                    elif file.endswith('.txt'):
                        txt_path = os.path.join(root, file)
                        print("Parsing" + txt_path)
                        with open(txt_path, 'r', encoding='utf-8') as txt_file:
                            txt_text = txt_file.read()
                        f.write(txt_text)
                    elif file.endswith('.xml'):
                        xml_path = os.path.join(root, file)
                        print("Parsing" + xml_path)
                        # Create a context for iteratively parsing the XML file
                        context = ET.iterparse(xml_path, events=('start', 'end'))
                        context = iter(context)
                        # Process the XML file chunk by chunk
                        for event, elem in context:
                            if event == 'end':
                                # Write the text content of the current element to the gz file
                                if elem.text:
                                    f.write(elem.text)
                                # Clean up the processed element to save memory
                                elem.clear()

            if url_file and os.path.exists(url_file):
                with open(url_file, 'r') as url_file_obj:
                    url_list = [line.strip() for line in url_file_obj]
                url_loader = SeleniumURLLoader(urls=url_list)
                url_data = url_loader.load()
                for i, data in enumerate(url_data):
                    text = data.page_content
                    f.write(text)

    if not os.path.exists(chain_path) or reindex:
        # Initialize an empty list to store processed text chunks
        processed_texts_cache = []

        with gzip.open(compressed_raw_text_file, 'rt', encoding='utf-8') as f:
            text_splitter = CustomTextSplitter(
                separators=['\n', '. '],
                chunk_size=5000,
                chunk_overlap=400,
                length_function=len,
            )
            
            current_chunk = ''
            for line in f:
                current_chunk += line
                if len(current_chunk) >= text_splitter._chunk_size:  # Corrected attribute name
                    # Process the current chunk
                    processed_chunk = text_splitter.split_text(current_chunk)
                    
                    # Append the processed chunk to the cache
                    processed_texts_cache.extend(processed_chunk)
                    
                    # Keep the chunk_overlap part of the current chunk for the next iteration
                    current_chunk = current_chunk[-text_splitter._chunk_overlap:]  # Corrected attribute name

        # Process the remaining part of the last chunk
        if current_chunk:
            processed_chunk = text_splitter.split_text(current_chunk)
            processed_texts_cache.extend(processed_chunk)

        os.remove(compressed_raw_text_file)

        embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)
        docsearch = FAISS.from_texts(processed_texts_cache, embeddings)
        chain = load_qa_chain(OpenAI(max_tokens=400,model_name=LANGCHAIN_MODEL,temperature=0.1), chain_type="stuff")
        docsearch.save_local(docsearch_path)
        chain.save(chain_path)
    else:
        embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)
        docsearch = FAISS.load_local(docsearch_path, embeddings)
        chain = load_chain(chain_path)

    # Load additional docsearch instances and combine them
    if os.path.exists(add_docsearch_file):
        with open(add_docsearch_file, 'r') as f:
            add_docsearch_config = json.load(f)

        additional_folders = add_docsearch_config.get('additional_folders', [])
        for folder in additional_folders:
            additional_docsearch_path = os.path.join(folder, 'docsearch')
            if os.path.exists(additional_docsearch_path):
                additional_docsearch = FAISS.load_local(additional_docsearch_path, embeddings)
                docsearch.merge_from(additional_docsearch)

    if query != '':
        docs = docsearch.similarity_search(query, k=10)
        answer = chain.run(input_documents=docs, question=query)
    else:
        answer = ''

    return answer
