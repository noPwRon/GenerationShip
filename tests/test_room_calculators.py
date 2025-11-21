import pytest

from env.rooms.child_dorm_8 import ChildDorm8
from env.rooms.hygiene_block import HygieneBlock


def test_child_dorm_compute_builds_geometry_and_hvac():
    spec = ChildDorm8.defaults()

    report = ChildDorm8.compute(spec)

    assert report.type_id == ChildDorm8.TYPE_ID
    assert report.geometry["floor_area_m2"] == pytest.approx(spec.floor_area_m2)
    assert report.geometry["volume_m3"] == pytest.approx(
        spec.floor_area_m2 * spec.height_m
    )
    assert report.hvac["ventilation_Lps"] == pytest.approx(27.2)
    assert report.hvac["sensible_load_kW"] == pytest.approx(0.64)
    assert report.hvac["latent_load_kW"] == pytest.approx(0.28)
    assert report.metadata["phase"] == spec.phase


def test_hygiene_block_includes_exhaust_and_ventilation():
    spec = HygieneBlock.defaults()

    report = HygieneBlock.compute(spec)

    assert report.type_id == HygieneBlock.TYPE_ID
    assert report.hvac["ventilation_Lps"] == pytest.approx(101.4)
    assert report.hvac["exhaust_Lps"] == pytest.approx(68.4)
    assert report.geometry["volume_m3"] == pytest.approx(
        spec.floor_area_m2 * spec.height_m
    )
