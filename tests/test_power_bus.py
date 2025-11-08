from data.loader import load_yaml

EXPECTED_BUSES = {"reactor_hv_bus", "aux_lv_bus"}

def test_bus_nodes_exist():
    cfg = load_yaml("configs/power/bus_layout_v0.yaml")
    buses = {b["id"] for b in cfg.get("system", {}).get("buses", [])}
    assert EXPECTED_BUSES.issubset(buses)

def test_has_reactor_generator():
    cfg = load_yaml("configs/power/bus_layout_v0.yaml")
    gens = {g["id"] for g in cfg.get("system", {}).get("generators", [])}
    assert "reactor_primary_bus" in gens

def test_converters_reference_valid_buses():
    cfg = load_yaml("configs/power/bus_layout_v0.yaml")
    bus_ids = {b["id"] for b in cfg.get("system", {}).get("buses", [])}
    for conv in cfg.get("system", {}).get("converters", []):
        assert conv["from"] in bus_ids
        assert conv["to"] in bus_ids
