import tkinter as tk
from threading import Thread
import uvicorn
import os
import sys
import socket

if getattr(sys, 'frozen', False):
    # Running from PyInstaller bundle
    os.chdir(sys._MEIPASS)

def is_port_in_use(port, host="127.0.0.1"):
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def run_server():
    uvicorn.run("main:app", host="0.0.0.0", port=8005, reload=False)

def start_server():
    if is_port_in_use(8005):
        status_label.config(text="❌ Port 8005 is already in use.")
        return

    start_button.config(state=tk.DISABLED)
    status_label.config(text="Starting server...")
    thread = Thread(target=run_server, daemon=True)
    thread.start()
    status_label.config(text="✅ Server running at http://localhost:8005")

root = tk.Tk()
root.title("ID Card Reader Server")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

start_button = tk.Button(frame, text="Start ID Card Server", command=start_server)
start_button.pack(pady=10)

status_label = tk.Label(frame, text="Server not running.")
status_label.pack()

root.mainloop()
