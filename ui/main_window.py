import os
import time
import json
import dotenv
import sys
import pyperclip
import subprocess
import tkinter as tk
from tkhtmlview import HTMLLabel, HTMLText
from tkinter import ttk, filedialog
from ui.main_window_functions import submit, change_font_size


def create_main_window():
    root = tk.Tk() 
    root.title("GPT Terminal")
    
    os.environ["APP_RESTART"] = "False"

    env_file = get_env_file()

    chat_history = []

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    dotenv.load_dotenv(dotenv_path=env_file, override=True)

    today = time.strftime("%Y-%m-%d")

    default_system_message = "You are a helpful assistant. Today is: " + today

    use_azure = os.getenv("USE_AZURE")
    frame_color = os.getenv("FRAME_COLOR")
    label_text = os.getenv("LABEL_TEXT")
    button_text = os.getenv("BUTTON_TEXT")
    input_color = os.getenv("INPUT_COLOR")

    gui_style = ttk.Style()
    gui_style.configure('My.TButton', foreground=button_text, background=frame_color, borderwidth= 0)

    gui_style2 = ttk.Style()
    gui_style2.configure('My.TFrame', background=frame_color)

    gui_style3 = ttk.Style()
    gui_style3.configure('My.TLabel', foreground=label_text, background=frame_color,font=("Helvetica", 10, "bold"))

    gui_style4 = ttk.Style()
    gui_style4.configure('My.TEntry', foreground=label_text, background=input_color,font=("Helvetica", 10, "bold"))

    main_frame = ttk.Frame(root, style='My.TFrame', padding="10", width=600, height=600)
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(1, weight=1)

    # Create input and output labels
    input_label = ttk.Label(main_frame, style='My.TLabel', text="Input Text:")
    input_label.grid(row=0, column=0,columnspan=2,sticky=tk.W)
    output_label = ttk.Label(main_frame, style='My.TLabel', text="Output Text:")
    output_label.grid(row=0, column=2,columnspan=1,sticky=tk.W)
    output_label = ttk.Label(main_frame, style='My.TLabel', text="Document Results:")
    output_label.grid(row=0, column=4,columnspan=2,sticky=tk.W)

    # Create input text widget
    input_text = tk.Text(main_frame, background=input_color, wrap="word", width=30, height=20)
    input_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)

    # Create output text widget
    output_text = HTMLText(main_frame, html="", background=input_color)
    output_text.grid(row=1, column=2, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
    main_frame.columnconfigure(2, weight=1)
    main_frame.columnconfigure(3, weight=1)

    # Create a button to copy the output text to the clipboard
    copy_button = ttk.Button(main_frame, text="Copy", command=lambda: copy_to_clipboard(output_text.get(1.0, tk.END)))
    copy_button.grid(row=0, column=3, sticky=tk.E)

    # Create a button to generate a new window
    new_window_button = ttk.Button(main_frame, text="New Instance", command=start_new_instance)
    new_window_button.grid(row=0, column=3, sticky=tk.W)


    # Create doc text widget that displays the contents of the searched documents
    doc_text = tk.Text(main_frame, background=input_color, wrap="word", width=60, height=20)
    doc_text.grid(row=1, column=4,columnspan=2,sticky=(tk.W, tk.E, tk.N, tk.S))
    main_frame.columnconfigure(4, weight=2)

    # Create voice label and entry
    voice_label = ttk.Label(main_frame, style='My.TLabel', text="Tell OpenAI what to do with the input (optional)")
    voice_label.grid(row=2, column=0, sticky=tk.W)
    voice_var = tk.StringVar()
    voice_var.set(default_system_message)
    voice_entry = tk.Text(main_frame, background=input_color, height=3, width=30, wrap="word")
    voice_entry.grid(row=3, column=0,columnspan=2,rowspan=2,sticky=(tk.W, tk.E))
    voice_entry.insert(tk.END, voice_var.get())

    # Create submit buttons
    # 0 = no data 1 = data 2 = data only
    submit_button = ttk.Button(main_frame, style='My.TButton', text="Submit without data", command=lambda: submit(total_docs_var,max_tokens_var,query_temp_var,openai_status_var,input_text, output_text, doc_text, voice_entry, 0, str(data_folder_var.get()),env_file, False, chat_history))
    submit_button.grid(row=2, column=2, sticky=(tk.W, tk.E))

    submit_button = ttk.Button(main_frame, style='My.TButton', text="Submit with data", command=lambda: submit(total_docs_var,max_tokens_var,query_temp_var,openai_status_var,input_text, output_text, doc_text, voice_entry, 1, str(data_folder_var.get()),env_file, False, chat_history))
    submit_button.grid(row=2, column=3, sticky=(tk.W, tk.E))

    submit_button = ttk.Button(main_frame, style='My.TButton', text="Data only search", command=lambda: (submit(total_docs_var,max_tokens_var,query_temp_var,openai_status_var,input_text, output_text, doc_text, voice_entry, 2, str(data_folder_var.get()),env_file, False,chat_history),update_query_temp_label(query_temp_var,query_temp_label,True)))
    submit_button.grid(row=3, column=2, columnspan=2, sticky=(tk.W, tk.E))

    # Create a button to force data folder indexing
    data_folder_button = ttk.Button(main_frame, style='My.TButton', text="Index Folder ($$$)", command=lambda: (submit(total_docs_var,max_tokens_var,query_temp_var,openai_status_var,input_text, output_text, doc_text, voice_entry, 2, str(data_folder_var.get()),env_file, True, chat_history),update_query_temp_label(query_temp_var,query_temp_label,True)))
    data_folder_button.grid(row=4, column=3, sticky=(tk.W, tk.E))

    # Create a button to open the directory selection dialog
    data_folder_button = ttk.Button(main_frame, style='My.TButton', text="Select Data Folder", command=lambda: select_data_folder(data_folder_var,root))
    data_folder_button.grid(row=4, column=2, sticky=(tk.W, tk.E))

    # Create a label and slider to adjust PROMPT_QUERY_TEMP
    query_temp_var = tk.StringVar()
    query_temp_var.set(os.environ.get('PROMPT_QUERY_TEMP', '0.4'))  # Use a default value if the environment variable is not set
    query_temp_label = ttk.Label(main_frame, style='My.TLabel', text=f"Temp: {query_temp_var.get()}")
    query_temp_label.grid(row=2, column=4, sticky=(tk.W, tk.E))
    query_temp_slider = ttk.Scale(main_frame, from_=0.0, to=1.0, length=200, orient=tk.HORIZONTAL, variable=query_temp_var, command=lambda value: update_query_temp_label(query_temp_var,query_temp_label))
    query_temp_slider.grid(row=2, column=5, sticky=(tk.W, tk.E))

    # Create a label and slider to adjust MAX_TOKENS
    max_tokens_var = tk.StringVar()
    max_tokens_var.set(os.getenv("MAX_TOKENS"))
    max_tokens_label = ttk.Label(main_frame, style='My.TLabel', text=f"Max Response Tokens: {max_tokens_var.get()}")
    max_tokens_label.grid(row=3, column=4, sticky=(tk.W, tk.E))
    max_tokens_slider = ttk.Scale(main_frame, from_=100, to=6500, length=200, orient=tk.HORIZONTAL, variable=max_tokens_var, command=lambda value: update_max_tokens_label(max_tokens_var, max_tokens_label))
    max_tokens_slider.grid(row=3, column=5, sticky=(tk.W, tk.E))

    # Create a label and slider to adjust NUM_DOCS_TO_SEARCH
    total_docs_var = tk.StringVar()
    total_docs_var.set(os.getenv("NUM_DOCS_TO_SEARCH"))
    total_docs_label = ttk.Label(main_frame, style='My.TLabel', text=f"Total Documents Searched: {total_docs_var.get()}")
    total_docs_label.grid(row=4, column=4, sticky=(tk.W, tk.E))
    total_docs_slider = ttk.Scale(main_frame, from_=1, to=1000, length=200, orient=tk.HORIZONTAL, variable=total_docs_var, command=lambda value: update_total_docs_label(total_docs_var, total_docs_label))
    total_docs_slider.grid(row=4, column=5, sticky=(tk.W, tk.E))

    # Create a separator
    ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=6, sticky=(tk.W, tk.E))

    # Create a label to display the selected path with the prefix
    data_folder_var = tk.StringVar()
    data_folder_label = ttk.Label(main_frame, style='My.TLabel', textvariable=data_folder_var)
    data_folder_label.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E))

    # Create a label to display the token count, etc
    openai_status_var = tk.StringVar()
    if use_azure.lower() == "true":
        openai_status_var.set("Terminal Ready: Using Azure API")
    else:
        openai_status_var.set("Terminal Ready: Using OpenAI API")
    openai_status_label = ttk.Label(main_frame, style='My.TLabel', textvariable=openai_status_var)
    openai_status_label.grid(row=7, column=0, columnspan=5, sticky=(tk.W, tk.E))

    # Add a new button for opening the settings window
    settings_icon = tk.PhotoImage(file="settings_icon.png").subsample(25, 25)  # Adjust the numbers to change the icon size
    settings_button = ttk.Button(main_frame,style='My.TButton',image=settings_icon, command=lambda: open_settings_window(root))
    settings_button.image = settings_icon
    settings_button.grid(row=6, column=4, rowspan=2, columnspan=2,sticky=tk.E)

    # Set the default data folder
    default_data_folder = load_data_folder_var()
    if default_data_folder:
        data_folder_var.set(default_data_folder)
    else:
        data_folder_var.set(os.path.abspath("data"))

    return root

