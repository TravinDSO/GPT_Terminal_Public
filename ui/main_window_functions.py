import os
import json
import tkinter as tk
from tkinter import filedialog
from api.question_processing import process_question


def submit(openai_status_var,input_text, output_text, doc_text, voice_var = '', data_use=0, data_folder="data"):
  
    output_text.delete(1.0, tk.END)

    openai_status_var.set("Processing...")
    
    doc_text.delete(1.0, tk.END)
    doc_text.update()

    question = input_text.get(1.0, tk.END).strip()
    prompt_style = voice_var.get()

    result = ""
    docs = []
    
    #data_use = # 0 = no data 1 = data 2 = data only
    result, docs, openai_status = process_question(data_use, question, prompt_style, data_folder,False)

    openai_status_var.set(openai_status)

    output_text.insert(tk.END, result)

    if docs:
        for doc in docs:
            doc_text.insert(tk.END, doc)
            doc_text.insert(tk.END, "\n\n")

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