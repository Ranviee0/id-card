# Thai ID Card Reader Server

Reads Thai national ID cards through a PC/SC smart card reader and serves the data over a local HTTP API (FastAPI) on port **8005**. A small tkinter window starts and stops the server.

| Endpoint | Returns |
|---|---|
| `GET /read-cid` | Card data as JSON (CID, names split into title / first / last, address split into parts, dates, …) |
| `GET /read-photo` | The photo stored on the card (JPEG) |
| `GET /docs` | Interactive API page for testing |

There is no page at `/`, so `http://localhost:8005/` returns `{"detail":"Not Found"}`. That is expected.

---

## 🪟 Build from source on Windows

The result is a single file, `dist\IDCardServer.exe`, that runs on any 64-bit Windows 10/11 PC without Python installed.

### Requirements

| | |
|---|---|
| OS | Windows 10 or 11, 64-bit |
| Python | **3.13** (64-bit). Not 3.14: `pyscard` has no prebuilt package for 3.14 yet, and installing it would need a C compiler. |
| Git | To clone the repo ([git-scm.com](https://git-scm.com/download/win)), or download the ZIP from GitHub instead |
| Hardware | A PC/SC smart card reader (only needed to *test*, not to build) |

### Step 1: Install Python 3.13

Either:

- **Python install manager** (Windows 11 / recent Python): open PowerShell and run
  ```powershell
  py install 3.13
  ```
- **or** the installer from [python.org/downloads](https://www.python.org/downloads/windows/). Pick the latest *Python 3.13.x, Windows installer (64-bit)*. Keep "tcl/tk and IDLE" checked (the GUI needs tkinter).

Check it:

```powershell
py -V:3.13 --version
```

### Step 2: Get the source

```powershell
git clone https://github.com/Ranviee0/id-card.git
cd id-card
```

All following commands are run from this `id-card` folder.

### Step 3: Allow PowerShell to activate the virtual environment (one time)

Windows blocks PowerShell scripts by default, which includes the venv's `Activate.ps1`. Allow local scripts for your user (no admin needed):

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Skip this if you use **Command Prompt (cmd)** instead of PowerShell. There, activate with `.venv\Scripts\activate.bat` in Step 4.

### Step 4: Create and activate the virtual environment

```powershell
py -V:3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Your prompt should now start with `(.venv)`. Run the activate line again in every new terminal.

### Step 5: Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyscard==2.3.1 pyinstaller==6.22.3
```

`pyscard` works fine inside the virtual environment on Windows. Older advice to install it globally applies to Linux/macOS only.

### Step 6: Check the card reader (optional but recommended)

Plug in the reader, then:

```powershell
python -c "from smartcard.System import readers; print(readers())"
```

You should see your reader's name in a list, e.g. `['ACS ACR39U ICC Reader 0']`. An empty list `[]` means no reader was detected; see [Troubleshooting](#-troubleshooting).

### Step 7: Run from source (optional)

```powershell
python start_server.py
```

Click **Start ID Card Server**, insert a card, and open <http://localhost:8005/read-cid>.

Or run the API alone, with auto-reload while editing code:

```powershell
uvicorn main:app --reload --port 8005
```

### Step 8: Build the executable

```powershell
pyinstaller --onefile --windowed --noconfirm --name IDCardServer --icon icon.ico --add-data "icon.ico;." start_server.py
```

Output: **`dist\IDCardServer.exe`** (about 17 MB). Copy that one file to any Windows PC and run it.

- `--onefile`: everything packed into one `.exe`
- `--windowed`: no black console window behind the GUI
- `--icon`: the icon shown in Explorer and the taskbar
- `--add-data "icon.ico;."`: bundles the icon so the app window can show it too

No `--hidden-import` flags are needed: `start_server.py` imports `main` directly, so PyInstaller finds every module (including `pyscard`) on its own.

The build also creates `build\` and `IDCardServer.spec`. Both are regenerated on every build and can be deleted.

> **Rebuild fails with `PermissionError: [WinError 5] Access is denied`?**
> `IDCardServer.exe` is still running. Close its window (and check Task Manager), then build again.

---

## 🎨 Changing the icon

`icon.ico` (committed) is generated from `icon.png`. The image is centered on a square transparent canvas (Windows icons must be square), its white corners are made transparent, and it's saved at 16–256 px. To regenerate it after changing `icon.png`:

```powershell
pip install pillow
python -c "from PIL import Image, ImageDraw; s=Image.open('icon.png').convert('RGBA'); w,h=s.size; [ImageDraw.floodfill(s,xy,(255,255,255,0),thresh=40) for xy in [(0,0),(w-1,0),(0,h-1),(w-1,h-1)]]; n=max(w,h); q=Image.new('RGBA',(n,n)); q.paste(s,((n-w)//2,(n-h)//2),s); q.resize((256,256),Image.LANCZOS).save('icon.ico',sizes=[(x,x) for x in (16,24,32,48,64,128,256)])"
```

Then rebuild (Step 8). If Explorer still shows the old icon, that's the Windows icon cache. Renaming or moving the `.exe` refreshes it.

---

## 🧯 Troubleshooting

| Problem | Fix |
|---|---|
| `Activate.ps1 cannot be loaded because running scripts is disabled` | Do Step 3, or skip activation and call `.\.venv\Scripts\python.exe` directly. |
| `No matching distribution found for pyscard` | You're on the wrong Python (e.g. 3.14). Delete `.venv` and recreate it with `py -V:3.13 -m venv .venv`. |
| `readers()` prints `[]` | Reader not connected or driver missing. Check it appears in Device Manager under *Smart card readers*, and that the service runs: `Get-Service SCardSvr` should say `Running`. |
| `Port 8005 is already in use` in the app | Another copy is already running. Close it (check Task Manager for `IDCardServer.exe`). |
| Windows Firewall prompt when starting the server | The server listens on all network interfaces (`0.0.0.0`). Allow it for other PCs on the network to reach the API, or deny it if only this PC uses it. |
| "Windows protected your PC" when running the `.exe` on another PC | Normal for unsigned executables. Click *More info → Run anyway*. |
| Antivirus flags the `.exe` | A known false positive for PyInstaller one-file builds. Add an exception, or build without `--onefile`. |

---

## 🐧 Linux / macOS (development only)

The build steps above are for Windows. To run from source on Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pyscard
python start_server.py
```

On Linux, `pyscard` needs the PC/SC daemon and headers (e.g. `sudo apt install pcscd libpcsclite-dev swig`). When building with PyInstaller there, use `--add-data "icon.ico:."` (colon instead of semicolon).
