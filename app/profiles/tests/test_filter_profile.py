import os
import re
from profiles import profiles
import pytest

KEYS = ["name", "driverFilters", "plotFilters"]
VALUES = ["test", ["test"], ["test"]]
PLOTS = ["gps.html", "speed.html", "Ax.html", "Ay.html", "Az.html", "Gx.html", "Gy.html", 
         "Gz.html", "Mx.html", "My.html", "Mz.html", "temp.html", "pressure.html"]
PLOT_FILTERS = ["ax.html", "ay.html", "az.html"]
FILTERED_PLOTS = ["ax", "ay", "az"]
DRIVERS = ["gps", "Altimeter", "THRUSter0", "BATMONIT", "Depthcell", "imu", "insidePressure"]
DRIVER_FILTERS = ["gps", "altimeter", "thruster0", "batmonit", "insidepressure"]

def clean_files():
    if os.path.exists("profiles.json"):
        os.remove("profiles.json")


def format_plots(plots):
    return [plot.lower().replace(".html", "") for plot in plots]


def format_drivers(drivers):
    return [driver.lower() for driver in drivers]


def format_filtered_files(files):
    output = []
    for file in files:
        file = file.lower()
        if (file.endswith(".html")):
            output.append(file.replace(".html", ""))
        else:
            output.append(file)

    return output

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


def test_filter_drivers():
    filtered_files = profiles.__filter_drivers(DRIVERS, DRIVER_FILTERS)
    filtered_files = [file.lower() for file in filtered_files]

    assert filtered_files == DRIVER_FILTERS


def test_filter_plots():
    filtered_files = profiles.__filter_plots(PLOTS, PLOT_FILTERS)
    filtered_files = [file.lower().replace(".html", "") for file in filtered_files]

    assert filtered_files == FILTERED_PLOTS


def test_filter():
    profile = {KEYS[0]: VALUES[0], KEYS[1]: DRIVER_FILTERS, KEYS[2]: PLOT_FILTERS}

    files = PLOTS

    filtered_files = profiles.filter(files, profile, filterPlots=True)
    filtered_files = format_plots(filtered_files)

    assert filtered_files == FILTERED_PLOTS

    files = DRIVERS

    filtered_files = profiles.filter(files, profile, filterDrivers=True)
    filtered_files = format_drivers(filtered_files)

    assert filtered_files == DRIVER_FILTERS

    files = PLOTS + DRIVERS

    filtered_files = profiles.filter(files, profile, True, True)
    filtered_files = format_filtered_files(filtered_files)

    assert filtered_files == DRIVER_FILTERS

