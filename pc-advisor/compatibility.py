import re
from typing import Any, Optional
from .models import ComponentSearch, CompatibilityIssue, ERROR, WARNING, INFO, PartMatch

# ---------------------------------------------------------------------------
# Compatibility checker
# ---------------------------------------------------------------------------

def _ddr_gen_from_speed(speed_field: Any) -> Optional[int]:
    """
    Extract DDR generation from the dataset speed field.
    The pc-part-dataset stores memory speed as [ddr_version, mhz], e.g. [4, 3200].
    Also handles plain strings like "DDR4-3200" or "DDR5".
    """
    if isinstance(speed_field, (list, tuple)) and len(speed_field) >= 1:
        try:
            return int(speed_field[0])
        except (TypeError, ValueError):
            pass
    # Fallback: parse "DDR4", "DDR5", "DDR3-1600", etc. from a string
    m = re.search(r"ddr\s*(\d)", str(speed_field).lower())
    return int(m.group(1)) if m else None

def _ddr_gen_from_str(text: str) -> Optional[int]:
    """Extract DDR generation from a freeform string (names, user preferences)."""
    m = re.search(r"ddr\s*(\d)", str(text).lower())
    return int(m.group(1)) if m else None

def _norm(s: str) -> str:
    return re.sub(r"[\s\-_]", "", str(s).lower())

def _num(v: Any) -> Optional[float]:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


