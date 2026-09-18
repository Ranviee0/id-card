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
    # Import here (not as a "main:app" string) so PyInstaller bundles main and its imports.
    # Deferred so the card reader isn't opened until the server is started.
    from main import app
    # log_config=None: in a --windowed build sys.stdout is None and uvicorn's default logging crashes.
    uvicorn.run(app, host="0.0.0.0", port=8005, reload=False, log_config=None)

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
icon_dir = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
try:
    root.iconbitmap(os.path.join(icon_dir, "icon.ico"))
except tk.TclError:
    pass  # Missing icon shouldn't stop the server GUI

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

start_button = tk.Button(frame, text="Start ID Card Server", command=start_server)
start_button.pack(pady=10)

status_label = tk.Label(frame, text="Server not running.")
status_label.pack()

root.mainloop()
