from pc_advisor.models import CompatibilityIssue, ComponentSearch, ERROR, WARNING, INFO

def _compat_for_gpt(issues: list[CompatibilityIssue]) -> str:
    if not issues:
        return "No compatibility issues detected."
    return "\n".join(
        f"[{i.severity}] ({', '.join(i.components)}) {i.message}"
        for i in issues
    )

def _fmt_compat(issues: list) -> str:
    """Format compat issues for the frontend Compatibility Issues panel."""
    if not issues:
        return "No compatibility issues detected."

    lines: list[str] = []
    for sev, label in [(ERROR, "ERRORS"), (WARNING, "WARNINGS"), (INFO, "NOTES")]:
        group = [i for i in issues if i.severity == sev]
        if not group:
            continue
        lines.append(f"── {label} ──")
        for issue in group:
            icon = {"ERROR": "❌", "WARNING": "⚠️", "INFO": "ℹ️"}.get(issue.severity, "•")
            lines.append(f"{icon}  [{', '.join(issue.components)}]")
            lines.append(f"   {issue.message}")
            lines.append("")

    errors   = sum(1 for i in issues if i.severity == ERROR)
    warnings = sum(1 for i in issues if i.severity == WARNING)
    infos    = sum(1 for i in issues if i.severity == INFO)
    lines.append(f"Summary: {errors} error(s), {warnings} warning(s), {infos} note(s)")
    return "\n".join(lines)

# ---------------------------------------------------------------------------
# GPT-4o prompt + call  (based on prototype.py)
# ---------------------------------------------------------------------------

def _dataset_block(searches: list[ComponentSearch]) -> str:
    lines: list[str] = []
    for cs in searches:
        lines.append(f"\n### {cs.category}")
        lines.append(f"  User preference: {cs.user_preference or 'None (any)'}")
        if cs.error:
            lines.append(f"  Data: UNAVAILABLE — {cs.error}")
            continue
        if not cs.matches:
            lines.append("  Data: No matches found.")
            continue
        lines.append(f"  Dataset matches ({len(cs.matches)}):")
        for i, m in enumerate(cs.matches, 1):
            ps = f"${m.price:,.2f}" if m.price else "N/A"
            lines.append(f"    {i}. {m.name}  |  Price (may be outdated): {ps}")
            specs = [k for k in m.data if k not in ("name", "price") and m.data[k] is not None]
            preview = ", ".join(f"{k}: {m.data[k]}" for k in specs[:8])
            if preview:
                lines.append(f"       Specs: {preview}")
    return "\n".join(lines)

def build_full_prompt(
    preferences: dict[str, str],
    budget: float,
    use_case: str,
    dataset_block: str,
    compat_block: str,
    mode: str,
) -> str:
    mode = "a PC build" if mode == "Full PC build" else "to upgrade their current PC build"
    budget_type = "all-inclusive" if mode == "a PC build" else "for new parts"
    selection_type = "preferences" if mode == "a PC build" else "current components"
    goal = "If a better part exists within budget — better performance, better value, better compatibility — recommend it instead and briefly explain why it's the superior choice." if mode == "a PC build " else "You should recommend new parts within the given budget with the goal of maximizing performance, value, and compatibility. This is an upgrade to their current build so recommendations should be given keeping in mind their current build and the fact that their budget excludes these parts as they already own them."
    est = "" if mode == "a PC build" else ", only sum the price of the components that are different from the users current components"
    return f"""You are a senior PC hardware expert with deep knowledge of component \
compatibility, current market prices, and performance benchmarking. A user is planning \
{mode} and needs your expert guidance.

You have been given two inputs to work from:
  1. A rule-based compatibility pre-check (automated, may miss edge cases or be wrong)
  2. Dataset search results showing parts that matched the user's {selection_type}

Your job is NOT to simply repeat this data back. You are the expert — use the pre-check \
as a starting point, then apply your own knowledge to verify, correct, and expand on it.

===========================================================
BUILD CONTEXT
===========================================================
Budget      : ${budget:,.2f} USD ({budget_type})
Use Case    : {use_case}

===========================================================
AUTOMATED COMPATIBILITY PRE-CHECK  (verify and expand on this)
===========================================================
{compat_block}

The pre-check above is rule-based and has limitations. You must:
- Confirm or correct each finding with your own expertise
- Catch anything the automated check missed (e.g. PCIe lane conflicts, power connector
  requirements, cooler clearance, RAM XMP support, NVMe gen mismatches, etc.)
- Add your own compatibility observations even if the automated check found nothing

===========================================================
DATASET MATCHES  (user {selection_type} + closest parts found)
===========================================================
{dataset_block}

NOTE: Dataset prices are from a historical PCPartPicker snapshot and are likely outdated.
Treat them as rough ballpark figures only.

===========================================================
YOUR RECOMMENDATIONS
===========================================================
The user's stated {selection_type} are a STARTING POINT, not a constraint. {goal}

For each component provide a section with:
  • Your recommended part (name + model)
  • Estimated current market price (your knowledge, not the dataset)
  • Why this is the best choice for the use case and budget
  • Any compatibility notes specific to this part

Then provide:

**Compatibility Assessment**
Your independent compatibility verdict for the full build. Address every issue the
automated pre-check flagged, confirm or correct each one, and add anything it missed.
Be direct: if parts are incompatible, say so clearly and explain exactly why and what
to replace.

**Total Estimated Cost**
Sum of your recommended parts at current market prices{est}. State whether it fits the budget.
If over budget, suggest which components to downgrade and by how much.

**Performance Notes**
Expected real-world performance for {use_case}. Be specific — frame rates, render times,
workload suitability — not generic statements.

**Price Disclaimer**
Remind the user that your prices are estimates and the dataset prices are historical.
Always verify on PCPartPicker or a retailer before purchasing."""
