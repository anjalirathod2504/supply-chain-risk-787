from pathlib import Path

import pandas as pd
import pytest

from scrisk import exposure, fmea, landed_cost

DATA = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture
def sup():
    return pd.read_csv(DATA / "suppliers.csv")


def test_gap_is_never_negative():
    df = pd.DataFrame([dict(package="A", supplier="s", country="c", ttr_wks=5, tts_wks=10, single_source=1),
                       dict(package="B", supplier="s", country="c", ttr_wks=12, tts_wks=4, single_source=0)])
    e = exposure.exposure_index(df).set_index("package")
    assert e.loc["A", "gap_wks"] == 0
    assert e.loc["B", "gap_wks"] == 8


def test_exposure_sorted(sup):
    assert exposure.exposure_index(sup)["exposure_score"].is_monotonic_decreasing


def test_rpn_math_and_validation():
    df = pd.DataFrame([dict(severity=9, occurrence=2, detection=2), dict(severity=5, occurrence=6, detection=6)])
    r = fmea.rpn(df)
    assert list(r["rpn"]) == [180, 36]
    assert r["action_required"].all()  # 180 >= 150, and severity 9 forces action
    with pytest.raises(ValueError):
        fmea.rpn(pd.DataFrame([dict(severity=11, occurrence=1, detection=1)]))


def test_tariff_raises_cost(sup):
    s = landed_cost.Settings(n_sims=2000)
    scen = landed_cost.run_scenarios(sup, s)
    assert scen["mean_musd"].is_monotonic_increasing
    assert scen.loc[0, "delta_vs_baseline_musd"] == 0
