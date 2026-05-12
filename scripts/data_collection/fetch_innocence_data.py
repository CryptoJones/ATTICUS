#!/usr/bin/env python3
"""
Fetch wrongful conviction and innocence data for ATTICUS.

Sources:
- National Registry of Exonerations (publically available data)
- Innocence Project case summaries
- Death Penalty Information Center case data
"""

import json
import time
from pathlib import Path

import requests

RAW_DIR = Path("data/raw/innocence")
RAW_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "ATTICUS-Research/1.0 (akclark@thenetwerk.net)"}


def fetch_exonerations_registry():
    """Fetch National Registry of Exonerations public data."""
    print("\n" + "=" * 60)
    print("Fetching National Registry of Exonerations...")
    print("=" * 60)

    # Public CSV export from the registry
    urls = [
        ("https://www.law.umich.edu/special/exoneration/Documents/exonerations_02_14_24.csv",
         "exonerations.csv"),
    ]

    for url, fname in urls:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=60)
            resp.raise_for_status()
            out = RAW_DIR / fname
            out.write_bytes(resp.content)
            print(f"Saved {fname} ({len(resp.content)//1024}KB)")
        except Exception as e:
            print(f"Warning ({fname}): {e}")
            # Try alternate location
            try:
                alt = "https://raw.githubusercontent.com/williamlief/exonerationRegistry/main/data/exonerations.csv"
                resp = requests.get(alt, headers=HEADERS, timeout=30)
                resp.raise_for_status()
                out = RAW_DIR / fname
                out.write_bytes(resp.content)
                print(f"Saved from alt source: {fname}")
            except Exception as e2:
                print(f"Alt also failed: {e2}")


def fetch_dpic_data():
    """Fetch Death Penalty Information Center data on exonerations."""
    print("\n" + "=" * 60)
    print("Fetching DPIC death row exoneration data...")
    print("=" * 60)
    url = "https://deathpenaltyinfo.org/death-row/innocence"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        out = RAW_DIR / "dpic_exonerations.html"
        out.write_bytes(resp.content)
        print(f"Saved DPIC data ({len(resp.content)//1024}KB)")
    except Exception as e:
        print(f"Warning: {e}")


def fetch_innocence_project():
    """Fetch Innocence Project case summaries."""
    print("\n" + "=" * 60)
    print("Fetching Innocence Project case data...")
    print("=" * 60)
    url = "https://innocenceproject.org/all-cases/"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        out = RAW_DIR / "innocence_project_cases.html"
        out.write_bytes(resp.content)
        print(f"Saved Innocence Project cases ({len(resp.content)//1024}KB)")
    except Exception as e:
        print(f"Warning: {e}")


def create_wrongful_conviction_schema():
    """Create a structured schema for wrongful conviction patterns."""
    schema = {
        "description": "Common causes of wrongful conviction — training signal for ATTICUS",
        "causes": [
            {
                "cause": "Eyewitness Misidentification",
                "prevalence": "~70% of DNA exonerations",
                "defense_strategy": "Challenge identification procedure, cross-examine on lighting/distance/stress",
                "key_cases": ["Manson v. Brathwaite (1977)", "Neil v. Biggers (1972)"],
            },
            {
                "cause": "False Confessions",
                "prevalence": "~30% of DNA exonerations",
                "defense_strategy": "Challenge interrogation methods, demonstrate coercion, present expert on false confessions",
                "key_cases": ["Colorado v. Connelly (1986)", "Missouri v. Seibert (2004)"],
            },
            {
                "cause": "Informant Testimony",
                "prevalence": "~15% of wrongful convictions",
                "defense_strategy": "Expose incentives for testimony, request Giglio material on informant deals",
                "key_cases": ["Giglio v. United States (1972)"],
            },
            {
                "cause": "Forensic Evidence Failures",
                "prevalence": "~45% of DNA exonerations involved bad forensics",
                "defense_strategy": "Challenge lab procedures, hire independent experts, Daubert challenges",
                "key_cases": ["Daubert v. Merrell Dow (1993)", "Kumho Tire v. Carmichael (1999)"],
            },
            {
                "cause": "Brady Violations",
                "prevalence": "Suppressed exculpatory evidence",
                "defense_strategy": "File Brady motion, request all exculpatory evidence, sanctions for violations",
                "key_cases": ["Brady v. Maryland (1963)", "Strickler v. Greene (1999)"],
            },
            {
                "cause": "Ineffective Assistance of Counsel",
                "prevalence": "Significant contributor to wrongful convictions",
                "defense_strategy": "Post-conviction: show deficient performance and prejudice under Strickland",
                "key_cases": ["Strickland v. Washington (1984)", "Wiggins v. Smith (2003)"],
            },
        ]
    }
    out = RAW_DIR / "wrongful_conviction_schema.json"
    out.write_text(json.dumps(schema, indent=2))
    print(f"Created wrongful conviction schema → {out}")


if __name__ == "__main__":
    fetch_exonerations_registry()
    fetch_innocence_project()
    fetch_dpic_data()
    create_wrongful_conviction_schema()
    print("\n✓ Innocence data collection complete.")
