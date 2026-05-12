#!/usr/bin/env python3
"""
Fetch U.S. Code Title 18 and Federal Rules of Criminal Procedure for ATTICUS.

Downloads:
- 18 U.S.C. (Crimes and Criminal Procedure) — same statutes SELMA charges with,
  but parsed from a DEFENSE perspective (elements the prosecution must prove)
- Federal Rules of Criminal Procedure (FRCrP) — procedural rights of defendants
- U.S. Sentencing Guidelines (USSG) — for mitigation analysis
"""

import json
import re
import sys
import zipfile
from pathlib import Path

import requests
from tqdm import tqdm

RAW_DIR = Path("data/raw/federal")
OUTPUT_DIR = Path("data/processed")
RAW_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TITLE18_FALLBACK = "https://uscode.house.gov/download/releasepoints/us/pl/119/88/xml_usc18@119-88.zip"
TITLE18_PAGE = "https://uscode.house.gov/download/download.shtml"


def discover_title18_url():
    try:
        resp = requests.get(TITLE18_PAGE, timeout=15)
        matches = re.findall(r'href="([^"]*xml_usc18@[^"]+\.zip)"', resp.text)
        if matches:
            url = matches[0]
            if url.startswith("http"):
                return url
            if not url.startswith("/"):
                url = "/download/" + url
            return "https://uscode.house.gov" + url
    except Exception as e:
        print(f"Warning: URL discovery failed ({e}); using fallback.")
    return TITLE18_FALLBACK


def fetch_title18():
    print("\n" + "=" * 60)
    print("Fetching U.S. Code Title 18 (Crimes & Criminal Procedure)...")
    print("=" * 60)
    url = discover_title18_url()
    zip_path = RAW_DIR / "usc18.zip"

    print(f"Downloading: {url}")
    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()
    total = int(resp.headers.get("content-length", 0))
    with open(zip_path, "wb") as f, tqdm(total=total, unit="B", unit_scale=True) as pbar:
        for chunk in resp.iter_content(8192):
            f.write(chunk)
            pbar.update(len(chunk))

    print(f"Saved to {zip_path}")
    return zip_path


def fetch_frcr():
    """Fetch Federal Rules of Criminal Procedure from Cornell LII."""
    print("\n" + "=" * 60)
    print("Fetching Federal Rules of Criminal Procedure...")
    print("=" * 60)
    url = "https://www.law.cornell.edu/rules/frcrmp"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        out = RAW_DIR / "federal_rules_criminal_procedure.html"
        out.write_bytes(resp.content)
        print(f"Saved FRCrP to {out} ({len(resp.content)//1024}KB)")
    except Exception as e:
        print(f"Warning: Could not fetch FRCrP: {e}")


def fetch_ussg():
    """Fetch U.S. Sentencing Guidelines from USSC."""
    print("\n" + "=" * 60)
    print("Fetching U.S. Sentencing Guidelines...")
    print("=" * 60)
    urls = [
        ("https://www.ussc.gov/guidelines/2024-guidelines-manual/2024-guidelines-manual-annotated",
         "ussg_guidelines.html"),
        ("https://www.ussc.gov/sites/default/files/pdf/guidelines-manual/2023/GLMFull.pdf",
         "ussg_guidelines_2023.pdf"),
    ]
    for url, fname in urls:
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            out = RAW_DIR / fname
            out.write_bytes(resp.content)
            print(f"Saved {fname} ({len(resp.content)//1024}KB)")
        except Exception as e:
            print(f"Warning: Could not fetch {fname}: {e}")


def fetch_constitutional_amendments():
    """Fetch the Bill of Rights and key amendments from Constitution.congress.gov."""
    print("\n" + "=" * 60)
    print("Fetching U.S. Constitution (Amendments)...")
    print("=" * 60)
    url = "https://constitution.congress.gov/constitution/"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        out = RAW_DIR / "constitution.html"
        out.write_bytes(resp.content)
        print(f"Saved constitution.html ({len(resp.content)//1024}KB)")
    except Exception as e:
        print(f"Warning: Could not fetch constitution: {e}")


if __name__ == "__main__":
    fetch_constitutional_amendments()
    fetch_title18()
    fetch_frcr()
    fetch_ussg()
    print("\n✓ Federal data collection complete.")
