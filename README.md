## 🛠️ Installation

> ❗ Note: `pyscard` must be installed **globally**, not in a virtual environment.

```bash
pip install pyscard==2.0.7 fastapi uvicorn
```

Test `pyscard` installation:

```bash
python3 -c "from smartcard.System import readers; print(readers())"
```

---

## 🧪 Running the Server (for development)

```bash
uvicorn main:app --reload --port 8005
```

Or via the GUI:

```bash
python start_server.py
```

---

## 🧰 Step 1: Create and Activate Virtual Environment

### 🐧 Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 🪟 Windows

```cmd
python -m venv venv
venv\Scripts\activate
```

---

## 📦 Step 2: Install Dependencies

Ensure `requirements.txt` contains:

```
fastapi
uvicorn
```

Then install:

```bash
pip install -r requirements.txt
```

---

## 🚀 Step 3: Run the App

You can either run it manually:

```bash
uvicorn main:app --host 0.0.0.0 --port 8005
```

Or use the tkinter GUI:

```bash
python start_server.py
```

---

## 🔧 Step 4: Build Executable with PyInstaller

(Outside venv or with system Python due to pyscard limitations)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed \
  --hidden-import=fastapi.middleware.cors \
  --hidden-import=fastapi.middleware \
  --hidden-import=fastapi \
  --hidden-import=uvicorn \
  --hidden-import=pyscard \
  --hidden-import=smartcard.System \
  --hidden-import=smartcard.util \
  --collect-submodules=smartcard \
  --add-data "main.py:." \
  --add-data "DataThaiCID.py:." \
  --add-data "ThaiCIDHelper.py:." \
  start_server.py
```

---

## ⚠️ Notes

- `pyscard` does **not bundle well in venv** — use global install for building.
- Make sure your smartcard drivers are available on your platform.