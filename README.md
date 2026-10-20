# AI Cyber Defense Framework — Laboratory A0

**Research status:** Synthetic pilot only; no real cyberattack detection claim.

This is the first executable deliverable for Experiment A (behavioral detection). All data is locally synthesized. No network requests, scanning, exploitation, or access to external systems.

## Requirements
- Python 3.10+; standard library for A0.
- Optional: `pip install -r requirements.txt` for the supervised ML baseline.

## Run
From the project root:
```bash
python src/lab.py --seed 42 --per-group 180
python -m unittest discover -s tests -v
# optional after installing dependencies:
python src/ml_baseline.py
```

Outputs: `data/synthetic_sessions.csv`, `results/baseline.json`, optional `results/ml_baseline.json`.

## Research design
- Three labeled scenarios: legitimate, conventional scripted automation, and *simulated* adaptive automation.
- Binary label: malicious versus legitimate. The `automation_type` field is **ground truth from synthetic generation only** and **is not a feature** in the detector.
- 80/20 train/test split by distinct session IDs. Do not tune rules using the test split; current thresholds are illustrative and must be fixed before confirmatory evaluation.
- Compare rule baseline to Random Forest. Later: external datasets, temporal splits, cross-environment tests, confidence intervals, false-positive rates, ablation and calibration.
- **Major confound:** synthetic generator determines feature distributions; strong scores on these samples do not establish real-world generalization or AI attribution.

## Next milestones
1. Define inclusion/exclusion criteria for literature review.
2. Identify datasets with reliable provenance and usage licenses (e.g. CIC-IDS2017 for generic intrusion detection; it does not label AI assistance).
3. Create a consented lab API telemetry collector with sensitive values removed.
4. Pre-register hypotheses, evaluation protocol and split policy before tuning.
5. Experiment B: separate local RAG/tool simulation, defensive policy enforcement and attack-success-rate measurement.

See `docs/experiment_A0.md` for the protocol.
