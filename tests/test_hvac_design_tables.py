import pytest

from env.hvac.calc_tables import get_rates, list_available_rooms
from env.hvac.design import get_hvac_design, resolve_room_activity, validate_exhaust_keys


def test_get_rates_merges_defaults_and_room_overrides():
    rates = get_rates("warehouse", activity="moderate_work")

    assert rates["ventilation"]["Rp_Lps_per_person"] == pytest.approx(0.03)
    assert rates["ventilation"]["Ra_Lps_per_m2"] == pytest.approx(0.3)
    assert rates["activity"]["sensible_W_per_person"] == pytest.approx(150.0)
    assert rates["activity"]["latent_W_per_person"] == pytest.approx(130.0)


def test_get_rates_includes_validated_exhaust_block():
    rates = get_rates("hygiene_block", activity="moderate_work")

    exhaust = rates["exhaust"]
    assert exhaust["Ra_Lps_per_m2"] == pytest.approx(3.8)
    assert exhaust["per_shower_Lps_continuous"] == pytest.approx(9.4)
    validate_exhaust_keys(exhaust)  # should not raise


def test_resolve_room_activity_uses_first_activity_when_unspecified():
    cfg = get_hvac_design()
    resolved = resolve_room_activity(cfg, room_type="mess_hall", activity=None)

    assert resolved["activity"]["sensible_W_per_person"] == pytest.approx(110.0)
    assert resolved["ventilation"]["Rp_Lps_per_person"] == pytest.approx(3.5)


def test_list_available_rooms_reports_activity_keys():
    summary = list_available_rooms()

    assert "hygiene_block" in summary
    assert "moderate_work" in summary["hygiene_block"]


def test_validate_exhaust_keys_rejects_unknown_key():
    with pytest.raises(KeyError):
        validate_exhaust_keys({"bad_key": 5.0})
