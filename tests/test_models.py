# tests/test_models.py
from pc_advisor.models import PartMatch, ComponentSearch, CompatibilityIssue, ERROR, WARNING, INFO


class TestPartMatch:

    def test_basic_creation(self):
        part = PartMatch(name="Intel i5-13600K", price=299.99, data={"socket": "LGA1700"})
        assert part.name == "Intel i5-13600K"
        assert part.price == 299.99
        assert part.data["socket"] == "LGA1700"

    def test_price_can_be_none(self):
        part = PartMatch(name="Some CPU", price=None, data={})
        assert part.price is None

    def test_data_accepts_arbitrary_keys(self):
        part = PartMatch(name="GPU", price=500.0, data={"tdp": 200, "vram": 12})
        assert part.data["vram"] == 12


class TestComponentSearch:

    def test_defaults(self):
        cs = ComponentSearch(category="CPU", user_preference="fast gaming CPU")
        assert cs.matches == []
        assert cs.error is None

    def test_each_instance_gets_own_matches_list(self):
        """
        default_factory=list means every instance gets a fresh list.
        Without it, all instances would share the same list. 
        Testing that each object has its own list.
        """
        cs1 = ComponentSearch(category="CPU", user_preference="any")
        cs2 = ComponentSearch(category="GPU", user_preference="any")
        cs1.matches.append("fake")
        assert cs2.matches == []  # cs2 should be unaffected

    def test_stores_matches_and_error(self):
        part = PartMatch(name="Ryzen 5 7600X", price=249.0, data={})
        cs = ComponentSearch(category="CPU", user_preference="AMD", matches=[part])
        assert len(cs.matches) == 1
        assert cs.matches[0].name == "Ryzen 5 7600X"

    def test_error_string_stored(self):
        cs = ComponentSearch(category="CPU", user_preference="x", error="No results found")
        assert cs.error == "No results found"


class TestCompatibilityIssue:

    def test_severity_levels(self):
        for sev in [ERROR, WARNING, INFO]:
            issue = CompatibilityIssue(severity=sev, components=["CPU"], message="test")
            assert issue.severity == sev

    def test_constants_are_strings(self):
        assert ERROR   == "ERROR"
        assert WARNING == "WARNING"
        assert INFO    == "INFO"

    def test_multiple_components(self):
        issue = CompatibilityIssue(
            severity=ERROR,
            components=["CPU", "GPU", "Power Supply (PSU)"],
            message="PSU undersized"
        )
        assert len(issue.components) == 3
        assert "GPU" in issue.components