NEXUS Portable AI Terminal v1.0.0

WHAT IS NEXUS?
NEXUS is a lightweight, keyboard-only AI terminal that runs directly
from a USB drive. No installation, no API keys, no internet required
for core features.

EXE LAUNCHER (WINDOWS)
1. Copy the entire NEXUS_USB folder to your USB drive.
2. Plug the USB into a Windows computer.
3. Open NEXUS_USB\dist\
4. Double-click NEXUS.exe
5. Login with your credentials.

BATCH LAUNCHER (WINDOWS / LINUX)
- Windows: double-click START_NEXUS.bat
- Linux: bash START_NEXUS.sh
These require Python 3.8+ installed on the host computer.

LOGIN CREDENTIALS (DEMO)
Default users:
  achyut / 200712
  guest / guest

You can switch users from the top-right dropdown in the terminal.

AVAILABLE COMMANDS
  help              - Show this help
  clear / cls       - Clear terminal
  status            - System status
  calculate <expr>  - Safe calculator
  notes             - List notes
  notes add <title> - Create note
  notes search <q>  - Search notes
  notes delete <id> - Delete note
  files             - List files in USB/data
  files <path>      - List specific path
  search <query>    - Search files
  history           - Command history
  history clear     - Clear history
  about             - About NEXUS
  version           - Version info
  logout / exit     - Logout
  demo              - Exhibition mode
  time / date       - Show current date and time
  open <site/url>   - Open website in default browser

You can also ask natural questions like:
  "what is Python?"
  "explain gravity"
  "who is Gandhi?"
  "tell me about space"
  "how does photosynthesis work?"
  "calculate 25 * 17"
  "open youtube"

MODEL SUPPORT
NEXUS supports local GGUF AI models for offline intelligence.

USING THE EXE:
1. Click the BROWSE button in the terminal header.
2. Select any .gguf model file from anywhere on the computer.
3. NEXUS will remember it for next time.

USING PYTHON MODE:
1. Place a .gguf file in the models/ folder.
2. Install ctransformers on the host: pip install ctransformers
3. Start NEXUS; it auto-detects the model.

RECOMMENDED FREE MODELS:
- Qwen2.5-1.5B-Instruct Q4_K_M (~1 GB)
- TinyLlama 1.1B Chat Q4_K_M (~637 MB)

OFFLINE LIMITATIONS
- Core features work fully offline.
- No cloud AI, no API calls, no microphone, no speaker.
- Local model inference is optional.

STORAGE BUDGET
- Application: ~1.09 GB (EXE)
- Models: optional, user-provided
- Total target: well below 3.72 GB when used on USB

NEXUS stores all user data on the USB drive. No data is stored on the host computer.

TROUBLESHOOTING
- EXE is large because it bundles Python and Tkinter.
- If model inference is slow, use a smaller quantized GGUF file.
- If the EXE fails, try running START_NEXUS.bat with Python installed.
