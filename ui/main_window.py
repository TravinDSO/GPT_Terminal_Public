import os
import dotenv
import tkinter as tk
from tkinter import ttk
from ui.main_window_functions import submit, change_font_size, select_data_folder, process_question
from ui.main_window_functions import load_data_folder_var, toggle_dark_mode

env_path = 'environment.env'


def create_main_window():
    root = tk.Tk()
    root.title("GPT Terminal")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    main_frame = ttk.Frame(root, padding="10", width=600, height=600)
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(1, weight=1)

    # Create input and output labels
    input_label = ttk.Label(main_frame, text="Input Text:")
    input_label.grid(row=0, column=0,columnspan=2,sticky=tk.W)
    output_label = ttk.Label(main_frame, text="Output Text:")
    output_label.grid(row=0, column=2,columnspan=2,sticky=tk.W)
    output_label = ttk.Label(main_frame, text="Document Results:")
    output_label.grid(row=0, column=4,sticky=tk.W)


    # Create input and output text widgets
    input_text = tk.Text(main_frame, wrap="word", width=30, height=20)
    input_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)

    output_text = tk.Text(main_frame, wrap="word", width=30, height=20)
    output_text.grid(row=1, column=2, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
    main_frame.columnconfigure(2, weight=1)
    main_frame.columnconfigure(3, weight=1)

    doc_text = tk.Text(main_frame, wrap="word", width=60, height=20)
    doc_text.grid(row=1, column=4, rowspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
    main_frame.columnconfigure(4, weight=2)

    # Create voice label and entry
    voice_label = ttk.Label(main_frame, text="Tell OpenAI what to do with the input (optional):")
    voice_label.grid(row=2, column=0, sticky=tk.W)
    voice_var = tk.StringVar()
    voice_entry = ttk.Entry(main_frame, textvariable=voice_var)
    voice_entry.grid(row=3, column=0,columnspan=2,sticky=(tk.W, tk.E))

    # Create submit buttons
    # 0 = no data 1 = data 2 = data only
    submit_button = ttk.Button(main_frame, text="Submit without data", command=lambda: submit(openai_status_var,input_text, output_text, doc_text, voice_var, 0, str(data_folder_var.get())))
    submit_button.grid(row=2, column=2, sticky=(tk.W, tk.E))

    submit_button = ttk.Button(main_frame, text="Submit with data", command=lambda: submit(openai_status_var,input_text, output_text, doc_text, voice_var, 1, str(data_folder_var.get())))
    submit_button.grid(row=2, column=3, sticky=(tk.W, tk.E))

    submit_button = ttk.Button(main_frame, text="Data only search", command=lambda: submit(openai_status_var,input_text, output_text, doc_text, voice_var, 2, str(data_folder_var.get())))
    submit_button.grid(row=3, column=2, columnspan=2, sticky=(tk.W, tk.E))

    # Create font size label and dropdown
    font_size_label = ttk.Label(main_frame, text="Font Size:")
    font_size_label.grid(row=4, column=0, sticky=tk.E)

    font_size_var = tk.StringVar()
    font_size_var.set("14")
    font_size_dropdown = ttk.OptionMenu(main_frame, font_size_var, "14", "10", "12", "14", "16", "18", "20", command=lambda size: change_font_size([input_text, output_text], size))
    font_size_dropdown.grid(row=4, column=1, sticky=(tk.W, tk.E))

    # Set default font size
    change_font_size([input_text, output_text], "14")

    # Create a button to open the directory selection dialog
    data_folder_button = ttk.Button(main_frame, text="Select Data Folder", command=lambda: select_data_folder(data_folder_var))
    data_folder_button.grid(row=4, column=2, sticky=(tk.W, tk.E))

    # Create a button to force data folder indexing
    data_folder_button = ttk.Button(main_frame, text="Index Folder ($$$)", command=lambda: process_question(2, '','',str(data_folder_var.get()),True))
    data_folder_button.grid(row=4, column=3, sticky=(tk.W, tk.E))

    # Create a separator
    ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=5, sticky=(tk.W, tk.E))

    # Create a label to display the selected path with the prefix
    data_folder_var = tk.StringVar()
    data_folder_label = ttk.Label(main_frame, textvariable=data_folder_var)
    data_folder_label.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E))

    # Create a label to display the token count, etc
    openai_status_var = tk.StringVar()
    openai_status_var.set("Terminal Ready")
    openai_status_label = ttk.Label(main_frame, textvariable=openai_status_var)
    openai_status_label.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E))

    # Create dark mode toggle button
    #dark_mode_icon = tk.PhotoImage(file="dark_mode_icon.png").subsample(4, 4)  # Adjust the numbers to change the icon size
    #is_dark_mode = tk.BooleanVar()
    #is_dark_mode.set(False)

    #dark_mode_button = ttk.Button(main_frame, image=dark_mode_icon, command=lambda: toggle_dark_mode(root, [input_text, output_text], is_dark_mode))
    #dark_mode_button.image = dark_mode_icon
    #dark_mode_button.grid(row=6, column=4, sticky=tk.E)

    # Add a new button for opening the settings window
    settings_icon = tk.PhotoImage(file="settings_icon.png").subsample(25, 25)  # Adjust the numbers to change the icon size
    settings_button = ttk.Button(main_frame, image=settings_icon, command=open_settings_window)
    settings_button.image = settings_icon
    settings_button.grid(row=6, column=4, rowspan=2, sticky=tk.E)

    # Set the default data folder
    default_data_folder = load_data_folder_var()
    if default_data_folder:
        data_folder_var.set(default_data_folder)
    else:
        data_folder_var.set(os.path.abspath("data"))

    return root


def open_settings_window():
    settings_window = tk.Toplevel()
    settings_window.title("Settings (note: changes currently require a restart))")
    
    settings_frame = ttk.Frame(settings_window, padding="10")
    settings_frame.pack(fill="both", expand=True)
    
    env_text = tk.Text(settings_frame, wrap="word", width=60, height=20)
    env_text.pack(fill="both", expand=True)
    
    # Try to read the .env file
    try:        
        # Ensure the .env file exists
        if not os.path.exists(env_path):
            print(f"No .env file found at: {env_path}")
            return

        with open(env_path, "r") as f:
            env_vars = f.read()

    except Exception as e:
        print(f"Failed to load .env file: {e}")
        return
    
    # Insert the contents of the .env file into the Text widget
    env_text.insert('end', env_vars)
    
    save_button = ttk.Button(settings_frame, text="Save", command=lambda: save_env_vars(env_text))
    save_button.pack(side="left")

    close_button = ttk.Button(settings_frame, text="Close", command=lambda: close_settings_window(settings_window))
    close_button.pack(side="right")

def save_env_vars(env_text):
    # Extract the environment variables from the Text widget
    env_vars_text = env_text.get('1.0', 'end').strip().split('\n')

    # Overwrite the .env file with the updated environment variables
    with open(env_path, 'w') as env_file:
        for env_var in env_vars_text:
            env_file.write(f"{env_var}\n")

    # Reload the environment variables
    dotenv.load_dotenv(dotenv_path=env_path, override=True)

def close_settings_window(settings_window):
    settings_window.destroy()

def generate_env_file(filename='environment.env'):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write("USE_AZURE=False\n")
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