import os
import tkinter as tk
from tkinter import ttk
from ui.main_window_functions import submit, change_font_size, select_data_folder, process_question
from ui.main_window_functions import load_data_folder_var, toggle_dark_mode

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

    # Create dark mode toggle button
    dark_mode_icon = tk.PhotoImage(file="ui\\dark_mode_icon.png").subsample(6, 6)  # Adjust the numbers to change the icon size
    is_dark_mode = tk.BooleanVar()
    is_dark_mode.set(False)

    dark_mode_button = ttk.Button(main_frame, image=dark_mode_icon, command=lambda: toggle_dark_mode(root, [input_text, output_text], is_dark_mode))
    dark_mode_button.image = dark_mode_icon
    dark_mode_button.grid(row=0, column=4, sticky=tk.E)

    # Create input and output labels
    input_label = ttk.Label(main_frame, text="Input Text:")
    input_label.grid(row=0, column=0,columnspan=2,sticky=tk.W)
    output_label = ttk.Label(main_frame, text="Output Text:")
    output_label.grid(row=0, column=3,columnspan=2,sticky=tk.W)

    # Create input and output text widgets
    input_text = tk.Text(main_frame, wrap="word", width=30, height=20)
    input_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)

    output_text = tk.Text(main_frame, wrap="word", width=30, height=20)
    output_text.grid(row=1, column=2, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
    main_frame.columnconfigure(2, weight=1)
    main_frame.columnconfigure(3, weight=1)

    # Create voice label and entry
    voice_label = ttk.Label(main_frame, text="Tell OpenAI what to do with the input (optional):")
    voice_label.grid(row=2, column=0, sticky=tk.W)
    voice_var = tk.StringVar()
    voice_entry = ttk.Entry(main_frame, textvariable=voice_var)
    voice_entry.grid(row=3, column=0,columnspan=2,sticky=(tk.W, tk.E))

    # Create submit buttons
    # 0 = no data 1 = data 2 = data only
    submit_button = ttk.Button(main_frame, text="Submit", command=lambda: submit(input_text, output_text, voice_var, 0, str(data_folder_var.get())))
    submit_button.grid(row=2, column=2, sticky=(tk.W, tk.E))

    submit_button = ttk.Button(main_frame, text="Submit with data", command=lambda: submit(input_text, output_text, voice_var, 1, str(data_folder_var.get())))
    submit_button.grid(row=2, column=3, sticky=(tk.W, tk.E))

    submit_button = ttk.Button(main_frame, text="Data only search", command=lambda: submit(input_text, output_text, voice_var, 2, str(data_folder_var.get())))
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
    data_folder_button = ttk.Button(main_frame, text="Index Folder ($$$)", command=lambda: process_question('', str(data_folder_var.get()),True))
    data_folder_button.grid(row=4, column=3, sticky=(tk.W, tk.E))

    # Create a label to display the selected path with the prefix
    ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E))
    data_folder_var = tk.StringVar()
    data_folder_label = ttk.Label(main_frame, textvariable=data_folder_var)
    data_folder_label.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E))

    # Set the default data folder
    default_data_folder = load_data_folder_var()
    if default_data_folder:
        data_folder_var.set(default_data_folder)
    else:
        data_folder_var.set(os.path.abspath("data"))

    return root