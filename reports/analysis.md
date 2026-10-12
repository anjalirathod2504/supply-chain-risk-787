# Boeing 787 Supply Chain — Risk & Tariff Scenario Analysis

> Inputs in `data/` are **illustrative assumptions** for a course project, not Boeing data.

## 1. TTR/TTS exposure index

| package                             | supplier                    | country     |   ttr_wks |   tts_wks |   gap_wks |   single_source |   units_lost |   exposure_score |   share_of_exposure |
|:------------------------------------|:----------------------------|:------------|----------:|----------:|----------:|----------------:|-------------:|-----------------:|--------------------:|
| Landing gear                        | Safran Landing Systems      | France      |        44 |        10 |        34 |               1 |         39.2 |             51   |               0.162 |
| Wing                                | Mitsubishi Heavy Industries | Japan       |        40 |        12 |        28 |               1 |         32.3 |             42   |               0.134 |
| Forward fuselage (Sec 43)           | Kawasaki Heavy Industries   | Japan       |        36 |        10 |        26 |               1 |         30   |             39   |               0.124 |
| Engines (pair)                      | Rolls-Royce / GE Aerospace  | UK/USA      |        52 |        14 |        38 |               0 |         43.8 |             38   |               0.121 |
| Center fuselage & horiz. stabilizer | Leonardo                    | Italy       |        34 |         9 |        25 |               1 |         28.8 |             37.5 |               0.119 |
| Forward fuselage (Sec 41)           | Spirit AeroSystems          | USA         |        32 |         8 |        24 |               1 |         27.7 |             36   |               0.114 |
| Center wing box                     | Subaru                      | Japan       |        30 |        10 |        20 |               1 |         23.1 |             30   |               0.095 |
| Passenger doors                     | Latecoere                   | France      |        18 |         8 |        10 |               1 |         11.5 |             15   |               0.048 |
| Cargo doors                         | Saab                        | Sweden      |        16 |         8 |         8 |               1 |          9.2 |             12   |               0.038 |
| Aft fuselage                        | Boeing South Carolina       | USA         |        20 |        12 |         8 |               0 |          9.2 |              8   |               0.025 |
| Raked wingtips                      | Korean Air Aerospace        | South Korea |        14 |         8 |         6 |               0 |          6.9 |              6   |               0.019 |

![TTR vs TTS](ttr_tts.png)

## 2. FMEA — risk priority numbers

| package                             | failure_mode                      |   severity |   occurrence |   detection |   rpn | action_required   |
|:------------------------------------|:----------------------------------|-----------:|-------------:|------------:|------:|:------------------|
| Forward fuselage (Sec 41)           | Supplier quality escape           |          8 |            6 |           5 |   240 | True              |
| Wing                                | Composite layup defect found late |          9 |            4 |           6 |   216 | True              |
| Center fuselage & horiz. stabilizer | Shimming non-conformance          |          7 |            5 |           5 |   175 | True              |
| Engines (pair)                      | Engine delivery late              |          9 |            6 |           3 |   162 | True              |
| Landing gear                        | Forging capacity shortfall        |          8 |            5 |           4 |   160 | True              |
| Wing                                | Ocean shipment delay              |          8 |            4 |           3 |    96 | False             |
| Aft fuselage                        | Internal capacity conflict        |          6 |            4 |           4 |    96 | False             |
| Passenger doors                     | Seal part non-conformance         |          5 |            4 |           4 |    80 | False             |
| Center wing box                     | Tariff increase on imports        |          6 |            5 |           2 |    60 | False             |
| Raked wingtips                      | Single shipment damaged           |          4 |            3 |           3 |    36 | False             |

## 3. Monte Carlo landed cost under tariff scenarios

| scenario              |   tariff_rate |   mean_musd |   p50_musd |   p90_musd |   p95_musd |   delta_vs_baseline_musd |
|:----------------------|--------------:|------------:|-----------:|-----------:|-----------:|-------------------------:|
| Baseline (0%)         |          0    |       69.44 |      69.45 |      70.93 |      71.32 |                     0    |
| Moderate tariff (10%) |          0.1  |       75.33 |      75.34 |      76.96 |      77.38 |                     5.89 |
| High tariff (25%)     |          0.25 |       84.18 |      84.18 |      86.01 |      86.49 |                    14.74 |

![Landed cost](landed_cost.png)

### Tariff cost drivers at 25%

| package                             | country   |   tariff_cost_at_25pct |
|:------------------------------------|:----------|-----------------------:|
| Engines (pair)                      | UK/USA    |                   7.61 |
| Wing                                | Japan     |                   2.45 |
| Center fuselage & horiz. stabilizer | Italy     |                   1.63 |
| Forward fuselage (Sec 43)           | Japan     |                   1.08 |
| Center wing box                     | Japan     |                   0.8  |
| Landing gear                        | France    |                   0.61 |