def open_settings_window(root):
    settings_window = tk.Toplevel()
    settings_window.title("Settings (Restart button loads new settings))")
    
    settings_frame = ttk.Frame(settings_window, padding="10")
    settings_frame.pack(fill="both", expand=True)
    
    env_text = tk.Text(settings_frame, wrap="word", width=60, height=20)
    env_text.pack(fill="both", expand=True)
    
    # Try to read the .env file
    try:        
        # Ensure the .env file exists
        if not os.path.exists(get_env_file()):
            print(f"No .env file found at: {get_env_file()}")
            return

        with open(get_env_file(), "r") as f:
            env_vars = f.read()

    except Exception as e:
        print(f"Failed to load .env file: {e}")
        return
    
    # Insert the contents of the .env file into the Text widget
    env_text.insert('end', env_vars)
    
    save_button = ttk.Button(settings_frame, text="Save", command=lambda: save_env_vars(env_text))
    save_button.pack(side="left")

    env_note = ttk.Label(settings_frame, text="Note: place environment.env files in data folders to create data specific settings")
    env_note.pack(side="left")

    close_button = ttk.Button(settings_frame, text="Restart", command=lambda: restart_app(root,settings_window))
    close_button.pack(side="right")

def save_env_vars(env_text):
    # Extract the environment variables from the Text widget
    env_vars_text = env_text.get('1.0', 'end').strip().split('\n')

    # Overwrite the .env file with the updated environment variables
    with open(get_env_file(), 'w') as env_file:
        for env_var in env_vars_text:
            env_file.write(f"{env_var}\n")

