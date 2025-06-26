# 🚀 Build and Package FastAPI ThaiCID Reader App

This guide explains how to set up a Python virtual environment, install dependencies, and compile your FastAPI app into a standalone executable using PyInstaller.

---

## ✅ 1. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
# Activate the environment

# For Linux/macOS:
source venv/bin/activate

# For Windows:
venv\Scripts\activate
```

---

## ✅ 2. Install Required Python Packages from `requirements.txt`

```bash
pip install -r requirements.txt
```

---

## ✅ 3. Install System-Level Dependencies (if not already installed)

Some packages like `pyscard` require additional system libraries.

### 🐧 For Fedora / RHEL / CentOS:

```bash
sudo dnf install pcsc-lite-devel swig gcc python3-devel
```

### 🐧 For Ubuntu / Debian:

```bash
sudo apt install libpcsclite-dev swig build-essential python3-dev
```

---

## ✅ 4. Compile the App into a Standalone Executable

```bash
pyinstaller --onefile start_server.py
```

> 🔒 Optional: Add hidden imports if needed

```bash
pyinstaller --onefile --hidden-import=smartcard start_server.py
```

---

## ✅ 5. Run the Compiled Binary

```bash
./dist/start_server       # Linux/macOS
dist\start_server.exe    # Windows
```

Your FastAPI server will be available at:  
**http://localhost:8005**

---