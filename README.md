# GPT Terminal

This project is a Python application that allows you to send a request to OpenAPI but also allows for setting a motivation for the request. It provides a graphical user interface that allows you to enter text and select various options for rewriting it.

As an option, the application can also source internal and external documents/URLs, index them though embeddings and vectors which will then be used to enhance the answers returned by OpenAI.

<a href="https://www.buymeacoffee.com/travin" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## How to Use
To use the GPT Terminal, simply run the `main.py` file. This will launch the graphical user interface. From there, you can enter text into the input box and select various options for submitting it.

## DATA FOLDER
You can select a folder that holds your data to be used as reference. Please note that the more data, the greater the cost with OpenAI.
Once you index the folder, it will not need to be indexed again unless you change or add/remove files. This data is portable as well should you need to take it with you somewhere else and use this application.

If you place PDFs or TXT files into the data folder, then these will be indexed and used by the application when you request it.
You can also create a urls.txt files in this folder as well, placing one URL on each line. The applicaton will pull in each URL and include that as the locally sourced data.

NOTE: The application creates a docsearch folder and chain.json that cache a portion of the search information. These should not be modified or deleted unless you add/remove files or URLs from the DATA folder.

### OPTION
You can also create a add_docsearch.json inside the main data folder that will combine multiple data folders that have already been indexed.
The structure for add_docsearch.json is below. Note that paths are absolute and special characters must be escaped.

add_docsearch.json structure:

{
    "additional_folders": [
        "path/to/first/additional/data_folder",
        "path/to/second/additional/data_folder",
        ...
    ]
}


## Available Options
- Font Size: Adjust the font size of the text in the input and output boxes.

Once you've entered your text and selected your options, click the "Submit" button to generate the output. You can then read the output in the output box.
The "Submit with data" button will process local embeddings and vectors to enhance the response.
The "Data only search" buttong will only use the embeddings and vectors to answer your question. 

## Dependencies
This project requires the following dependencies:
- Python3
- tkinter
- requests
- openai
- PyPDF2
- langchain
- faiss-cpu
- playwright
- unstructured
- python-dotenv

## How to Install
1. Install Python 3: If you don't already have Python installed on your computer, you'll need to download and install it from the official Python website: https://www.python.org/downloads/. Follow the installation instructions for your operating system.

2. Install the required dependencies: Once Python is installed, you'll need to install the dependencies required by the app. To do this, open a command prompt or terminal window and navigate to the directory where the app is located. Then, run the following command:

   ```
   pip install -r requirements.txt
   ```

   This will install all the necessary dependencies for the app.

3. To obtain your OPENAI_API_KEY, sign up for an account at https://beta.openai.com/signup/
Then