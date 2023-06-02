import os
import re
from profiles import profiles
import pytest

KEYS = ["name", "driverFilters", "plotFilters"]
VALUES = ["test", ["test"], ["test"]]

def clean_files():
    if os.path.exists("profiles.json"):
        os.remove("profiles.json")


def test_filter_drivers_invalid_input_type():
    with pytest.raises(TypeError) as e:
        profiles.__filter_drivers(1, [])

    assert "Files must be a list or tuple" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.__filter_drivers(None, [])

    assert "Files must be a list or tuple" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.__filter_drivers([], 1)
    
    assert "Driver filters must be a list or tuple" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.__filter_drivers([1], [])

    assert "Files must be a list or tuple of strings" in str(e.value)


def test_filter_drivers_invalid_input_value():
    with pytest.raises(ValueError) as e:
        profiles.__filter_drivers([""], [])

    assert "Files can't contain empty strings" in str(e.value)


def test_filter_plots_invalid_input_type():
    with pytest.raises(TypeError) as e:
        profiles.__filter_plots(1, [])

    assert "Files must be a list or tuple" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.__filter_plots(None, [])

    assert "Files must be a list or tuple" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.__filter_plots([], 1)

    assert "Plot filters must be a list or tuple" in str(e.value)
