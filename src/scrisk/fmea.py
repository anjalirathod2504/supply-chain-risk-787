"""Failure Mode and Effects Analysis: Risk Priority Number = Severity x Occurrence x Detection."""
from __future__ import annotations

import pandas as pd


def rpn(fmea: pd.DataFrame, action_threshold: int = 150) -> pd.DataFrame:
    for col in ("severity", "occurrence", "detection"):
        if not fmea[col].between(1, 10).all():
            raise ValueError(f"{col} must be scored 1-10")
    d = fmea.copy()
    d["rpn"] = d["severity"] * d["occurrence"] * d["detection"]
    # Severity >= 9 always needs an action regardless of RPN (standard AIAG guidance).
    d["action_required"] = (d["rpn"] >= action_threshold) | (d["severity"] >= 9)
    return d.sort_values("rpn", ascending=False).reset_index(drop=True)
