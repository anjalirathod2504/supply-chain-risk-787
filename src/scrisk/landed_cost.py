"""Monte Carlo landed-cost model under tariff scenarios.

Landed cost per aircraft = sum over packages of
    unit_cost * (1 + freight_pct) * (1 + tariff_rate if tariff_exposed)
  + schedule penalty when sampled lead time exceeds the planned lead time.

Unit cost and freight are perturbed with a triangular distribution (±8% / ±25%),
lead times with a normal distribution, to reflect uncertainty in the inputs.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

SCENARIOS = {
    "Baseline (0%)": 0.00,
    "Moderate tariff (10%)": 0.10,
    "High tariff (25%)": 0.25,
}


@dataclass
class Settings:
    n_sims: int = 10_000
    late_penalty_musd_per_wk: float = 0.05   # carrying cost / disruption per week late, per package
    seed: int = 2026


def simulate(suppliers: pd.DataFrame, tariff: float, s: Settings | None = None) -> np.ndarray:
    s = s or Settings()
    rng = np.random.default_rng(s.seed)
    n = len(suppliers)
    cost = suppliers["unit_cost_musd"].to_numpy()
    freight = suppliers["freight_pct"].to_numpy()
    exposed = suppliers["tariff_exposed"].to_numpy()
    lt_mean = suppliers["lead_time_wks"].to_numpy()
    lt_sd = suppliers["lead_time_sd_wks"].to_numpy()

    cost_s = cost * rng.triangular(0.92, 1.0, 1.08, size=(s.n_sims, n))
    freight_s = freight * rng.triangular(0.75, 1.0, 1.25, size=(s.n_sims, n))
    lt_s = rng.normal(lt_mean, lt_sd, size=(s.n_sims, n))
    late_wks = np.clip(lt_s - lt_mean, 0, None)

    landed = cost_s * (1 + freight_s) * (1 + tariff * exposed)
    penalty = late_wks * s.late_penalty_musd_per_wk
    return (landed + penalty).sum(axis=1)


def run_scenarios(suppliers: pd.DataFrame, s: Settings | None = None) -> pd.DataFrame:
    rows = []
    for name, rate in SCENARIOS.items():
        sims = simulate(suppliers, rate, s)
        rows.append({
            "scenario": name, "tariff_rate": rate,
            "mean_musd": round(sims.mean(), 2),
            "p50_musd": round(np.percentile(sims, 50), 2),
            "p90_musd": round(np.percentile(sims, 90), 2),
            "p95_musd": round(np.percentile(sims, 95), 2),
        })
    out = pd.DataFrame(rows)
    out["delta_vs_baseline_musd"] = (out["mean_musd"] - out.loc[0, "mean_musd"]).round(2)
    return out


def tariff_sensitivity(suppliers: pd.DataFrame) -> pd.DataFrame:
    """Which packages drive the tariff cost increase (deterministic, at 25%)."""
    d = suppliers.copy()
    d["tariff_cost_at_25pct"] = (d["unit_cost_musd"] * (1 + d["freight_pct"]) * 0.25 * d["tariff_exposed"]).round(2)
    return d[["package", "country", "tariff_cost_at_25pct"]].sort_values(
        "tariff_cost_at_25pct", ascending=False).reset_index(drop=True)