class CompatibilityChecker:
    """
    Rule-based, offline compatibility checker.
    Uses spec fields from the pc-part-dataset records.
    """

    _PSU_OVERHEAD = 1.20    # 20 % headroom above component draw
    _PLATFORM_W   = 75      # baseline watts for MB + RAM + storage + fans

    def __init__(self, searches: list[ComponentSearch]):
        self._searches = searches   # kept for preference string fallback in checks
        self._best: dict[str, Optional[PartMatch]] = {
            cs.category: (cs.matches[0] if cs.matches else None)
            for cs in searches
        }
        self.issues: list[CompatibilityIssue] = []

    def run_all(self) -> list[CompatibilityIssue]:
        self.issues = []
        self._cpu_mb_socket()
        self._cpu_mb_chipset()
        self._ram_type()
        self._ram_slots()
        self._case_form_factor()
        self._psu_wattage()
        self._cooler_socket()
        self._cooler_tdp()
        self._storage_m2()
        return self.issues

    # -- helpers --------------------------------------------------------------

    def _f(self, cat: str, *keys: str) -> Optional[Any]:
        p = self._best.get(cat)
        if not p:
            return None
        for k in keys:
            v = p.data.get(k)
            if v is not None and v != "":
                return v
        return None

    def _add(self, sev: str, comps: list[str], msg: str) -> None:
        self.issues.append(CompatibilityIssue(sev, comps, msg))

    # -- checks ---------------------------------------------------------------

    def _cpu_mb_socket(self) -> None:
        cpu_s = self._f("CPU", "socket")
        mb_s  = self._f("Motherboard", "socket")
        if not cpu_s or not mb_s:
            if cpu_s or mb_s:
                self._add(INFO, ["CPU", "Motherboard"],
                          "Could not verify socket — one part is missing socket data. Check manually.")
            return
        cpu_n  = _norm(str(cpu_s))
        mb_set = {_norm(s) for s in re.split(r"[,/\s]+", _norm(str(mb_s))) if s}
        if cpu_n in mb_set or _norm(str(mb_s)) in cpu_n:
            self._add(INFO, ["CPU", "Motherboard"],
                      f"Socket OK — CPU ({cpu_s}) matches Motherboard ({mb_s}).")
        else:
            self._add(ERROR, ["CPU", "Motherboard"],
                      f"Socket MISMATCH — CPU is {cpu_s}, Motherboard is {mb_s}. Incompatible.")

    def _cpu_mb_chipset(self) -> None:
        cpu_p = self._best.get("CPU")
        mb_p  = self._best.get("Motherboard")
        if not cpu_p or not mb_p:
            return
        cn, mn = cpu_p.name.lower(), mb_p.name.lower()
        if re.search(r"i[3-9]-\d{4,5}k\b", cn) and not re.search(r"\bz\d{3}\b", mn):
            self._add(WARNING, ["CPU", "Motherboard"],
                      "Intel K-series CPU with non-Z chipset: overclocking unavailable.")
        if re.search(r"ryzen\s+\d\s+\d{3,4}x\b", cn) and re.search(r"\ba[35]20\b", mn):
            self._add(WARNING, ["CPU", "Motherboard"],
                      "AMD Ryzen X-series CPU on A320/A520: overclocking not supported.")

    def _ram_type(self) -> None:
        """
        Check DDR generation compatibility between RAM and Motherboard.

        Dataset field layout (from API.md):
          memory.speed  = [ddr_version, speed_mhz]  e.g. [4, 3200] for DDR4-3200
          motherboard   = no explicit ddr_type field; infer from name or memory_slots label

        We also check the user's raw preference string so that typing "DDR3" is
        caught even if a stray match was found in the dataset.
        """
        ram_cs = next((cs for cs in self._searches if cs.category == "Memory (RAM)"), None)
        mb_cs  = next((cs for cs in self._searches if cs.category == "Motherboard"),  None)
        ram_p  = self._best.get("Memory (RAM)")
        mb_p   = self._best.get("Motherboard")

        # --- Determine RAM DDR generation ---
        # Priority: dataset speed field (most reliable) > name > user preference string
        ram_ddr: Optional[int] = None
        if ram_p:
            ram_ddr = (_ddr_gen_from_speed(ram_p.data.get("speed"))
                       or _ddr_gen_from_str(ram_p.name))
        # If no match found in dataset, fall back to what the user typed
        if ram_ddr is None and ram_cs and ram_cs.user_preference:
            ram_ddr = _ddr_gen_from_str(ram_cs.user_preference)

        # --- Determine Motherboard DDR support ---
        # The dataset motherboard records don't have an explicit ddr_type field,
        # so we infer from the board name (e.g. "DDR5" often appears in the name).
        mb_ddr: Optional[int] = None
        if mb_p:
            mb_ddr = (_ddr_gen_from_str(mb_p.name)
                      or _ddr_gen_from_str(str(mb_p.data.get("memory_type", ""))))
        if mb_ddr is None and mb_cs and mb_cs.user_preference:
            mb_ddr = _ddr_gen_from_str(mb_cs.user_preference)

        # --- Compare ---
        if ram_ddr and mb_ddr:
            if ram_ddr == mb_ddr:
                self._add(INFO, ["Memory (RAM)", "Motherboard"],
                          f"RAM type OK — both are DDR{ram_ddr}.")
            else:
                self._add(ERROR, ["Memory (RAM)", "Motherboard"],
                          f"RAM type MISMATCH — selected RAM is DDR{ram_ddr} "
                          f"but Motherboard supports DDR{mb_ddr}. "
                          f"DDR{ram_ddr} modules are physically incompatible with a "
                          f"DDR{mb_ddr} motherboard and will not fit or function.")
        elif ram_ddr and not mb_ddr:
            self._add(WARNING, ["Memory (RAM)", "Motherboard"],
                      f"RAM is DDR{ram_ddr} — could not confirm motherboard DDR support. "
                      f"Verify the board explicitly supports DDR{ram_ddr} before purchasing.")
        elif mb_ddr and not ram_ddr:
            self._add(WARNING, ["Memory (RAM)", "Motherboard"],
                      f"Motherboard supports DDR{mb_ddr} — could not confirm RAM DDR generation. "
                      f"Ensure your RAM kit is DDR{mb_ddr}.")
        else:
            self._add(INFO, ["Memory (RAM)", "Motherboard"],
                      "Could not determine DDR generation for either part — "
                      "verify DDR4 vs DDR5 compatibility manually.")

    def _ram_slots(self) -> None:
        mods  = _num(self._f("Memory (RAM)", "modules", "module_count"))
        slots = _num(self._f("Motherboard", "memory_slots"))
        if mods and slots:
            if mods > slots:
                self._add(ERROR, ["Memory (RAM)", "Motherboard"],
                          f"RAM has {int(mods)} sticks but board has only {int(slots)} DIMM slots.")
            else:
                self._add(INFO, ["Memory (RAM)", "Motherboard"],
                          f"DIMM slots OK — {int(mods)}-stick kit fits in {int(slots)}-slot board.")

    def _case_form_factor(self) -> None:
        mb_ff   = self._f("Motherboard", "form_factor")
        case_ff = self._f("Case", "type")
        if not mb_ff or not case_ff:
            self._add(INFO, ["Motherboard", "Case"],
                      "Could not verify form factor — check ATX/mATX/ITX fit manually.")
            return
        SIZE = {"miniitx": 1, "microatx": 2, "matx": 2, "atx": 3, "eatx": 4}
        mb_r   = next((v for k, v in SIZE.items() if k in _norm(str(mb_ff))), None)
        case_r = max((v for k, v in SIZE.items() if k in _norm(str(case_ff))), default=None)
        if mb_r and case_r:
            if mb_r > case_r:
                self._add(ERROR, ["Motherboard", "Case"],
                          f"Motherboard ({mb_ff}) too large for Case ({case_ff}).")
            else:
                self._add(INFO, ["Motherboard", "Case"],
                          f"Form factor OK — {mb_ff} fits in {case_ff} case.")

    def _psu_wattage(self) -> None:
        psu_w   = _num(self._f("Power Supply (PSU)", "wattage"))
        cpu_tdp = _num(self._f("CPU", "tdp"))
        gpu_tdp = _num(self._f("Video Card (GPU)", "tdp"))
        if not psu_w:
            self._add(INFO, ["Power Supply (PSU)"],
                      "PSU wattage not in dataset — verify manually.")
            return
        draw = (cpu_tdp or 0) + (gpu_tdp or 0)
        if not draw:
            self._add(INFO, ["Power Supply (PSU)"],
                      f"PSU is {int(psu_w)}W — no TDP data to verify against.")
            return
        total = draw + self._PLATFORM_W
        rec   = int(total * self._PSU_OVERHEAD)
        parts = []
        if cpu_tdp: parts.append(f"CPU ~{int(cpu_tdp)}W")
        if gpu_tdp: parts.append(f"GPU ~{int(gpu_tdp)}W")
        parts.append(f"overhead ~{self._PLATFORM_W}W")
        summary = " + ".join(parts) + f" = ~{int(total)}W"
        if psu_w < total:
            self._add(ERROR, ["CPU", "Video Card (GPU)", "Power Supply (PSU)"],
                      f"PSU UNDERSIZED. Draw: {summary}. PSU: {int(psu_w)}W. Need >= {rec}W.")
        elif psu_w < rec:
            self._add(WARNING, ["CPU", "Video Card (GPU)", "Power Supply (PSU)"],
                      f"PSU tight. Draw: {summary}. PSU: {int(psu_w)}W. Recommend {rec}W.")
        else:
            self._add(INFO, ["CPU", "Video Card (GPU)", "Power Supply (PSU)"],
                      f"PSU OK — {int(psu_w)}W covers ~{int(total)}W draw.")

    def _cooler_socket(self) -> None:
        cpu_s    = self._f("CPU", "socket")
        cooler_s = self._f("CPU Cooler", "socket", "sockets", "socket_compatibility")
        if not cpu_s or not cooler_s:
            self._add(INFO, ["CPU", "CPU Cooler"],
                      "Could not verify cooler socket — check manually.")
            return
        if _norm(str(cpu_s)) in _norm(str(cooler_s)):
            self._add(INFO, ["CPU", "CPU Cooler"], f"Cooler socket OK — supports {cpu_s}.")
        else:
            self._add(WARNING, ["CPU", "CPU Cooler"],
                      f"Cooler may not support {cpu_s}. Listed: {cooler_s}. Verify first.")

    def _cooler_tdp(self) -> None:
        cpu_tdp    = _num(self._f("CPU", "tdp"))
        cooler_tdp = _num(self._f("CPU Cooler", "tdp", "max_tdp", "cooling_capacity"))
        if not cpu_tdp or not cooler_tdp:
            return
        if cooler_tdp < cpu_tdp:
            self._add(WARNING, ["CPU", "CPU Cooler"],
                      f"Cooler rated {int(cooler_tdp)}W but CPU TDP is {int(cpu_tdp)}W. May struggle.")
        else:
            self._add(INFO, ["CPU", "CPU Cooler"],
                      f"Cooler TDP OK — {int(cooler_tdp)}W handles {int(cpu_tdp)}W CPU.")

    def _storage_m2(self) -> None:
        storage = self._best.get("Storage")
        if not storage:
            return
        iface = str(storage.data.get("interface", "")).lower()
        form  = str(storage.data.get("form_factor", "")).lower()
        if "m.2" not in form and "nvme" not in iface and "pcie" not in iface:
            return
        m2 = _num(self._f("Motherboard", "m2_slots", "m.2_slots"))
        if m2 is not None:
            if m2 == 0:
                self._add(ERROR, ["Storage", "Motherboard"],
                          "M.2/NVMe storage selected but Motherboard has 0 M.2 slots.")
            else:
                self._add(INFO, ["Storage", "Motherboard"],
                          f"M.2 OK — Motherboard has {int(m2)} M.2 slot(s).")
        else:
            self._add(INFO, ["Storage", "Motherboard"],
                      "M.2/NVMe storage selected — verify board has an available M.2 slot.")

# ---------------------------------------------------------------------------
# Compatibility report
# ---------------------------------------------------------------------------

def run_compatibility_check(searches: list[ComponentSearch]) -> list[CompatibilityIssue]:
    checker = CompatibilityChecker(searches)
    issues  = checker.run_all()

    print("\n" + "=" * 60)
    print("  COMPATIBILITY REPORT")
    print("=" * 60)

    if not issues:
        print("  No issues detected.")
        return issues

    icons = {ERROR: "ERROR", WARNING: "WARNING", INFO: "INFO"}
    for sev, label in [(ERROR, "ERRORS"), (WARNING, "WARNINGS"), (INFO, "NOTES")]:
        group = [i for i in issues if i.severity == sev]
        if not group:
            continue
        print(f"\n  -- {label} --")
        for issue in group:
            print(f"\n  [{issue.severity}] ({', '.join(issue.components)})")
            print(f"    {issue.message}")

    errors   = sum(1 for i in issues if i.severity == ERROR)
    warnings = sum(1 for i in issues if i.severity == WARNING)
    infos    = sum(1 for i in issues if i.severity == INFO)
    print(f"\n  Summary: {errors} error(s), {warnings} warning(s), {infos} note(s)")
    print("=" * 60)
    return issues
