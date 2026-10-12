"""Run the full analysis and write reports/analysis.md with charts.

    python -m scrisk.run_analysis
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from . import exposure, fmea, landed_cost

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    sup = pd.read_csv(ROOT / "data" / "suppliers.csv")
    fm = pd.read_csv(ROOT / "data" / "fmea.csv")
    out = ROOT / "reports"
    out.mkdir(exist_ok=True)

    exp = exposure.exposure_index(sup)
    rp = fmea.rpn(fm)
    scen = landed_cost.run_scenarios(sup)
    sens = landed_cost.tariff_sensitivity(sup)

    # Chart: TTR vs TTS
    d = sup.sort_values("ttr_wks")
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.barh(d["package"], d["ttr_wks"], color="#e76f51", label="Time to Recover")
    ax.barh(d["package"], d["tts_wks"], color="#2a9d8f", label="Time to Survive")
    ax.set_xlabel("Weeks"); ax.legend(frameon=False, fontsize=8)
    ax.tick_params(axis="y", labelsize=8); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(out / "ttr_tts.png", dpi=150); plt.close(fig)

    # Chart: landed cost distributions
    fig, ax = plt.subplots(figsize=(8, 3.6))
    for (name, rate), color in zip(landed_cost.SCENARIOS.items(), ["#2a9d8f", "#e9c46a", "#e76f51"]):
        ax.hist(landed_cost.simulate(sup, rate), bins=60, alpha=0.6, label=name, color=color)
    ax.set_xlabel("Landed cost of modelled packages per aircraft ($M)")
    ax.legend(frameon=False, fontsize=8); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(out / "landed_cost.png", dpi=150); plt.close(fig)

    md = [
        "# Boeing 787 Supply Chain — Risk & Tariff Scenario Analysis",
        "",
        "> Inputs in `data/` are **illustrative assumptions** for a course project, not Boeing data.",
        "",
        "## 1. TTR/TTS exposure index",
        "",
        exp.to_markdown(index=False),
        "",
        "![TTR vs TTS](ttr_tts.png)",
        "",
        "## 2. FMEA — risk priority numbers",
        "",
        rp[["package", "failure_mode", "severity", "occurrence", "detection", "rpn", "action_required"]]
            .to_markdown(index=False),
        "",
        "## 3. Monte Carlo landed cost under tariff scenarios",
        "",
        scen.to_markdown(index=False),
        "",
        "![Landed cost](landed_cost.png)",
        "",
        "### Tariff cost drivers at 25%",
        "",
        sens.head(6).to_markdown(index=False),
        "",
    ]
    (out / "analysis.md").write_text("\n".join(md), encoding="utf-8")
    print(f"Top exposure: {exp.iloc[0]['package']} | Highest RPN: {rp.iloc[0]['failure_mode']} "
          f"| +25% tariff adds ${scen.iloc[-1]['delta_vs_baseline_musd']}M per aircraft (mean)")


if __name__ == "__main__":
    main()
