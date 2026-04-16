import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_SCRIPT_DIR = Path(__file__).parent
# Override with env var DATASET_DIR if the repo is elsewhere
DATASET_DIR = Path(os.environ.get("DATASET_DIR", _SCRIPT_DIR / "pc-part-dataset")) / "data" / "json"

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