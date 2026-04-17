import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI

from pc_advisor.config import COMPONENT_FILES, DATASET_DIR, OPENAI_API_KEY
from pc_advisor.models import CompatibilityIssue
from pc_advisor.dataset import DatasetLoader, search_dataset
from pc_advisor.compatibility import run_compatibility_check
from pc_advisor.prompt import _compat_for_gpt, _fmt_compat, _dataset_block, build_full_prompt
from pc_advisor.llm import get_recommendations

# ---------------------------------------------------------------------------
# FastAPI server
# Run with:  uvicorn compatability:app --reload --port 8000
# ---------------------------------------------------------------------------

app = FastAPI(title="PC Build Advisor")
client = OpenAI(api_key=OPENAI_API_KEY)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
        ],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RunRequest(BaseModel):
    selected: dict[str, str]


class CompatibilityRequest(BaseModel):
    selected: dict[str, str]


def _build_searches(selected: dict[str, str]) -> tuple[list, float, str, str]:
    """
    Parse the `selected` dict from the frontend into the structures
    that the existing compatibility / prompt functions expect.
    Returns: (searches, budget, use_case, mode)
    """
    use_case   = selected.get("_use_case", "General use / gaming")
    mode       = selected.get("Mode", "Full PC build")
    budget_raw = selected.get("Budget", "0").replace("$", "").replace(",", "").strip()
    try:
        budget = float(budget_raw)
    except ValueError:
        budget = 0.0

    # Build preferences — blank out "(any)" placeholders the frontend sends
    preferences: dict[str, str] = {}
    for component in COMPONENT_FILES:
        val = selected.get(component, "")
        preferences[component] = "" if val in ("", "(any)") else val

    loader   = DatasetLoader(DATASET_DIR)
    searches = search_dataset(loader, preferences)
    return searches, budget, use_case, mode


def _selected_components(selected: dict[str, str]) -> set[str]:
    chosen: set[str] = set()
    for component in COMPONENT_FILES:
        val = (selected.get(component) or "").strip()
        if val and val != "(any)":
            chosen.add(component)
    return chosen


def _filter_issues_for_selected(
    issues: list[CompatibilityIssue],
    selected_components: set[str],
) -> list[CompatibilityIssue]:
    # Show only checks where every involved component was selected.
    if not selected_components:
        return []
    return [
        issue
        for issue in issues
        if all(component in selected_components for component in issue.components)
    ]

@app.post("/compatibility")
def compatibility_endpoint(req: CompatibilityRequest):
    """
    Endpoint for compatibility checks
    """
    searches, _, _, _ = _build_searches(req.selected)
    selected_components = _selected_components(req.selected)
    issues = _filter_issues_for_selected(run_compatibility_check(searches), selected_components)
    compat_text = _fmt_compat(issues)
    return {"compat_issues": compat_text}


@app.post("/run")
def run_endpoint(req: RunRequest):
    """
    Single-call endpoint — returns both compat issues and full AI output at once.
    Frontend sets setCompatIssues and setAiOutput from the response.
    """
    searches, budget, use_case, mode = _build_searches(req.selected)
    selected_components = _selected_components(req.selected)

    issues       = _filter_issues_for_selected(run_compatibility_check(searches), selected_components)
    compat_text  = _fmt_compat(issues)
    compat_block = _compat_for_gpt(issues)
    dataset_blk  = _dataset_block(searches)

    preferences = {c: (req.selected.get(c) or "") for c in COMPONENT_FILES}
    prompt      = build_full_prompt(preferences, budget, use_case, dataset_blk, compat_block, mode)

    ai_output = get_recommendations(client, prompt)

    return {"compat_issues": compat_text, "ai_output": ai_output}


@app.post("/stream")
def stream_endpoint(req: RunRequest):
    """
    Streaming endpoint (SSE).
    Sends compat issues first, then streams AI tokens.
    Event format:  data: {"type": "compat"|"token"|"done", "text": "..."}
    """
    searches, budget, use_case, mode = _build_searches(req.selected)
    selected_components = _selected_components(req.selected)

    issues       = _filter_issues_for_selected(run_compatibility_check(searches), selected_components)
    compat_text  = _fmt_compat(issues)
    compat_block = _compat_for_gpt(issues)
    dataset_blk  = _dataset_block(searches)

    preferences = {c: (req.selected.get(c) or "") for c in COMPONENT_FILES}
    prompt      = build_full_prompt(preferences, budget, use_case, dataset_blk, compat_block, mode)
    def generate():
        # Send compat results immediately so the UI updates before AI starts
        yield f"data: {json.dumps({'type': 'compat', 'text': compat_text})}\n\n"

        with client.chat.completions.stream(
            model="gpt-4o",
            max_tokens=2500,
            temperature=0.7,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior PC hardware expert. "
                        "You have deep knowledge of CPU socket compatibility, chipset features, "
                        "RAM DDR generations, PSU sizing, case form factors, GPU power requirements, "
                        "NVMe generations, and current market pricing as of early 2025. "
                        "You independently verify compatibility rather than just repeating automated checks. "
                        "You prioritize recommending the best parts for the user's use case and budget. "
                        "You are direct and specific: name exact incompatibilities and always suggest a fix."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        ) as stream:
            for event in stream:
                #print(event)
                if event.type == "response.output_text.delta":
                    yield f"data: {json.dumps({'type': 'token', 'text': event.delta})}\n\n"
                elif event.type == "content.delta":
                    yield f"data: {json.dumps({'type': 'token', 'text': event.delta})}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
