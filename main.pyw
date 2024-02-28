import threading
import keyboard
import random
import pystray
from pystray import MenuItem as item
from PIL import Image
from pynput.keyboard import Key, Listener
import time
import pyautogui
import clipboard
import os

# Define a list of emoji codes (replace with desired emojis)
emoji_codes = [
    "😘",  
    "😥",  
    "🐩",  
    "⫸",  
]

stop_flag = threading.Event()

# Define a function to quit the program
def on_quit_clicked(icon, item):
    icon.stop()
    stop_flag.set()
    os._exit(0)

# Create a system tray icon
def create_tray_icon():
    try:
        icon = pystray.Icon("example_icon", Image.open("./patata.png"), "Hi there")

        # Define the quit menu item
        quit_item = item("Quit", on_quit_clicked)
        icon.menu = (quit_item,)

        # Set the icon visible
        icon.run()
    except SystemExit:
        pass  # Suppress SystemExit exception when quitting from system tray

# Function to handle keyboard events
def on_press(key):
    if key == Key.space:
        pyautogui.press('backspace', presses=1)
        clipboard.copy(random.choice(emoji_codes))
        disable()
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.0001) 
        enable()

# Function to enable keyboard
def enable():
    for i in range(150):
        keyboard.unblock_key(i)

# Function to disable keyboard
def disable():
    for i in range(150):
        keyboard.block_key(i)
# Create and start the listener in a separate thread
def start_listener():
    with Listener(on_press=on_press) as listener:
        while not stop_flag.is_set():  # Check if the stop flag is set
            listener.join(0.01)

# Block program exit
if __name__ == "__main__":    
    # Start the keyboard listener in a separate thread
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()
    create_tray_icon()
