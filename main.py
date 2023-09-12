import os
from ui.main_window import generate_env_file, create_main_window

# pip install -U -r requirements.txt
# pip freeze > requirements.txt
# pyinstaller --onefile --noconsole --icon=twist.ico main.py

def main():

    # Generate the environment file if it doesn't exist
    generate_env_file()

    # Create the main application window
    root = create_main_window()

    # Start the main event loop of the application
    root.mainloop()

    # Close the root window
    root.quit()

    if os.environ["APP_RESTART"] == "True":
        restart_main_loop()

def restart_main_loop():
    # Create a new instance of Tk
    root = create_main_window()

    # Start the main event loop of the application
    root.mainloop()

    # Close the root window
    root.quit()

    if os.environ["APP_RESTART"] == "True":
        restart_main_loop()

if __name__ == "__main__":
    # Run the main function when the script is executed
    main()
