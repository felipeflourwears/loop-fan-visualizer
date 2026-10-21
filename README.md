# Loop Fan Visualizer

**Loop Fan Visualizer** is a Python-based circular video player designed to display looping videos inside a circular masked window—perfect for 3D fan displays or round LED screens. The app runs videos continuously from a specified folder, resizing and rendering each frame in a smooth circular interface.

Features:
- Circular video playback in a loop from the `media/` folder.
- Remote control web page (Flask) to switch to the next/previous video from a phone.
- Optional sync of the playlist from a Google Drive folder (one folder per fan).

---

## 🛠 Project Setup

### 1. Virtual environment and dependencies

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment variables (`.env`)

Copy the example file and fill in the values for this machine:

```bash
copy .env.example .env
```

| Variable | Description | Default |
|---|---|---|
| `DRIVE_FOLDER_ID` | Google Drive folder ID for this fan. Leave empty to disable sync. | _(empty)_ |
| `GOOGLE_CREDENTIALS_PATH` | Path to the Google service account JSON. | `credentials/service_account.json` |
| `MEDIA_DIR` | Local folder where videos are stored. | `media` |
| `SYNC_INTERVAL_SECONDS` | Seconds between Drive syncs. | `600` |
| `SERVER_HOST` | Host for the remote control server. | `0.0.0.0` |
| `SERVER_PORT` | Port for the remote control server. | `5000` |

> 🔒 **Never commit secrets.** `.env`, `config.json`, `credentials/` and any service account JSON are ignored by git. Only `.env.example` (without real values) is versioned.
>
> `config.json` (see `config.example.json`) is still supported as a fallback when `DRIVE_FOLDER_ID` is not set.

### 3. Google Drive sync (optional)

1. Create a service account in Google Cloud and enable the Drive API.
2. Download its JSON key and save it as `credentials/service_account.json`.
3. Share the fan's Drive folder with the service account email (read-only is enough).
4. Set `DRIVE_FOLDER_ID` in `.env`.

Manual one-time sync:

```bash
python drive_sync.py --credentials credentials/service_account.json --folder-id <FOLDER_ID> --once
```

### 4. Run

```bash
python main.py
```

Remote control: open `http://<fan-ip>:5000` from a phone on the same network.

### Init Setup (kiosk mode)

Put a shortcut to `start_ventilador.bat` in the Windows Startup folder:

```
C:\Users\<Nombre de usuario>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

`start_ventilador.bat` runs from its own folder, activates `venv` and starts `main.py`.
