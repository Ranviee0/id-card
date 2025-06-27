import tkinter as tk
from threading import Thread
import uvicorn
import os
import sys

if getattr(sys, 'frozen', False):
    # Running from PyInstaller bundle
    os.chdir(sys._MEIPASS)

def run_server():
    uvicorn.run("main:app", host="0.0.0.0", port=8005, reload=False)

def start_server():
    start_button.config(state=tk.DISABLED)  # Disable the button
    status_label.config(text="Starting server...")
    thread = Thread(target=run_server, daemon=True)
    thread.start()
    status_label.config(text="Server running at http://localhost:8005")

root = tk.Tk()
root.title("FastAPI Server Controller")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

start_button = tk.Button(frame, text="Start FastAPI Server", command=start_server)
start_button.pack(pady=10)

status_label = tk.Label(frame, text="Server not running.")
status_label.pack()

root.mainloop()
