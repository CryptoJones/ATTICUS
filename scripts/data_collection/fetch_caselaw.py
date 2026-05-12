#!/usr/bin/env python3
"""
Fetch criminal defense case law for ATTICUS training.

Downloads:
- SCOTUS opinions on criminal rights (4th, 5th, 6th, 8th, 14th Amendment)
- CourtListener federal criminal appeals (acquittals, reversals, suppressions)
- Harvard Caselaw Access Project state court opinions
- Landmark suppression orders and Brady/Giglio decisions
"""

import json
import os
import time
from pathlib import Path

import requests
from tqdm import tqdm

RAW_DIR = Path("data/raw/caselaw")
CONST_DIR = Path("data/raw/constitutional")
RAW_DIR.mkdir(parents=True, exist_ok=True)
CONST_DIR.mkdir(parents=True, exist_ok=True)

# Key SCOTUS criminal rights cases — landmark decisions every defense attorney needs
LANDMARK_SCOTUS_CASES = [
    # 4th Amendment
    "Mapp v. Ohio (1961) — exclusionary rule applies to states",
    "Terry v. Ohio (1968) — stop and frisk standard",
    "Katz v. United States (1967) — reasonable expectation of privacy",
    "United States v. Jones (2012) — GPS tracking is a search",
    "Carpenter v. United States (2018) — cell phone location data",
    "Riley v. California (2014) — warrant required for cell phone search",
    # 5th Amendment
    "Miranda v. Arizona (1966) — Miranda warnings required",
    "Berghuis v. Thompkins (2010) — waiver of Miranda",
    "Salinas v. Texas (2013) — pre-arrest silence",
    # 6th Amendment
    "Gideon v. Wainwright (1963) — right to counsel",
    "Strickland v. Washington (1984) — ineffective assistance standard",
    "Crawford v. Washington (2004) — confrontation clause",
    "Batson v. Kentucky (1986) — race-based peremptory challenges",
    "Padilla v. Kentucky (2010) — counsel must advise on deportation",
    # 8th Amendment
    "Roper v. Simmons (2005) — no death penalty for juveniles",
    "Atkins v. Virginia (2002) — no death penalty for intellectually disabled",
    "Graham v. Florida (2010) — no LWOP for juveniles (non-homicide)",
    # Brady/Giglio
    "Brady v. Maryland (1963) — prosecution must disclose exculpatory evidence",
    "Giglio v. United States (1972) — impeachment evidence must be disclosed",
    "United States v. Bagley (1985) — materiality standard for Brady",
    # Double Jeopardy
    "Blockburger v. United States (1932) — same elements test",
    # Speedy Trial
    "Barker v. Wingo (1972) — speedy trial balancing test",
    # Due Process
    "Jackson v. Virginia (1979) — sufficiency of evidence standard",
    "Strickler v. Greene (1999) — Brady materiality",
]


def fetch_courtlistener_criminal_defense(max_pages=20):
    """Fetch criminal defense opinions from CourtListener API."""
    print("\n" + "=" * 60)
    print("Fetching CourtListener criminal defense opinions...")
    print("=" * 60)

    base_url = "https://www.courtlistener.com/api/rest/v4/opinions/"
    cl_token = os.environ.get("COURTLISTENER_TOKEN", "")
    headers = {
        "User-Agent": "ATTICUS-Research/1.0 (akclark@thenetwerk.net)",
        "Authorization": f"Token {cl_token}" if cl_token else "",
    }

    # Search for suppression orders, acquittals, reversals
    queries = [
        ("suppression_motion", "suppression+motion+fourth+amendment"),
        ("brady_giglio", "brady+material+exculpatory+evidence"),
        ("ineffective_counsel", "ineffective+assistance+counsel+strickland"),
        ("miranda_violations", "miranda+warnings+custodial+interrogation"),
        ("acquittals_reversals", "reversed+criminal+conviction+insufficient+evidence"),
        ("sentencing_mitigation", "downward+departure+sentencing+guidelines+mitigation"),
    ]

    all_results = []
    for query_name, query in queries:
        print(f"\n  Fetching: {query_name}")
        page = 1
        count = 0
        while page <= max_pages:
            try:
                resp = requests.get(
                    base_url,
                    params={"q": query, "type": "o", "order_by": "score desc",
                            "page": page, "format": "json"},
                    headers=headers,
                    timeout=30
                )
                if resp.status_code == 429:
                    print("  Rate limited, waiting 60s...")
                    time.sleep(60)
                    continue
                resp.raise_for_status()
                data = resp.json()
                results = data.get("results", [])
                if not results:
                    break
                for r in results:
                    all_results.append({
                        "source": "courtlistener",
                        "query": query_name,
                        "case_name": r.get("case_name", ""),
                        "date_filed": r.get("date_filed", ""),
                        "court": r.get("court", ""),
                        "url": r.get("absolute_url", ""),
                        "snippet": r.get("snippet", ""),
                    })
                count += len(results)
                page += 1
                time.sleep(1)  # be polite
            except Exception as e:
                print(f"  Warning: {e}")
                break
        print(f"  Got {count} results for {query_name}")

    out = RAW_DIR / "courtlistener_defense.jsonl"
    with open(out, "w") as f:
        for r in all_results:
            f.write(json.dumps(r) + "\n")
    print(f"\nSaved {len(all_results)} opinions to {out}")


