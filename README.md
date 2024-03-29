# GPT Terminal

This project is a Python application that allows you to send a request to OpenAI (or Azure OpenAI) but also allows for setting a motivation for the request. It provides a graphical user interface that allows you to enter text and select various options for rewriting it.

As an option, the application can also source internal and external documents/URLs, and index them through embeddings and vectors, which will then be used to enhance the answers returned by OpenAI.

<a href="https://www.buymeacoffee.com/travin" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## Sources
- Local: TXT, PDF, CSV, XML
- URLs (no crawling)
- BOX folders (box.com)
- Notion DBs (notion.so)

## How to Use
To use the GPT Terminal, simply run the `main.py` file. This will launch the graphical user interface. From there, you can enter text into the input box and select various options for submitting it.

## DATA FOLDER
You can select a folder that holds your data to be used as a reference. Please note that the more data, the greater the cost with OpenAI.
Once you index the folder, it will not need to be indexed again unless you change or add/remove files. This data is also portable, should you take it with you somewhere else and use this application.

If you place PDFs or TXT files into the data folder, then the application will index and use them when you request them.
You can also create a urls.txt file in this folder as well, placing one URL on each line. The application will pull in each URL and include that as the locally sourced data.

NOTE: The application creates a docsearch folder and chain.json that caches a portion of the search information. Unless you add/remove files or URLs from the DATA folder, these should not be modified or deleted.

### Joining indexes
You can also create a add_docsearch.json inside the main data folder that will combine multiple data folders that have already been indexed.
The structure for add_docsearch.json is below. Note that paths are absolute, and special characters must be escaped.

add_docsearch.json structure:

{
    "additional_folders": [
        "path/to/first/additional/data_folder",
        "path/to/second/additional/data_folder",
        ...
    ]
}

### Per-data folder settings
Each data folder can have its own environment.env, which allows the user to simply select the data folder without having to continuously reconfigure keys or other settings.

Once you've entered your text and selected your options, click the "Submit" button to generate the output. You can then read the output in the output box.
The "Submit with data" button will process local embeddings and vectors to enhance the response.
The "Data only search" button will only use the embeddings and vectors to answer your question. 

## Dependencies
This project requires the following dependencies:
- Python3
- requests
- openai
- PyPDF2
- PyCryptodome
- langchain
- faiss-cpu
- selenium
- playwright
- unstructured
- python-dotenv
- tiktoken
- notion_client
- tkhtmlview
- markdown2
- pyperclip
- box-sdk-gen[jwt]

## How to Install
1. Install Python 3: If you don't already have Python installed on your computer, you'll need to download and install it from the official Python website: https://www.python.org/downloads/. Follow the installation instructions for your operating system.

2. Install the required dependencies: Once Python is installed, you'll need to install the dependencies required by the app. To do this, open a command prompt or terminal window and navigate to the directory where the app is located. Then, run the following command:

   ```
   pip install -r requirements.txt
   ```

   This will install all the necessary dependencies for the app.

3. To obtain your OPENAI_API_KEY, sign up for an account at https://beta.openai.com/signup/

4. Add the OPENAI_API_KEY to the enviroment.env
