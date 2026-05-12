# ATTICUS Changelog

## Versioning Scheme

Mirrors SELMA's versioning:

| Component | When to bump | Example |
|---|---|---|
| **Major** (X.0.0) | Base model swap | v1.0.0 |
| **Minor** (0.X.0) | New training data, new states, significant prompt changes | v0.2.0 |
| **Patch** (0.0.X) | Parameter tuning, bug fixes, small prompt adjustments | v0.1.1 |

---

## [v0.1.0-dev] — In Development (Started 2026-05-12)

**Status:** 🚧 Scaffolding in progress
**Base model:** `meta-llama/Llama-3.3-70B-Instruct` (planned)
**Type:** Prompt-engineered baseline (pre-fine-tune)

### Added
- Initial project structure mirroring SELMA architecture
- Defense-focused system prompt with constitutional override
- Covers 1st, 4th, 5th, 6th, 7th, 8th, 14th Amendment protections
- Brady/Giglio obligation flagging
- Sentencing mitigation analysis
