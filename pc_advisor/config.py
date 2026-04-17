import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_SCRIPT_DIR = Path(__file__).parent
DATASET_DIR = Path(os.environ.get("DATASET_DIR", _SCRIPT_DIR / "pc-part-dataset")) / "data" / "json"

OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set")

# Maps user-facing component names to dataset JSON filenames (without .json)
COMPONENT_FILES: dict[str, str] = {
    "CPU":                "cpu",
    "CPU Cooler":         "cpu-cooler",
    "Motherboard":        "motherboard",
    "Memory (RAM)":       "memory",
    "Storage":            "internal-hard-drive",
    "Video Card (GPU)":   "video-card",
    "Case":               "case",
    "Power Supply (PSU)": "power-supply",
    "Operating System":   "os",
    "Monitor":            "monitor",
}

MAX_SEARCH_RESULTS = 5