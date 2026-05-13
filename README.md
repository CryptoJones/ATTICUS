# ATTICUS — Advocacy, Trial, Testimony, Innocence, Case, Unified Scout

**An Open-Source Model Trained for Public Defenders**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Ronin48%2Fatticus-yellow)](https://huggingface.co/Ronin48/atticus)
[![Version](https://img.shields.io/badge/version-v0.1.0--dev-orange)](CHANGELOG.md)

> *"You never really understand a person until you consider things from his point of view...
> until you climb into his skin and walk around in it."*
> — Atticus Finch, *To Kill a Mockingbird*

```
python3 assets/banner.py
```

---

## Supporters

ATTICUS is community-funded. Every contribution — great or small — keeps this project free,
open, and in the hands of the people it is meant to serve. Public defenders are chronically
under-resourced. ATTICUS exists to change that.

| Donor | Amount | Note |
|---|---|---|
| Ronin 48, LLC | N/A | Founding donor |
| Joe Sixpack (anonymous) | $200 | Founding donor |

*Want to support ATTICUS? Reach out to the maintainers.*

---

## Overview

ATTICUS is an open-source machine learning model fine-tuned to assist public defenders and
defense attorneys. Given a case file, charge sheet, or fact pattern, ATTICUS identifies
defense strategies, constitutional violations, evidentiary weaknesses, Brady/Giglio
obligations, and mitigating factors — all in plain language, all with cited authority.

The name is deliberate. Atticus Finch was not a man who won every case. He was a man who
believed that every defendant deserved someone in their corner who would look at the evidence
honestly, challenge the state's case rigorously, and treat the accused as a human being worthy
of a real defense. This model carries that obligation.

### Sister Project: SELMA

ATTICUS is one half of a balanced system.

[**SELMA**](https://codeberg.org/Ronin48/SELMA) — *Specified Encapsulated Limitless Memory Archive* —
is ATTICUS's companion model, built for law enforcement. Where SELMA identifies what the
prosecution can charge, ATTICUS builds the defense. Where SELMA maps evidence to statutes,
ATTICUS maps evidence to constitutional protections.

This symmetry is intentional. A system that only serves prosecution is a system that can cause
harm. ATTICUS ensures that every capability SELMA gives law enforcement has a counterpart in
the hands of the public defender.

| | SELMA | ATTICUS |
|---|---|---|
| **Purpose** | Prosecution-side statute identification | Defense-side strategy and analysis |
| **Users** | Patrol officers, detectives, special agents | Public defenders, defense attorneys |
| **Output** | Applicable charges and elements, legal reasoning | Defense theories, constitutional violations, evidentiary weaknesses |
| **Training data** | Criminal statutes, case law, charging documents | Suppression motions, acquittals, Brady/Giglio material, exoneration data |
| **Repository** | [Ronin48/SELMA](https://codeberg.org/Ronin48/SELMA) | [Ronin48/ATTICUS](https://codeberg.org/Ronin48/ATTICUS) |

---

## Architecture

- **Base Model:** [Meta Llama 3.3 70B Instruct](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct) (Llama 3.1 Community License)
- **Fine-tuning Method:** QLoRA (4-bit quantization with Low-Rank Adaptation)
- **Context Window:** 128K tokens (native)
- **Quantization:** NF4 double quantization via bitsandbytes
- **Origin:** Meta Platforms, Inc. (United States)

---

## Capabilities

Given a charge sheet or incident description, ATTICUS can:

1. **Defense Strategy** — Identify viable defense theories (alibi, self-defense, lack of intent,
   entrapment, duress, consent, mistake of fact, etc.) and explain what evidence supports each
2. **Constitutional Analysis** — Flag 4th, 5th, 6th, and 14th Amendment violations: unlawful
   search and seizure, Miranda failures, right to counsel violations, due process deprivations,
   and selective prosecution
3. **Evidentiary Weaknesses** — Identify gaps in the prosecution's evidence, element failures,
   chain-of-custody problems, and reliability issues with forensic methods or expert witnesses
4. **Brady/Giglio Material** — Flag categories of evidence the prosecution may be obligated to
   disclose, and the standard (*Strickler v. Greene*) for establishing materiality
5. **Sentencing Mitigation** — Identify mitigating factors under U.S.S.G., state equivalents,
   diversion eligibility, plea alternatives, and departures or variances
6. **Lesser Included Offenses** — Identify charges the jury could convict on instead of the
   primary charge, and how to request lesser included instructions
7. **Cross-Reference** — Flag relevant case law, circuit splits, jurisdictional quirks, and
   precedents that may not be obvious from the face of the charge
8. **Wrongful Conviction Patterns** — Flag fact patterns associated with documented wrongful
   convictions: eyewitness misidentification, false confessions, informant testimony, bad
   forensics, and Brady suppression

---

## Constitutional Override

The U.S. Constitution is the supreme law of the land. ATTICUS is trained to treat it that way.
No statute, agency policy, or local rule overrides the Bill of Rights. Where a charge,
a search, an interrogation, or a prosecution implicates a defendant's constitutional rights,
ATTICUS will say so plainly:

> ⚠ **CONSTITUTIONAL CONCERN** — this charge or evidence may not survive challenge under the
> [Amendment]. ATTICUS recommends filing a motion to suppress / dismiss before trial.

Constitutional protections covered:

- **First Amendment** — speech, association, and protected activity that cannot form the basis of a charge
- **Fourth Amendment** — unlawful searches and seizures; suppression under the exclusionary rule (*Mapp v. Ohio*)
- **Fifth Amendment** — self-incrimination, Miranda rights, double jeopardy, grand jury protections
- **Sixth Amendment** — right to counsel, speedy trial, confrontation clause, jury trial rights
- **Seventh Amendment** — right to jury trial in civil matters that touch criminal exposure
- **Eighth Amendment** — excessive bail, cruel and unusual punishment, disproportionate sentencing
- **Fourteenth Amendment** — due process, equal protection, and selective prosecution

---

## Jurisdictions

ATTICUS mirrors SELMA's multi-state architecture:

- **Federal:** U.S. Code + Federal Rules of Criminal Procedure (baseline for all models)
- **50 State Models:** Each state's criminal code + federal law + state constitution
- **Priority states:** Georgia, California, Texas, New York, Florida

---

## Where to Get ATTICUS

### HuggingFace

Adapter weights and merged model weights will be published at:

- **LoRA Adapter:** `Ronin48/atticus-lora-adapter` — fine-tuned adapter only (smaller download)
- **Merged Model:** `Ronin48/atticus-70b` — full merged weights, ready for inference
- **Quantized (GGUF):** `Ronin48/atticus-70b-GGUF` — for use with llama.cpp, LM Studio, and Ollama

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("Ronin48/atticus-70b")
```

### Ollama

Once GGUF weights are published, ATTICUS will be available on the Ollama registry:

```bash
ollama run Ronin48/atticus
```

### LM Studio

Once GGUF weights are published to HuggingFace, ATTICUS will be searchable and
downloadable directly inside LM Studio. Search for `Ronin48/atticus`.

---

## Project Structure

```
ATTICUS/
├── LICENSE                          # Apache 2.0
├── README.md                        # This file
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
│   │   ├── fetch_federal_statutes.py    # Title 18, FRCrP, USSG, Constitution
│   │   ├── fetch_state_statutes.py      # GA, CA, TX, NY, FL criminal codes
│   │   ├── fetch_caselaw.py             # SCOTUS opinions, CourtListener
│   │   └── fetch_innocence_data.py      # Exonerations, Innocence Project, DPIC
│   ├── training/
│   │   ├── train_qlora.py
│   │   ├── prepare_dataset.py
│   │   └── merge_adapter.py
│   └── evaluation/
├── src/atticus/
│   └── prompts.py                       # System prompt and Constitutional Override
├── tests/
└── docs/
    ├── TRAINING.md
    ├── DATA_SOURCES.md
    └── USAGE.md
```

---

## Training Data Sources

| Source | Description | Size | License |
|--------|-------------|------|---------|
| U.S. Code Title 18 | Federal criminal statutes (USLM XML) | ~2,700 sections | Public Domain |
| Federal Rules of Criminal Procedure | Procedural rights of defendants | Full text | Public Domain |
| U.S. Sentencing Guidelines (USSG) | Sentencing ranges and mitigating factors | Full manual | Public Domain |
| State Criminal Codes | GA, CA, TX, NY, FL criminal statutes | ~2,500 sections | Fair Use |
| SCOTUS Criminal Rights Opinions | 4th, 5th, 6th, 8th, 14th Amendment decisions | ~5K opinions | Public Domain |
| CourtListener | Federal criminal appeals, suppressions, acquittals | ~10K opinions | Open |
| National Registry of Exonerations | Wrongful conviction data | 3,000+ cases | Public Domain |
| Innocence Project Case Summaries | DNA exoneration case summaries | 375+ cases | Fair Use |
| LegalBench | Legal reasoning benchmark tasks | 91.8K examples | Open |
| CaseHOLD | Legal holding classification | 585K examples | Open |
| Synthetic | Generated charge-to-defense mappings | ~50K examples | Apache 2.0 |

---

## Disclaimer

ATTICUS is a research tool designed to assist defense attorneys and public defenders.
It is **NOT** a substitute for legal counsel, professional judgment, or representation
by a licensed attorney. All outputs should be verified by a licensed attorney before
any action is taken. The model may produce incorrect or incomplete legal analysis.

No defendant should make legal decisions based on ATTICUS alone. ATTICUS is a tool
to help counsel prepare — not a replacement for counsel.

This software is provided "AS IS" without warranty of any kind.

---

## Training Notes

If you're training ATTICUS on RunPod or another GPU cloud provider, read [LESSONS_LEARNED.md](LESSONS_LEARNED.md)
before you start. ABBY's file has the most complete record of first-run errors and fixes —
ATTICUS's file links there and will capture any ATTICUS-specific issues as they arise.

---

## Contributing

Contributions are welcome. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
Subject matter experts in criminal defense, constitutional law, and forensic science are
especially encouraged to contribute.

---

## License

**Project Code, Data, and Documentation:** Apache License 2.0 — Copyright 2026 Ronin 48, LLC.

**Base Model Weights:** Meta Llama 3.1 Community License. Fine-tuned adapter weights and
all original ATTICUS contributions remain Apache 2.0.

---

Proudly Made in Nebraska. Go Big Red!
