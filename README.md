# ATTICUS — Automated Trial and Legal Intelligence for Criminal Defense Use Cases and Support

**An Open-Source Model Trained for Public Defenders**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Version](https://img.shields.io/badge/version-v0.1.0--dev-orange)](CHANGELOG.md)

> *"You never really understand a person until you consider things from his point of view...
> until you climb into his skin and walk around in it."*
> — Atticus Finch, *To Kill a Mockingbird*

```
python3 assets/banner.py
```

---

## Overview

ATTICUS is an open-source machine learning model fine-tuned to assist public defenders
and defense attorneys. Given a case file, charge sheet, or fact pattern, ATTICUS identifies
defense strategies, constitutional violations, evidentiary weaknesses, and mitigating factors.

ATTICUS is the companion model to [SELMA](https://codeberg.org/Ronin48/SELMA) — where SELMA
identifies what the prosecution can charge, ATTICUS builds the defense.

## Architecture

- **Base Model:** [Meta Llama 3.1 70B Instruct](https://huggingface.co/meta-llama/Llama-3.1-70B-Instruct) (Llama 3.1 Community License)
- **Fine-tuning Method:** QLoRA (4-bit quantization with Low-Rank Adaptation)
- **Context Window:** 128K tokens (native)
- **Origin:** Meta Platforms, Inc. (United States)

## Capabilities

Given a charge sheet or incident description, ATTICUS can:

1. **Defense Strategy** — Identify viable defense theories (alibi, self-defense, lack of intent, entrapment, etc.)
2. **Constitutional Analysis** — Flag 4th, 5th, 6th, and 14th Amendment violations (unlawful search, Miranda, right to counsel, due process)
3. **Evidentiary Weaknesses** — Identify gaps in the prosecution's evidence and element failures
4. **Brady Material** — Flag potential Brady/Giglio obligations (exculpatory evidence the prosecution must disclose)
5. **Sentencing Mitigation** — Identify mitigating factors, diversion eligibility, and sentencing alternatives
6. **Lesser Included Offenses** — Identify charges the jury could convict on instead of the primary charge
7. **Cross-Reference** — Flag related case law, precedents, and jurisdictional defenses

## Constitutional Override

The U.S. Constitution is the supreme law of the land. ATTICUS hard-overrides all federal,
state, and local law with constitutional protections. Any charge that conflicts with a
defendant's constitutional rights is flagged:

> ⚠ **CONSTITUTIONAL CONCERN** — this charge or evidence may not survive challenge under [Amendment].

## Jurisdictions

ATTICUS mirrors SELMA's multi-state architecture:

- **Federal:** U.S. Code + Federal Rules of Criminal Procedure (baseline for all models)
- **50 State Models:** Each state's criminal code + federal law + state constitution
- **Priority states:** Georgia, California, Texas, New York, Florida

## Project Structure

```
ATTICUS/
├── LICENSE
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── assets/
│   └── banner.py
├── models/
│   ├── federal/
│   ├── georgia/
│   └── [48 more states]/
├── configs/
│   ├── training_config.yaml
│   └── model_config.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   └── synthetic/
├── scripts/
│   ├── data_collection/
│   ├── training/
│   └── evaluation/
├── src/atticus/
├── tests/
└── docs/
    ├── TRAINING.md
    ├── DATA_SOURCES.md
    └── USAGE.md
```

## Disclaimer

ATTICUS is a research tool designed to assist defense attorneys and public defenders.
It is **NOT** a substitute for legal counsel or professional judgment. All outputs should
be verified by a licensed attorney before any action is taken.

This software is provided "AS IS" without warranty of any kind.

## Relationship to SELMA

| | SELMA | ATTICUS |
|---|---|---|
| **Purpose** | Prosecution-side statute identification | Defense-side strategy and analysis |
| **Users** | Law enforcement | Public defenders, defense attorneys |
| **Output** | Applicable charges and elements | Defense theories, constitutional violations, weaknesses |
| **Training data** | Criminal statutes, charging documents | Case law, suppression motions, acquittals, Brady material |

## License

**Project Code, Data, and Documentation:** Apache License 2.0 — Copyright 2026 Ronin 48, LLC.

**Base Model Weights:** Meta Llama 3.1 Community License.
