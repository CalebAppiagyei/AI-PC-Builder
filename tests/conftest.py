# tests/conftest.py
import pytest
from pc_advisor.models import PartMatch, ComponentSearch


def make_part(name: str, **data) -> PartMatch:
    return PartMatch(name=name, price=100.0, data=data)


def make_search(category: str, name: str, preference: str = "", **data) -> ComponentSearch:
    return ComponentSearch(
        category=category,
        user_preference=preference,
        matches=[make_part(name, **data)]
    )


# --- Fixtures: reusable fake parts ---

@pytest.fixture
def cpu_lga1700():
    return make_search("CPU", "Intel i5-13600K", socket="LGA1700", tdp=125)

@pytest.fixture
def cpu_am5():
    return make_search("CPU", "Ryzen 5 7600X", socket="AM5", tdp=105)

@pytest.fixture
def mb_lga1700_ddr5():
    return make_search("Motherboard", "ASUS Z790 DDR5", socket="LGA1700",
                       form_factor="ATX", memory_slots=4)

@pytest.fixture
def mb_am5_ddr5():
    return make_search("Motherboard", "MSI B650 DDR5", socket="AM5",
                       form_factor="ATX", memory_slots=4)

@pytest.fixture
def ram_ddr5():
    return make_search("Memory (RAM)", "Corsair DDR5-5600", speed=[5, 5600])

@pytest.fixture
def ram_ddr4():
    return make_search("Memory (RAM)", "Corsair Vengeance DDR4-3200", speed=[4, 3200])

@pytest.fixture
def gpu_200w():
    return make_search("Video Card (GPU)", "RTX 4070", tdp=200)

@pytest.fixture
def psu_750w():
    return make_search("Power Supply (PSU)", "EVGA 750W", wattage=750)

@pytest.fixture
def psu_300w():
    return make_search("Power Supply (PSU)", "Cheap PSU", wattage=300)

@pytest.fixture
def case_atx():
    return make_search("Case", "Fractal ATX Tower", type="ATX")

@pytest.fixture
def case_itx():
    return make_search("Case", "NCase M1", type="Mini-ITX")