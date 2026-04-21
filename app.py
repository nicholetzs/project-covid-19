from pathlib import Path
import os
import runpy

BASE_DIR = Path(__file__).resolve().parent

CANDIDATE_APP_PATHS = [
    BASE_DIR / "kdd" / ".devcontainer" / "app.py",
    BASE_DIR / "kdd" / "app.py",
    BASE_DIR / ".devcontainer" / "app.py",
]

app_file = next((p for p in CANDIDATE_APP_PATHS if p.exists()), None)

if app_file is None:
    searched = "\n".join(str(p) for p in CANDIDATE_APP_PATHS)
    raise FileNotFoundError(
        "Could not find Streamlit main module. Checked:\n"
        f"{searched}\n"
        "Set Streamlit main file path to a valid app.py in the repository."
    )

# Run from the app file directory so relative imports and local data paths keep working.
os.chdir(app_file.parent)
runpy.run_path(str(app_file), run_name="__main__")
