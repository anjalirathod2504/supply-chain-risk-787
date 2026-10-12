"""Time-to-Recover (TTR) vs Time-to-Survive (TTS) risk exposure index.

TTR = weeks for a supplier to restore full output after a disruption.
TTS = weeks the downstream line can keep producing using buffer stock / alternates.
If TTR > TTS the line stops; the gap (in weeks) times the value flowing through
that node per week is the exposure. This follows the TTR/TTS framing popularised
by Simchi-Levi et al. (Harvard Business Review, 2014).
"""
from __future__ import annotations

import pandas as pd


def exposure_index(suppliers: pd.DataFrame, rate_per_month: float = 5.0) -> pd.DataFrame:
    """Return suppliers ranked by exposure.

    rate_per_month: aircraft produced per month (drives value at risk per week).
    """
    d = suppliers.copy()
    weekly_units = rate_per_month * 12 / 52
    d["gap_wks"] = (d["ttr_wks"] - d["tts_wks"]).clip(lower=0)
    d["units_lost"] = (d["gap_wks"] * weekly_units).round(1)
    # Value at risk uses the whole aircraft, not just the part: a missing wing stops a whole airplane.
    d["single_source_multiplier"] = 1 + 0.5 * d["single_source"]
    d["exposure_score"] = (d["gap_wks"] * d["single_source_multiplier"]).round(1)
    total = d["exposure_score"].sum()
    d["share_of_exposure"] = (d["exposure_score"] / total).round(3) if total else 0.0
    cols = ["package", "supplier", "country", "ttr_wks", "tts_wks", "gap_wks", "single_source",
            "units_lost", "exposure_score", "share_of_exposure"]
    return d[cols].sort_values("exposure_score", ascending=False).reset_index(drop=True)


def buffer_needed(suppliers: pd.DataFrame) -> pd.DataFrame:
    """Extra weeks of buffer (or alternate source) needed per package to close the gap."""
    d = suppliers[["package", "ttr_wks", "tts_wks"]].copy()
    d["extra_buffer_wks"] = (d["ttr_wks"] - d["tts_wks"]).clip(lower=0)
    return d[d["extra_buffer_wks"] > 0].sort_values("extra_buffer_wks", ascending=False).reset_index(drop=True)
