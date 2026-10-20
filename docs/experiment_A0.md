# Experiment A0 — preregistration draft

**Research question:** Can behavioral features distinguish simulated malicious automation from benign API sessions under a controlled synthetic generator?

**Not tested:** Whether traffic was produced by an LLM; real-world attribution to AI; deployment suitability.

**Independent variable:** Session scenario (legitimate, scripted_probe, adaptive_probe). **Dependent variables:** precision, recall, F1, false-positive rate, and (ML) PR-AUC. **Controlled:** generator seed, sample size, feature set, split rule, model hyperparameters.

**Protocol:** Generate 180 sessions per group with seed 42; hold out every fifth session in each group; evaluate fixed rule thresholds on test set. For ML, fit only on training sessions. Report confusion matrix and all metrics. Avoid tuning against test results. Use multiple unseen seeds in a future exploratory replication, then reserve an untouched confirmatory set.

**Potential leakage:** The scenario is built into feature-generation distributions. Do not include `scenario`, `session`, `split`, `automation_type`, or `label_malicious` in model inputs. Even without direct label leakage, artifacts of generation can inflate performance.

**Ethics:** Only simulated data; no live attack generation, credential testing, or external targeting. Protect personal information if real telemetry is later added.

**Go/no-go:** Proceed to real-data feasibility only after documenting baseline results and obtaining permission and provenance for external datasets.
