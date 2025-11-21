import pytest

from env.hvac import calc_env


def test_ventilation_rate_combines_people_and_area():
    result = calc_env.ventilation_rate(
        occupants=4, Lps_per_person=5.0, area_m2=20.0, lps_per_m2=0.5
    )
    assert result == pytest.approx(4 * 5.0 + 20.0 * 0.5)


def test_exhaust_rate_zero_when_no_info():
    assert calc_env.exhaust_rate(area_m2=25.0, exhaust_info=None) == 0.0
    assert calc_env.exhaust_rate(area_m2=25.0, exhaust_info={}, fixtures=0) == 0.0


def test_exhaust_rate_prefers_max_of_area_and_fixture():
    exhaust_info = {"Ra_Lps_per_m2": 1.0, "per_fixture_Lps": 4.0}
    result = calc_env.exhaust_rate(area_m2=3.0, exhaust_info=exhaust_info, fixtures=2)
    # Area driver = 3.0 L/s, fixture driver = 8.0 L/s -> expect fixture to win
    assert result == pytest.approx(8.0)


def test_supply_rate_meets_or_exceeds_exhaust():
    assert calc_env.supply_rate(total_ventilation=10.0, required_exhaust=12.0) == 12.0
    assert calc_env.supply_rate(total_ventilation=14.0, required_exhaust=12.0) == 14.0


def test_validate_exhaust_keys_rejects_unknown_key():
    with pytest.raises(KeyError):
        calc_env.validate_exhaust_keys({"unknown_key": 1.0})


def test_load_scaling_helpers():
    assert calc_env.metabolic_heat_kW(occupants=5, sensible_W=120.0) == pytest.approx(
        0.6
    )
    assert calc_env.latent_heat_kW(occupants=5, latent_W=50.0) == pytest.approx(0.25)
    base, peak = calc_env.device_load_kW(occupants=6)
    assert base == pytest.approx(0.6)
    assert peak == pytest.approx(0.9)
    assert calc_env.latent_load_kgph(occupants=10) == pytest.approx(1.2)


def test_comfort_band_placeholders():
    assert calc_env.temp_band("any") == (20.0, 24.0)
    assert calc_env.rh_band("any") == (35.0, 60.0)
