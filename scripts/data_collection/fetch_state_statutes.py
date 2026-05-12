#!/usr/bin/env python3
"""
Fetch state criminal codes for ATTICUS.

Priority states: Georgia, California, Texas, New York, Florida.
Each state's code is fetched from official legislature sources.
"""

import json
import time
from pathlib import Path

import requests

RAW_DIR = Path("data/raw/states")
RAW_DIR.mkdir(parents=True, exist_ok=True)

STATES = {
    "georgia": {
        "name": "Georgia",
        "code": "O.C.G.A. Title 16",
        "url": "https://law.justia.com/codes/georgia/title-16/",
        "notes": "Crimes and Offenses",
    },
    "california": {
        "name": "California",
        "code": "California Penal Code",
        "url": "https://law.justia.com/codes/california/penal-code/",
        "notes": "California Penal Code",
    },
    "texas": {
        "name": "Texas",
        "code": "Texas Penal Code",
        "url": "https://law.justia.com/codes/texas/penal-code/",
        "notes": "Texas Penal Code",
    },
    "new_york": {
        "name": "New York",
        "code": "NY Penal Law",
        "url": "https://law.justia.com/codes/new-york/penal-law/",
        "notes": "New York Penal Law",
    },
    "florida": {
        "name": "Florida",
        "code": "Florida Statutes Title XLVI",
        "url": "https://law.justia.com/codes/florida/title-xlvi/",
        "notes": "Crimes",
    },
    "federal": {
        "name": "Federal",
        "code": "18 U.S.C.",
        "url": "https://law.justia.com/codes/us/title-18/",
        "notes": "Federal criminal code",
    },
}

HEADERS = {"User-Agent": "ATTICUS-Research/1.0 (akclark@thenetwerk.net)"}


def fetch_state(state_key: str):
    state = STATES[state_key]
    print(f"\n  Fetching {state['name']} — {state['code']}...")
    out_dir = RAW_DIR / state_key
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        resp = requests.get(state["url"], headers=HEADERS, timeout=30)
        resp.raise_for_status()
        out = out_dir / "index.html"
        out.write_bytes(resp.content)

        meta = {
            "state": state_key,
            "name": state["name"],
            "code": state["code"],
            "source_url": state["url"],
            "notes": state["notes"],
            "size_bytes": len(resp.content),
        }
        (out_dir / "meta.json").write_text(json.dumps(meta, indent=2))
        print(f"    Saved {len(resp.content)//1024}KB → {out}")
    except Exception as e:
        print(f"    Warning: {e}")

    time.sleep(2)


if __name__ == "__main__":
    import sys
    states_to_fetch = sys.argv[1:] if len(sys.argv) > 1 else list(STATES.keys())
    print("=" * 60)
    print("ATTICUS — State Statute Collection")
    print("=" * 60)
    for state in states_to_fetch:
        if state in STATES:
            fetch_state(state)
        else:
            print(f"Unknown state: {state}. Available: {list(STATES.keys())}")
    print("\n✓ State statute collection complete.")
