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

## 🔧 Building Standalone Executable

Use `PyInstaller`:

```bash
pip install pyinstaller
```

Then run:

```bash
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

Result:

```
dist/start_server     # Linux
dist/start_server.exe # Windows
```

---

## ⚠️ Troubleshooting

- ❌ `ModuleNotFoundError: No module named 'smartcard'`  
  → Ensure `pyscard` is installed globally.

- 🐧 On Linux, make sure you have PC/SC daemon and readers installed:
  ```bash
  sudo apt install pcscd libpcsclite1
  sudo systemctl start pcscd
  ```

- 🪟 On Windows, install appropriate smartcard drivers.

---

## 📚 References

- [FastAPI Docs](https://fastapi.tiangolo.com)
- [pyscard Docs](https://pyscard.sourceforge.io/)
- [PC/SC Overview](https://pcsclite.apdu.fr/)

---

## 👨‍💼 Author

Woraphet Rueangpornvisut  
📅 Updated: Jan 2024  
📄 Python 3.11.5