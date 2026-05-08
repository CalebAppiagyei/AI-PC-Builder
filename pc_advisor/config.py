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
    #raise RuntimeError("OPENAI_API_KEY environment variable is not set")
    print("You need a key.")

# Maps user-facing component names to database table names
COMPONENT_TABLES: dict[str, str] = {
    "CPU":                "cpus",
    "CPU Cooler":         "cpu_coolers",
    "Motherboard":        "motherboards",
    "Memory (RAM)":       "memory",
    "Storage":            "internal_hard_drives",
    "Video Card (GPU)":   "video_cards",
    "Case":               "cases",
    "Power Supply (PSU)": "power_supplies",
    "Operating System":   "operating_systems",
    "Monitor":            "monitors",
}

MAX_SEARCH_RESULTS = 5