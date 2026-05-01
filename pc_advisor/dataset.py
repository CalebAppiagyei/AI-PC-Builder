import json
from pathlib import Path

from pc_advisor.models import ComponentSearch, PartMatch
from pc_advisor.config import COMPONENT_FILES, MAX_SEARCH_RESULTS

# ---------------------------------------------------------------------------
# Dataset loader
# ---------------------------------------------------------------------------

class DatasetLoader:
    """Loads and caches JSON files from the cloned pc-part-dataset repo."""

    def __init__(self, dataset_dir: Path):
        self.dataset_dir = dataset_dir
        self._cache: dict[str, list[dict]] = {}

    def load(self, filename: str) -> list[dict]:
        if filename in self._cache:
            return self._cache[filename]

        path = self.dataset_dir / f"{filename}.json"
        if not path.exists():
            raise FileNotFoundError(
                f"Dataset file not found: {path}\n"
                f"Clone https://github.com/docyx/pc-part-dataset next to this script,\n"
                f"or set the DATASET_DIR environment variable."
            )

        with open(path, encoding="utf-8") as f:
            raw = json.load(f)

        records: list[dict] = (
            raw if isinstance(raw, list)
            else raw.get("data", raw.get("parts", list(raw.values())[0] if raw else []))
        )
        self._cache[filename] = records
        return records

    def search(self, filename: str, query: str) -> list[PartMatch]:
        """
        Case-insensitive token search over part names.
        Returns up to MAX_SEARCH_RESULTS matches sorted by relevance then price.
        """
        if not query.strip():
            return []

        records    = self.load(filename)
        q_lower    = query.lower().strip()
        tokens     = q_lower.split()
        scored: list[tuple[int, PartMatch]] = []

        for rec in records:
            name       = rec.get("name", "")
            name_lower = name.lower()
            if all(t in name_lower for t in tokens):
                score     = 2 if name_lower.startswith(q_lower) else 1
                price_raw = rec.get("price")
                price     = float(price_raw) if price_raw is not None else None
                scored.append((score, PartMatch(name=name, price=price, data=rec)))

        scored.sort(key=lambda x: (-x[0], x[1].price if x[1].price is not None else 1e9))
        return [m for _, m in scored[:MAX_SEARCH_RESULTS]]

    def top(self, filename: str) -> list[PartMatch]:
        """Return the first MAX_SEARCH_RESULTS records (used when user has no preference)."""
        records = self.load(filename)
        results = []
        for rec in records[:MAX_SEARCH_RESULTS]:
            price_raw = rec.get("price")
            price     = float(price_raw) if price_raw is not None else None
            results.append(PartMatch(name=rec.get("name", "Unknown"), price=price, data=rec))
        return results

# ---------------------------------------------------------------------------
# Dataset search
# ---------------------------------------------------------------------------

def search_dataset(loader: DatasetLoader, preferences: dict[str, str]) -> list[ComponentSearch]:
    results: list[ComponentSearch] = []

    print("\n" + "=" * 60)
    print("  Searching local pc-part-dataset...")
    print("=" * 60)

    for component, preference in preferences.items():
        filename = COMPONENT_FILES.get(component, "")
        cs = ComponentSearch(category=component, user_preference=preference)

        print(f"\n  [{component}]  query: \"{preference or '(any)'}\"")

        if not filename:
            cs.error = "No dataset file mapped."
            results.append(cs)
            continue

        try:
            matches = loader.search(filename, preference) if preference else loader.top(filename)
            if not matches:
                print("    No matches found.")
                cs.error = "No matches found in dataset."
            else:
                for m in matches:
                    ps = f"${m.price:,.2f}" if m.price else "Price N/A"
                    print(f"    - {m.name[:55]:55s}  {ps}")
                cs.matches = matches
        except FileNotFoundError as exc:
            cs.error = str(exc)
            print(f"    ERROR: {exc}")

        results.append(cs)

    return results
