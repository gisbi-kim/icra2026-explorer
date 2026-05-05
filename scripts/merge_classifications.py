"""Merge the 5 fullaff_*_classified.json files into a single authoritative
affiliation -> country lookup table.

Outputs:
  - aff_country_table.json : { affiliation_string: country }
  - aff_country_stats.txt  : summary by country, list of Unknowns
"""
from __future__ import annotations
import json
import sys
import io
from pathlib import Path
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
CLASSIFICATION = ROOT / "classification"

def main():
    table = {}
    seen = set()
    duplicates = []
    for i in range(1, 6):
        fp = CLASSIFICATION / f"fullaff_{i}_classified.json"
        if not fp.exists():
            print(f"WARNING: {fp.name} missing — agent may not have finished")
            continue
        arr = json.loads(fp.read_text(encoding="utf-8"))
        for d in arr:
            aff = d["aff"]
            country = d["country"]
            # Normalize HK/Macau into China defensively
            if country in ("Hong Kong", "Macau"):
                country = "China"
            if aff in seen:
                duplicates.append(aff)
                continue
            seen.add(aff)
            table[aff] = country

    # Stats
    counter = Counter(table.values())
    unknowns = [a for a, c in table.items() if c == "Unknown"]

    print(f"total entries: {len(table)}")
    print(f"distinct countries: {len(counter)}")
    print(f"unknowns: {len(unknowns)}")
    print(f"duplicates skipped: {len(duplicates)}")
    print("\ncountry breakdown:")
    for c, n in counter.most_common():
        print(f"  {n:5d}  {c}")
    if unknowns:
        print("\nunknown affiliations:")
        for u in unknowns[:50]:
            print(f"  {u}")

    out_table = CLASSIFICATION / "aff_country_table.json"
    out_table.parent.mkdir(parents=True, exist_ok=True)
    out_table.write_text(json.dumps(table, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nwrote {out_table}")

if __name__ == "__main__":
    main()
