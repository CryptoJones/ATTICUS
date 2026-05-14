#!/usr/bin/env python3
"""Prepare training dataset for ATTICUS fine-tuning."""

import json
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src" / "atticus"))

SYNTHETIC_DIR = REPO_ROOT / "data" / "synthetic"
RAW_DIR = REPO_ROOT / "data" / "raw"
OUTPUT_DIR = REPO_ROOT / "data" / "processed"

from prompts import SYSTEM_PROMPT


def load_synthetic() -> list[dict]:
    examples = []
    for path in SYNTHETIC_DIR.glob("*.jsonl"):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    examples.append(json.loads(line))
    print(f"  Synthetic: {len(examples)} examples")
    return examples


def load_raw() -> list[dict]:
    examples = []
    if not RAW_DIR.exists():
        return examples
    for path in RAW_DIR.glob("*.jsonl"):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        examples.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    print(f"  Raw: {len(examples)} examples")
    return examples


def split_dataset(examples: list[dict], eval_ratio: float = 0.05) -> tuple:
    random.shuffle(examples)
    split_idx = int(len(examples) * (1 - eval_ratio))
    return examples[:split_idx], examples[split_idx:]


def save_jsonl(examples: list[dict], path: Path):
    with open(path, "w") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")


def main():
    print("=" * 60)
    print("ATTICUS — Preparing Training Dataset")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_examples = []

    print("\nLoading synthetic scenarios...")
    all_examples.extend(load_synthetic())

    print("\nLoading raw data...")
    all_examples.extend(load_raw())

    print(f"\nTotal examples: {len(all_examples)}")

    train, eval_set = split_dataset(all_examples)
    print(f"Train: {len(train)}, Eval: {len(eval_set)}")

    save_jsonl(train, OUTPUT_DIR / "train.jsonl")
    save_jsonl(eval_set, OUTPUT_DIR / "eval.jsonl")

    stats = {
        "total": len(all_examples),
        "train": len(train),
        "eval": len(eval_set),
    }
    with open(OUTPUT_DIR / "dataset_stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    print(f"\nDataset saved to {OUTPUT_DIR}/")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