def fetch_scotus_opinions():
    """Fetch SCOTUS criminal rights opinions via CourtListener."""
    print("\n" + "=" * 60)
    print("Fetching SCOTUS criminal rights opinions...")
    print("=" * 60)

    cl_token = os.environ.get("COURTLISTENER_TOKEN", "")
    headers = {
        "User-Agent": "ATTICUS-Research/1.0 (akclark@thenetwerk.net)",
        "Authorization": f"Token {cl_token}" if cl_token else "",
    }
    criminal_rights_queries = [
        "fourth amendment search seizure",
        "fifth amendment self incrimination miranda",
        "sixth amendment right to counsel",
        "eighth amendment cruel unusual punishment",
        "fourteenth amendment due process criminal",
        "brady material exculpatory evidence",
        "double jeopardy fifth amendment",
        "speedy trial sixth amendment",
    ]

    all_opinions = []
    for query in criminal_rights_queries:
        try:
            resp = requests.get(
                "https://www.courtlistener.com/api/rest/v4/opinions/",
                params={"q": query, "court": "scotus", "type": "o",
                        "order_by": "score desc", "page_size": 50, "format": "json"},
                headers=headers,
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            results = data.get("results", [])
            for r in results:
                all_opinions.append({
                    "source": "scotus",
                    "query": query,
                    "case_name": r.get("case_name", ""),
                    "date_filed": r.get("date_filed", ""),
                    "url": r.get("absolute_url", ""),
                    "snippet": r.get("snippet", ""),
                })
            print(f"  '{query}' → {len(results)} opinions")
            time.sleep(1)
        except Exception as e:
            print(f"  Warning for '{query}': {e}")

    out = CONST_DIR / "scotus_criminal_rights.jsonl"
    with open(out, "w") as f:
        for r in all_opinions:
            f.write(json.dumps(r) + "\n")
    print(f"\nSaved {len(all_opinions)} SCOTUS opinions to {out}")

    # Save landmark cases index
    landmark_out = CONST_DIR / "landmark_cases_index.json"
    with open(landmark_out, "w") as f:
        json.dump({"landmark_cases": LANDMARK_SCOTUS_CASES}, f, indent=2)
    print(f"Saved landmark cases index to {landmark_out}")


def fetch_hf_legal_datasets():
    """Fetch defense-relevant HuggingFace datasets."""
    print("\n" + "=" * 60)
    print("Fetching HuggingFace legal datasets...")
    print("=" * 60)

    try:
        from datasets import load_dataset

        # LegalBench — legal reasoning tasks
        print("  Loading LegalBench...")
        defense_tasks = [
            "hearsay",                          # evidence admissibility
            "rule_qa",                          # rule application
            "citation_prediction_classification", # case law
            "abercrombie",                      # legal standards
        ]
        for task in defense_tasks:
            try:
                ds = load_dataset("HazyResearch/legalbench", task, trust_remote_code=True)
                out = Path("data/raw") / f"legalbench_{task}.jsonl"
                count = 0
                with open(out, "w") as f:
                    for split in ds:
                        for example in ds[split]:
                            f.write(json.dumps(dict(example)) + "\n")
                            count += 1
                print(f"  LegalBench/{task}: {count} examples → {out}")
            except Exception as e:
                print(f"  Warning LegalBench/{task}: {e}")

        # CaseHOLD — legal holding classification
        print("  Loading CaseHOLD...")
        try:
            ds = load_dataset("casehold/casehold", trust_remote_code=True)
            out = Path("data/raw/caselaw/casehold.jsonl")
            count = 0
            with open(out, "w") as f:
                for split in ds:
                    for ex in tqdm(ds[split], desc=f"CaseHOLD/{split}"):
                        f.write(json.dumps(dict(ex)) + "\n")
                        count += 1
            print(f"  CaseHOLD: {count} examples → {out}")
        except Exception as e:
            print(f"  Warning CaseHOLD: {e}")

        # MultiLegalPile — multilingual legal corpus
        print("  Loading MultiLegalPile (US subset)...")
        try:
            ds = load_dataset("joelniklaus/multi_legal_pile", "default", streaming=True, trust_remote_code=True)
            out = Path("data/raw/caselaw/multi_legal_pile_en.jsonl")
            count = 0
            with open(out, "w") as f:
                for ex in tqdm(ds["train"].take(50000), desc="MultiLegalPile"):
                    f.write(json.dumps({"text": ex.get("text", ""), "source": ex.get("source", "")}) + "\n")
                    count += 1
            print(f"  MultiLegalPile: {count} examples → {out}")
        except Exception as e:
            print(f"  Warning MultiLegalPile: {e}")

    except ImportError:
        print("  Install datasets: pip install datasets")


if __name__ == "__main__":
    fetch_scotus_opinions()
    fetch_courtlistener_criminal_defense()
    fetch_hf_legal_datasets()
    print("\n✓ Case law collection complete.")
