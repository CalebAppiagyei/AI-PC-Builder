"""
CLI entry point for the PC Build Advisor.

Setup:
    pip install openai python-dotenv
    git clone https://github.com/docyx/pc-part-dataset
    # Place this script next to the cloned repo, or set DATASET_DIR env var.

Run:
    python -m pc_advisor.cli
"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

from .config import COMPONENT_FILES, DATASET_DIR
from .models import CompatibilityIssue
from .dataset import DatasetLoader, search_dataset
from .compatibility import run_compatibility_check
from .prompt import _compat_for_gpt, _dataset_block, build_full_prompt
from .llm import get_recommendations

# ---------------------------------------------------------------------------
# User input  (based on prototype.py)
# ---------------------------------------------------------------------------

def prompt_user_inputs() -> tuple[dict[str, str], float]:
    print("\n" + "=" * 60)
    print("        PC BUILD ADVISOR")
    print("=" * 60)
    print("Let's gather your preferences for each component.")
    print("Leave a field blank if you have no preference.\n")

    preferences: dict[str, str] = {}
    for component in COMPONENT_FILES:
        value = input(f"  {component}: ").strip()
        preferences[component] = value if value else ""

    print()
    while True:
        budget_str = input("What is your total budget (USD)? $").strip()
        try:
            budget = float(budget_str.replace(",", ""))
            if budget <= 0:
                raise ValueError
            break
        except ValueError:
            print("   Please enter a valid positive number.")

    print()
    use_case = input(
        "What will you primarily use this PC for?\n"
        "   (e.g., gaming, video editing, 3D rendering, general use): "
    ).strip()
    if not use_case:
        use_case = "General use / gaming"

    preferences["_use_case"] = use_case
    return preferences, budget


def get_api_key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        key = input("Enter your OpenAI API key: ").strip()
    return key



# ---------------------------------------------------------------------------
# Main  (based on prototype.py structure)
# ---------------------------------------------------------------------------

def main():
    load_dotenv()

    # Verify dataset directory exists
    if not DATASET_DIR.exists():
        print(f"\nERROR: Dataset directory not found: {DATASET_DIR}")
        print("Clone the dataset repo first:")
        print("  git clone https://github.com/docyx/pc-part-dataset")
        print("Then run this script from the same directory, or set:")
        print("  export DATASET_DIR=/path/to/pc-part-dataset")
        sys.exit(1)

    api_key = get_api_key()
    client  = OpenAI(api_key=api_key)

    # Step 1: gather user inputs
    preferences, budget = prompt_user_inputs()
    use_case = preferences.pop("_use_case", "General use / gaming")

    # Step 2: search local dataset for matching parts
    loader   = DatasetLoader(DATASET_DIR)
    searches = search_dataset(loader, preferences)

    # Step 3: run compatibility checks (zero extra API calls)
    issues       = run_compatibility_check(searches)
    compat_block = _compat_for_gpt(issues)
    dataset_blk  = _dataset_block(searches)

    # Step 4: build prompt and call GPT-4o (single call)
    prompt          = build_full_prompt(preferences, budget, use_case, dataset_blk, compat_block, "Full PC build")
    recommendations = get_recommendations(client, prompt)

    print(recommendations)
    print("=" * 60)

    # Step 5: optionally save full report
    save = input("\nWould you like to save these recommendations to a file? (y/n): ").strip().lower()
    if save == "y":
        filename = "pc_build_recommendations.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("PC BUILD ADVISOR — FULL REPORT\n")
            f.write("=" * 60 + "\n\n")

            f.write("--- COMPATIBILITY PRE-CHECK ---\n\n")
            for issue in issues:
                f.write(f"  [{issue.severity}] ({', '.join(issue.components)})\n")
                f.write(f"    {issue.message}\n\n")

            f.write("\n--- DATASET SEARCH RESULTS ---\n\n")
            for cs in searches:
                f.write(f"[{cs.category}]  Preference: {cs.user_preference or 'None'}\n")
                if cs.error:
                    f.write(f"  Error: {cs.error}\n\n")
                    continue
                for m in cs.matches:
                    ps = f"${m.price:,.2f}" if m.price else "N/A"
                    f.write(f"  - {m.name}  |  {ps}\n")
                    specs = [k for k in m.data if k not in ("name", "price") and m.data[k] is not None]
                    for k in specs[:8]:
                        f.write(f"    {k}: {m.data[k]}\n")
                f.write("\n")

            f.write("\n--- GPT-4o RECOMMENDATIONS ---\n\n")
            f.write(recommendations)
            f.write("\n\n" + "=" * 60 + "\n")

        print(f"Recommendations saved to '{filename}'")

    print("\nHappy building!\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled by user.\n")
        sys.exit(0)
