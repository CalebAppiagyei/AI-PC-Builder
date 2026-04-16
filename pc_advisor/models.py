from dataclasses import dataclass, field
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class PartMatch:
    name:  str
    price: Optional[float]       # None if unlisted in dataset
    data:  dict[str, Any]        # full raw record from JSON


@dataclass
class ComponentSearch:
    category:        str
    user_preference: str
    matches:         list[PartMatch] = field(default_factory=list)
    error:           Optional[str]   = None


ERROR   = "ERROR"
WARNING = "WARNING"
INFO    = "INFO"


@dataclass
class CompatibilityIssue:
    severity:   str          # ERROR | WARNING | INFO
    components: list[str]
    message:    str