import os
import tkinter as tk
from markdown2 import Markdown
from api.question_processing import process_question


def submit(total_docs_var,max_tokens_var,query_temp_var,openai_status_var,input_text, output_text, doc_text, voice_entry = '', data_use=0, data_folder="data", env_file='environment.env',reindex=False,chat_history=[]):

    #output_text.delete(1.0, tk.END)

    openai_status_var.set("Processing...")
    
    doc_text.delete(1.0, tk.END)
    doc_text.update()

    question = input_text.get(1.0, tk.END).strip()
    prompt_style = voice_entry.get(1.0, tk.END).strip()

    result = ""
    docs = []
    #data_use = # 0 = no data 1 = data 2 = data only
    result, docs, openai_status = process_question(total_docs_var,max_tokens_var,query_temp_var,openai_status_var,doc_text,env_file,data_use, question, prompt_style, data_folder,reindex,chat_history)

    doc_text.delete(1.0, tk.END)
    doc_text.update()

    openai_status_var.set(openai_status)

    output_text.insert(tk.END, result)
    output_text.update()

    if docs:
        for doc in docs:
            doc_text.insert(tk.END, doc)
            doc_text.insert(tk.END, "\n\n")

def change_font_size(output_text,text_widgets, size):
    for widget in text_widgets:
        if isinstance(widget, tk.Text):
            current_font = widget.cget("font")
            widget.configure(font=(current_font, size))
    output_text.config(font=(current_font, size))

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