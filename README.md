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

in Windows pyscard can be one of the requirements
```
pyscard
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

(With venv active)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --noconfirm --name IDCardServer --icon icon.ico --add-data "icon.ico;." start_server.py
```

`icon.ico` is generated from `icon.png` (padded to square, white corners made transparent, 16–256 px). On Linux/macOS use `--add-data "icon.ico:."`.

Output: `dist/IDCardServer.exe`. No `--hidden-import` / `--add-data` flags are needed: `start_server.py` imports `main` directly, so PyInstaller finds every module on its own.

---

## ⚠️ Notes

- `pyscard` does **not bundle well in venv** — use global install for building.
- However, `pyscard` works perfectly on venv(s) in Windows.
- Make sure your smartcard drivers are available on your platform..