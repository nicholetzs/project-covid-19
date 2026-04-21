from pathlib import Path
import os
import runpy

BASE_DIR = Path(__file__).resolve().parent
INNER_APP_DIR = BASE_DIR / ".devcontainer"
INNER_APP_FILE = INNER_APP_DIR / "app.py"

if not INNER_APP_FILE.exists():
    raise FileNotFoundError(
        f"Main module not found: {INNER_APP_FILE}. "
        "Check if .devcontainer/app.py exists."
    )

# Execute the real Streamlit app from its directory so relative imports and paths keep working.
os.chdir(INNER_APP_DIR)
runpy.run_path(str(INNER_APP_FILE), run_name="__main__")
