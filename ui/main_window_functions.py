import os
import json
import tkinter as tk
import time
from tkinter import filedialog
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chains import load_chain
from api.openai_api import rewrite_text
from api.question_processing import process_question


def submit(input_text, output_text, voice_var, data_use=0, data_folder="data"):
  
    output_text.delete(1.0, tk.END)
    g_color = output_text.cget("bg")
    output_text.configure(bg="#E3C0D5")
    output_text.insert(tk.END, "Processing...")
    output_text.update()
    
    question = input_text.get(1.0, tk.END).strip()
    prompt_style = voice_var.get()

    result = ""
    if question:
        if data_use == 1:
            supporting_data = process_question(question, data_folder,False)
            result = rewrite_text(question, prompt_style, supporting_data)
        elif data_use == 2:
            result = process_question(question, data_folder, False)
        else:
            result = rewrite_text(question, prompt_style, "")
        
    output_text.configure(bg=g_color)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, result)

def change_font_size(text_widgets, size):
    for widget in text_widgets:
        if isinstance(widget, tk.Text):
            current_font = widget.cget("font")
            widget.configure(font=(current_font, size))

def select_data_folder(data_folder_var):
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        full_path = os.path.abspath(selected_folder)
        data_folder_var.set(full_path)
        save_data_folder_var(full_path)  # Save the selected folder path to config.json

def save_data_folder_var(data_folder_var_value, config_file='config.json'):
    with open(config_file, 'w') as f:
        json.dump({"data_folder": data_folder_var_value}, f)

def load_data_folder_var(config_file='config.json'):
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config_data = json.load(f)
            return config_data.get("data_folder")
    return None

def toggle_dark_mode(root, text_widgets, is_dark_mode):
    if is_dark_mode.get():
        root.configure(bg="gray12")
        for widget in text_widgets:
            widget.configure(bg="gray12", fg="white", insertbackground="white")
    else:
        root.configure(bg="white")
        for widget in text_widgets:
            widget.configure(bg="white", fg="black", insertbackground="black")

    is_dark_mode.set(not is_dark_mode.get())