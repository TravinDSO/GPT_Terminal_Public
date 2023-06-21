from ui.main_window import generate_env_file, create_main_window

def main():

    # Generate the environment file if it doesn't exist
    generate_env_file()

    # Create the main application window
    root = create_main_window()

    # Start the main event loop of the application
    root.mainloop()

if __name__ == "__main__":
    # Run the main function when the script is executed
    main()
