# tests/test_helpers.py
import pytest
from pc_advisor.compatibility import _ddr_gen_from_speed, _ddr_gen_from_str, _norm, _num, CompatibilityChecker
from pc_advisor.models import ERROR, WARNING, INFO
from tests import conftest
        
# Helpers

def run(searches):
    return CompatibilityChecker(searches).run_all()

def severities(issues):
    return [i.severity for i in issues]

# DDR tests

class TestDdrGenFromSpeed:

    # Testing each of these cases
    @pytest.mark.parametrize("speed, expected", [
        ([4, 3200], 4),
        ([5, 4800], 5),
        ([3, 1600], 3),
        ([5], 5),   # single-element list still works
    ])
    def test_list_format(self, speed, expected):
        assert _ddr_gen_from_speed(speed) == expected

    @pytest.mark.parametrize("text, expected", [
        ("DDR4-3200", 4),
        ("DDR5", 5),
        ("ddr3", 3),
    ])
    def test_string_fallback(self, text, expected):
        assert _ddr_gen_from_speed(text) == expected

    @pytest.mark.parametrize("bad_input", [None, [], "unknown", "no info"])
    def test_returns_none_for_garbage(self, bad_input):
        assert _ddr_gen_from_speed(bad_input) is None

class TestNum:
    # Parameterized tests for various inputs
    @pytest.mark.parametrize("value, expected", [
        ("125",  125.0),
        (125,    125.0),
        (3.14,   3.14),
        ("3.14", 3.14),
    ])
    def test_valid_conversions(self, value, expected):
        assert _num(value) == expected

    @pytest.mark.parametrize("bad", [None, "N/A", "unknown", ""])
    def test_invalid_returns_none(self, bad):
        assert _num(bad) is None

class TestDdrGenFromStr:

    @pytest.mark.parametrize("text, expected", [
        ("DDR4-3200", 4),
        ("DDR5 6000", 5),
        ("ddr3", 3),
        ("Corsair Vengeance DDR5 32GB", 5),  # embedded in longer name
        ("DDR4", 4),  # uppercase
    ])
    def test_various_formats(self, text, expected):
        assert _ddr_gen_from_str(text) == expected

    @pytest.mark.parametrize("text", ["no memory info", "", "SDRAM"])
    def test_no_match_returns_none(self, text):
        assert _ddr_gen_from_str(text) is None


class TestNorm:

    @pytest.mark.parametrize("raw, expected", [
        ("LGA 1700", "lga1700"),
        ("AM-5", "am5"),
        ("AM5", "am5"),
        ("Mini-ITX", "miniitx"),
        ("micro_atx", "microatx"),
    ])
    def test_normalisation(self, raw, expected):
        assert _norm(raw) == expected


# Socket 

class TestCpuMotherboardSocket:

    def test_matching_socket_is_info(self, cpu_lga1700, mb_lga1700_ddr5):
        issues = run([cpu_lga1700, mb_lga1700_ddr5])
        socket_issues = [i for i in issues if "CPU" in i.components and "socket" in i.message.lower()]
        assert any(i.severity == INFO for i in socket_issues)

    def test_mismatched_socket_is_error(self, cpu_lga1700, mb_am5_ddr5):
        issues = run([cpu_lga1700, mb_am5_ddr5])
        assert ERROR in severities(issues)

    def test_missing_cpu_does_not_error(self, mb_lga1700_ddr5):
        """Without a CPU we can't confirm — should warn/info, not hard error."""
        issues = run([mb_lga1700_ddr5])
        assert ERROR not in severities(issues)


# RAM Type 

class TestRamType:

    def test_ddr5_match_is_info(self, ram_ddr5, mb_lga1700_ddr5):
        issues = run([ram_ddr5, mb_lga1700_ddr5])
        ram_issues = [i for i in issues if "Memory (RAM)" in i.components]
        assert any(i.severity == INFO for i in ram_issues)

    def test_ddr4_on_ddr5_board_is_error(self, ram_ddr4, mb_lga1700_ddr5):
        issues = run([ram_ddr4, mb_lga1700_ddr5])
        assert ERROR in severities(issues)

    def test_unknown_ddr_does_not_error(self):
        """If DDR version can't be determined, we note it — never hard block."""
        searches = [
            conftest.make_search("Memory (RAM)", "Generic 16GB Kit"),
            conftest.make_search("Motherboard", "Generic Z790 Board"),
        ]
        issues = run(searches)
        ram_issues = [i for i in issues if "Memory (RAM)" in i.components]
        assert ERROR not in [i.severity for i in ram_issues]


# PSU Wattage

class TestPsuWattage:

    def test_sufficient_psu_is_info(self, cpu_lga1700, gpu_200w, psu_750w):
        # 125 + 200 + 75 overhead = 400W, ×1.2 = 480W needed — 750W is plenty
        issues = run([cpu_lga1700, gpu_200w, psu_750w])
        psu_issues = [i for i in issues if "Power Supply (PSU)" in i.components]
        assert any(i.severity == INFO for i in psu_issues)

    def test_undersized_psu_is_error(self, cpu_lga1700, gpu_200w, psu_300w):
        # 400W needed, only 300W available
        issues = run([cpu_lga1700, gpu_200w, psu_300w])
        assert ERROR in severities(issues)

    def test_tight_psu_is_warning(self, cpu_lga1700, gpu_200w):
        # 480W recommended, 450W PSU — over minimum but under headroom
        psu_450 = conftest.make_search("Power Supply (PSU)", "Mid PSU", wattage=450)
        issues = run([cpu_lga1700, gpu_200w, psu_450])
        assert WARNING in severities(issues)


# Form Factor

class TestCaseFormFactor:

    def test_atx_in_atx_is_ok(self, mb_lga1700_ddr5, case_atx):
        issues = run([mb_lga1700_ddr5, case_atx])
        ff_issues = [i for i in issues if "Case" in i.components]
        assert ERROR not in [i.severity for i in ff_issues]

    def test_atx_in_itx_case_is_error(self, mb_lga1700_ddr5, case_itx):
        issues = run([mb_lga1700_ddr5, case_itx])
        assert ERROR in severities(issues)