def restart_app(root,settings_window = None):
    os.environ["APP_RESTART"] = "True"
    if settings_window:
        settings_window.destroy()
    root.destroy()

def select_data_folder(data_folder_var,root):
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        full_path = os.path.abspath(selected_folder)
        data_folder_var.set(full_path)
        save_data_folder_var(full_path)  # Save the selected folder path to config.json
        restart_app(root)

def save_data_folder_var(data_folder_var_value, config_file='config.json'):
    with open(config_file, 'w') as f:
        json.dump({"data_folder": data_folder_var_value}, f)

def load_data_folder_var(config_file='config.json'):
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config_data = json.load(f)
            return config_data.get("data_folder")
    return None

def get_env_file():
    data_folder = load_data_folder_var()
    env_path = ''
    data_folder_env = ''
    if data_folder:
        data_folder_env = os.path.join(data_folder, "environment.env")
        if os.path.exists(data_folder_env):
            env_path = data_folder_env
        else:
            env_path = 'environment.env'
    else:
        env_path = 'environment.env'
    
    return env_path

def update_query_temp_label(query_temp_var,query_temp_label,data_only=False):
    query_temp_var.set(round(float(query_temp_var.get()), 2))
    query_temp_label.configure(text=f"Temp: {query_temp_var.get()}")

def update_max_tokens_label(max_tokens_var, max_tokens_label):
    max_tokens = int(float(max_tokens_var.get()))
    max_tokens_label.configure(text=f"Max Response Tokens: {max_tokens}")

def update_total_docs_label(total_docs_var, total_docs_label):
    total_docs = int(float(total_docs_var.get()))
    total_docs_label.configure(text=f"Total Documents Searched: {total_docs}")

def copy_to_clipboard(content):
    pyperclip.copy(content)  # Copy the content to the clipboard

def start_new_instance():
    subprocess.Popen([sys.executable, "main.py"])

def generate_env_file(filename='environment.env'):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write("USE_AZURE=False\n")
            f.write("USE_NOTION=False\n")
            f.write("USE_BOX=False\n")
            f.write("PROMPT_QUERY_TEMP=0.7\n")
            f.write("MAX_TOKENS=800\n")
            f.write("NUM_DOCS_TO_SEARCH=5\n")
            f.write("OPENAI_API_KEY=\"\"\n")
            f.write("OPENAI_API_ENDPOINT=\"https://api.openai.com/v1/completions\"\n")
            f.write("OPENAI_API_MODEL=\"gpt-3.5-turbo\"\n")
            f.write("EMBEDDINGS_MODEL=\"text-embedding-ada-002\"\n")
            f.write("AZURE_OPENAI_API_KEY=\"\"\n")
            f.write("AZURE_OPENAI_API_ENDPOINT=\"\"\n")
            f.write("AZURE_OPENAI_API_MODEL=\"\"\n")
            f.write("AZURE_EMBEDDINGS_MODEL=\"\"\n")
            f.write("AZURE_OPENAI_API_VERSION=\"\"\n")
            f.write("AZURE_OPENAI_API_LOCATION=\"\"\n")
            f.write("NOTION_API_KEY=\"\"\n")
            f.write("NOTION_DATABASE_ID=\"\"\n")
            f.write("BOX_CLIENT_ID=\"\"\n")
            f.write("BOX_CLIENT_SECRET=\"\"\n")
            f.write("BOX_ENTERPRISE_ID=\"\"\n")
            f.write("BOX_USER_ID=\"\"\n")
            f.write("BOX_FOLDER_ID==\"\"\n")
            f.write("BOX_DEVELOPER_TOKEN==\"\"\n")
            f.write("FRAME_COLOR=\"#04993B\"\n")
            f.write("LABEL_TEXT=\"#FFFFFF\"\n")
            f.write("BUTTON_TEXT=\"#000000\"\n")
            f.write("INPUT_COLOR=\"#CCFFE1\"\n")