"""Generate the institution canonicalization audit artifacts.

The seed mappings come from the external final prompt. This script then marks
which aliases are observed in the current ICRA 2026 data and adds a conservative
set of high-confidence aliases discovered in the repository.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

from institution_canonicalization import (
    canonicalize_affiliation,
    normalize_affiliation_text,
    normalized_dict,
    normalized_multimap,
)


ROOT = Path(__file__).resolve().parent.parent
CLASSIFICATION_DIR = ROOT / "classification"
DEFAULT_PROMPT = Path.home() / "Downloads" / "institution_canonicalization_final_prompt.md"


EXTRA_ALIASES = {
    "ETH": "ETH Zurich",
    "ETHZ": "ETH Zurich",
    "ETH ZUrich": "ETH Zurich",
    "RSL, ETHZ": "ETH Zurich",
    "Rehabilitation Engineering Laboratory, ETH Zurich": "ETH Zurich",
    "ETH Zurich, Mimic Robotics": "ETH Zurich",
    "ETH Zurich, Autonomous Systems Lab": "ETH Zurich",
    "ETH Zurich, Automatic Control Laboratory (IfA)": "ETH Zurich",
    "Epfl": "EPFL",
    "École Polytechnique Fédérale De Lausanne (EPFL)": "EPFL",
    "École Polytechnique Fédérale De Lausanne (EPFL), Switzerland": "EPFL",
    "EPFL, Lausanne, Switzerland": "EPFL",
    "Ecole Polytechnique Federale De Lausanne": "EPFL",
    "Ecole Polytechnique Fédérale De Lausanne": "EPFL",
    "Technische Universitaet Muenchen": "Technical University of Munich",
    "University of Michigan Ann Arbor": "University of Michigan",
    "University of Michigan - Ann Arbor": "University of Michigan",
    "University of Michigan-Ann Arbor": "University of Michigan",
    "Univeristy of Michigan": "University of Michigan",
    "University of Wisconsin -- Madison": "University of Wisconsin-Madison",
    "University of Wisconsin, Madison": "University of Wisconsin-Madison",
    "University of Wisconsin Madison": "University of Wisconsin-Madison",
    "UIUC": "University of Illinois Urbana-Champaign",
    "University of Illinois-Urbana Champaign": "University of Illinois Urbana-Champaign",
    "University of California at Berkeley": "UC Berkeley",
    "University of California -- Berkeley": "UC Berkeley",
    "University of California: Berkeley": "UC Berkeley",
    "UC University of California, Berkeley": "UC Berkeley",
    "UC,Berkeley": "UC Berkeley",
    "UC, Berkeley": "UC Berkeley",
    "Univeristy of California, Berkeley": "UC Berkeley",
    "Univerisity of California, Berkeley": "UC Berkeley",
    "Berkeley": "UC Berkeley",
    "University of California - San Diego": "UC San Diego",
    "University of California San Diego (UCSD)": "UC San Diego",
    "University of California at San Diego": "UC San Diego",
    "UC San Diego (UCSD)": "UC San Diego",
    "University of California Los Angeles": "UCLA",
    "University of California, Los Angeles (UCLA)": "UCLA",
    "University of California at Los Angeles": "UCLA",
    "University of California Riverside": "University of California, Riverside",
    "University of California - Riverside": "University of California, Riverside",
    "UC Riverside": "University of California, Riverside",
    "UC Davis": "University of California, Davis",
    "University of California Santa Barbara": "University of California, Santa Barbara",
    "UC Merced": "University of California, Merced",
    "University of California, Merced": "University of California, Merced",
    "CALTECH": "Caltech",
    "California Institute of Technology (Caltech)": "Caltech",
    "NASA JPL": "NASA Jet Propulsion Laboratory",
    "The Georgia Institute of Technology": "Georgia Tech",
    "Oxford University": "University of Oxford",
    "Responsible Technology Institute, University of Oxford": "University of Oxford",
    "King’s College London": "King's College London",
    "Southern University of Science and Technology (SUSTech)": "SUSTech",
    "TsinghuaUniversity": "Tsinghua University",
    "Tsinghua Univeristy": "Tsinghua University",
    "Tsinghua Unviersity": "Tsinghua University",
    "Tsinghua Univ": "Tsinghua University",
    "Tsinghua university": "Tsinghua University",
    "tsinghua university": "Tsinghua University",
    "​Tsinghua University": "Tsinghua University",
    "Institute for AI Industry Research (AIR), Tsinghua University": "Tsinghua University",
    "Institute for AI Industry Research(AIR), Tsinghua University": "Tsinghua University",
    "AIR, Tsinghua University": "Tsinghua University",
    "Shenzhen Graduate School, Tsinghua University": "Tsinghua University",
    "Tsinghua Shenzhen International Graduate School, Tsinghua University": "Tsinghua University",
    "Peking University (PKU)": "Peking University",
    "Peking Univesity": "Peking University",
    "Peking Universitiy": "Peking University",
    "Institute for Artificial Intelligence, Peking University": "Peking University",
    "Peking University Shenzhen Graduate School": "Peking University",
    "State Key Laboratory of General Artificial Intelligence, Peking University, Shenzhen Graduate School": "Peking University",
    "State Key Laboratory of General Artificial Inteligence, Peking University, Shenzhen Graduate School": "Peking University",
    "Advanced Institute of Information Technology (AIIT), Peking University": "Peking University",
    "Shanghai Jiao Ton University": "Shanghai Jiao Tong University",
    "Shanghai Jiao Tong Univ": "Shanghai Jiao Tong University",
    "Shanghai Jiao Tong University, Shanghai Innovation Institute": "Shanghai Jiao Tong University",
    "Shanghai Jiao Tong University, Shanghai Artificial Intelligence Laboratory": "Shanghai Jiao Tong University",
    "Zhejiang Univerisity": "Zhejiang University",
    "Zhejiang university, robotics institute": "Zhejiang University",
    "Zhejiang University, Robotics Institute": "Zhejiang University",
    "Southern University of Science and Technology (SUSTech)": "SUSTech",
    "National University of Singapore (NUS)": "National University of Singapore",
    "NUS": "National University of Singapore",
    "Nanyang Technological University (NTU)": "Nanyang Technological University",
    "Nanyang Technological University, Singapore": "Nanyang Technological University",
    "Nanyang Technology University": "Nanyang Technological University",
    "Nanyang Technoligical University": "Nanyang Technological University",
    "The Chinese University of Hong Kong (CUHK)": "CUHK",
    "CUHK": "CUHK",
    "T-Stone Robotics Institute, the Chinese University of Hong Kong": "CUHK",
    "Hong Kong University": "University of Hong Kong",
    "The Chinese University of Hong Kong (Shenzhen)": "CUHK Shenzhen",
    "Chinese University of Hong Kong (Shenzhen)": "CUHK Shenzhen",
    "The Chinese Unviersity of Hong Kong, Shenzhen": "CUHK Shenzhen",
    "The Chinese University of Hong Kong CUHK (Shenzhen)": "CUHK Shenzhen",
    "CUHK(SZ)": "CUHK Shenzhen",
    "The Hong Kong University of Science and Technology(Guangzhou)": "HKUST Guangzhou",
    "The Hong Kong University of Science and Technology(GuangZhou)": "HKUST Guangzhou",
    "The Hong Kong University of Science and Technology (HKUST)": "HKUST",
    "The Hong Kong University of Science and Technology, Robotic Institute": "HKUST",
    "The Hong Kong Polytechnic University (PolyU)": "Hong Kong Polytechnic University",
    "KAUST (King Abdullah University of Science and Technology)": "KAUST",
    "Inria Center at University of Rennes": "Inria",
    "Inria Bordeaux": "Inria",
    "Inria Paris": "Inria",
    "INRIA Nancy - Grand Est": "Inria",
    "Inria centre at the university of Bordeaux, F-33405 Talence, France": "Inria",
}


EXTRA_MULTIMAP = {
    "ETH Zurich & IDSIA, USI-SUPSI": ["ETH Zurich", "IDSIA, USI-SUPSI"],
    "ETH Zurich, Stanford": ["ETH Zurich", "Stanford University"],
    "ETH Zurich & University of Cyprus": ["ETH Zurich", "University of Cyprus"],
    "ETH Zurich and EPFL": ["ETH Zurich", "EPFL"],
    "Idiap Research Institute; EPFL": ["Idiap Research Institute", "EPFL"],
    "Idiap Research Institute and EPFL": ["Idiap Research Institute", "EPFL"],
    "NASA / Caltech Jet Propulsion Laboratory": ["NASA Jet Propulsion Laboratory", "Caltech"],
    "Nasa's Jet Propulsion Laboratory, Caltech": ["NASA Jet Propulsion Laboratory", "Caltech"],
    "MIT, Woods Hole Oceanographic Institution": ["MIT", "Woods Hole Oceanographic Institution"],
    "Singapore University of Technology and Design, MIT": [
        "Singapore University of Technology and Design",
        "MIT",
    ],
    "UC Berkeley / TOYOTA Motor North America": ["UC Berkeley", "Toyota Motor North America"],
    "NVIDIA, UC Berkeley": ["NVIDIA", "UC Berkeley"],
    "University of Illinois Urbana-Champaign/NASA Jet Propulsion Laboratory": [
        "University of Illinois Urbana-Champaign",
        "NASA Jet Propulsion Laboratory",
    ],
    "University of Illinois Urbana-Champaign & Instituto Tecnológico Autónomo de México": [
        "University of Illinois Urbana-Champaign",
        "Instituto Tecnológico Autónomo de México",
    ],
    "University of Illinois Urbana-Champaign & Instituto Tecnológico Autónomo De México": [
        "University of Illinois Urbana-Champaign",
        "Instituto Tecnológico Autónomo de México",
    ],
    "Stanford & UIUC": ["Stanford University", "University of Illinois Urbana-Champaign"],
    "University of Oxford, NVIDIA": ["University of Oxford", "NVIDIA"],
    "National University of Singapore, the University of Hong Kong": [
        "National University of Singapore",
        "University of Hong Kong",
    ],
    "Dalian Univ. of Tech.; CUHK-Shenzhen": ["Dalian University of Technology", "CUHK Shenzhen"],
    "Beijing University of Posts and Telecommunications / Tsinghua University": [
        "Beijing University of Posts and Telecommunications",
        "Tsinghua University",
    ],
    "Tsinghua University; Shanghai Qi Zhi Institute": [
        "Tsinghua University",
        "Shanghai Qi Zhi Institute",
    ],
    "Tencent, Tsinghua University": ["Tencent", "Tsinghua University"],
    "Zhejiang University, Westlake University": ["Zhejiang University", "Westlake University"],
    "Westlake University, Zhejiang University": ["Westlake University", "Zhejiang University"],
    "Zhejiang University, Idiap Research Institute": ["Zhejiang University", "Idiap Research Institute"],
    "Zhejiang University, Shanghai AI Laboratory": ["Zhejiang University", "Shanghai AI Laboratory"],
}


EXTRA_DO_NOT_MERGE = [
    {
        "a": "University of Oxford",
        "b": "Oxford Brookes University",
        "reason": "Different UK universities despite shared city name.",
    },
    {
        "a": "MIT",
        "b": "Mitsubishi Electric Research Laboratories",
        "reason": "Substring MIT appears inside unrelated institution/company names.",
    },
    {
        "a": "University of California",
        "b": "University of California, Merced",
        "reason": "System-level name should not be automatically mapped to a specific campus.",
    },
]


def load_prompt_json_blocks(prompt_path: Path) -> tuple[dict[str, str], dict[str, list[str]], list[dict[str, str]]]:
    text = prompt_path.read_text(encoding="utf-8")
    blocks = re.findall(r"```json\s*(.*?)\s*```", text, re.S)
    if len(blocks) < 3:
        raise ValueError(f"Expected at least 3 JSON blocks in {prompt_path}, found {len(blocks)}")
    aliases = json.loads(blocks[0])
    multimap = json.loads(blocks[1])
    do_not_merge = json.loads(blocks[2])
    return aliases, multimap, do_not_merge


def load_affiliation_counts() -> Counter[str]:
    papers = json.loads((ROOT / "output" / "papers.json").read_text(encoding="utf-8"))["papers"]
    counts: Counter[str] = Counter()
    for paper in papers:
        seen = set()
        for author in paper["authors"]:
            aff = author["aff"]
            if aff not in seen:
                counts[aff] += 1
                seen.add(aff)
    return counts


def fold_country(country: str) -> str:
    return "China" if country in {"Hong Kong", "Macau"} else country


def country_by_canonical(
    aliases: dict[str, str],
    multimap: dict[str, list[str]],
    aff_country: dict[str, str],
) -> dict[str, str]:
    votes: dict[str, Counter[str]] = defaultdict(Counter)
    for raw, country in aff_country.items():
        country = fold_country(country)
        if country == "Unknown":
            continue
        for inst in canonicalize_affiliation(raw, aliases, multimap):
            votes[inst][country] += 1

    out: dict[str, str] = {}
    for institution, counter in votes.items():
        if len(counter) == 1:
            out[institution] = next(iter(counter))
        else:
            winner, _ = counter.most_common(1)[0]
            out[institution] = winner
    return dict(sorted(out.items()))


def ascii_fold(text: str) -> str:
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii").lower()


def merge_type(raw: str, canonical: str) -> str:
    raw_l = raw.lower()
    canon_l = canonical.lower()
    if "," in raw or ";" in raw:
        if canonical.lower() in raw_l:
            return "campus/subunit suffix"
        return "punctuation variant"
    if raw.upper() == raw and len(raw) <= 8:
        return "acronym/full-name"
    if "(" in raw and ")" in raw:
        return "acronym/full-name"
    if ascii_fold(raw) == ascii_fold(canonical) and raw != canonical:
        return "accent/unaccented"
    if raw_l.replace("the ", "") == canon_l.replace("the ", ""):
        return "article variant"
    if raw_l.replace(" ", "") == canon_l.replace(" ", ""):
        return "spacing/case variant"
    if "univeristy" in raw_l or "unverisity" in raw_l or "coorporation" in raw_l or "technoligical" in raw_l:
        return "typo variant"
    if raw_l.endswith(" university") and canonical.startswith("University of "):
        return "inverted university-name variant"
    if canonical in raw:
        return "lab suffix"
    return "name variant"


def is_observed(raw: str, observed: set[str]) -> bool:
    n = normalize_affiliation_text(raw)
    return n in {normalize_affiliation_text(x) for x in observed}


def build_ambiguous(
    aff_counts: Counter[str],
    aliases: dict[str, str],
    multimap: dict[str, list[str]],
    aff_country: dict[str, str],
) -> list[dict[str, object]]:
    alias_n = set(normalized_dict(aliases))
    multimap_n = set(normalized_multimap(multimap))
    suspicious = re.compile(r"(,|;|/|&|\band\b|\bwith\b)", re.I)
    rows = []
    for aff, count in aff_counts.most_common():
        n = normalize_affiliation_text(aff)
        if n in alias_n or n in multimap_n:
            continue
        if suspicious.search(aff):
            rows.append(
                {
                    "affiliation": aff,
                    "count": count,
                    "country": fold_country(aff_country.get(aff, "Other")),
                    "reason": "Contains a separator or subunit phrase and is not covered by alias/multimap.",
                }
            )
    return rows[:120]


def table_row(values: list[object]) -> str:
    escaped = [str(v).replace("|", "\\|").replace("\n", " ") for v in values]
    return "| " + " | ".join(escaped) + " |"


def json_block(obj: object) -> str:
    return "```json\n" + json.dumps(obj, ensure_ascii=False, indent=2) + "\n```"


def write_review_log(
    aliases: dict[str, str],
    multimap: dict[str, list[str]],
    do_not_merge: list[dict[str, str]],
    ambiguous: list[dict[str, object]],
    aff_country: dict[str, str],
    aff_counts: Counter[str],
    institution_country: dict[str, str],
) -> None:
    grouped: dict[str, list[str]] = defaultdict(list)
    for raw, canonical in aliases.items():
        grouped[canonical].append(raw)

    observed = {normalize_affiliation_text(x) for x in aff_country} | {
        normalize_affiliation_text(x) for x in aff_counts
    }

    merge_rows = []
    potential_rows = []
    inverted_rows = []
    for canonical, raws in sorted(grouped.items()):
        obs = [r for r in raws if normalize_affiliation_text(r) in observed]
        pot = [r for r in raws if normalize_affiliation_text(r) not in observed]
        confidence = "high" if obs else "potential"
        notes = "observed in current table" if obs else "potential alias; not observed in current table"
        row = [
            canonical,
            "; ".join(raws),
            institution_country.get(canonical, aff_country.get(canonical, "Other")),
            ", ".join(sorted({merge_type(r, canonical) for r in raws})),
            confidence,
            notes,
        ]
        merge_rows.append(row)
        if pot:
            potential_rows.append([canonical, "; ".join(pot), "potential alias"])
        for raw in raws:
            if raw.lower().endswith(" university") and canonical.startswith("University of "):
                inverted_rows.append([raw, canonical, "explicit alias only"])

    multi_rows = []
    for raw, institutions in sorted(multimap.items()):
        multi_rows.append(
            [
                raw,
                "; ".join(institutions),
                aff_counts.get(raw, 0),
                "observed" if raw in aff_counts or raw in aff_country else "potential",
                "split only by exact multimap lookup",
            ]
        )

    lines = [
        "# Institution Canonicalization Audit",
        "",
        "## 1. Executive Summary",
        "",
        "`classification/aff_country_table.json` remains the authoritative affiliation-to-country lookup table, but it is not a canonical institution table. Institution-level rankings are distorted when aliases, acronyms, typos, accents, inverted names, lab suffixes, company suffixes, and compound affiliations are counted as separate institutions. This audit adds a conservative layer: raw affiliation string -> canonical institution name(s) -> country.",
        "",
        "Be conservative. Merge only when identity is clear. If uncertain, send the case to manual review. Commas are not blindly split, and `X University` is not blindly rewritten as `University of X`.",
        "",
        "## 2. Canonical Merge Table",
        "",
        table_row(["Canonical Institution", "Raw Aliases to Merge", "Country", "Merge Type", "Confidence", "Notes"]),
        table_row(["---", "---", "---", "---", "---", "---"]),
    ]
    lines.extend(table_row(row) for row in merge_rows)
    lines.extend(
        [
            "",
            "## 3. Inverted University-Name Variant Table",
            "",
            table_row(["Raw Variant", "Canonical Institution", "Rule"]),
            table_row(["---", "---", "---"]),
        ]
    )
    lines.extend(table_row(row) for row in inverted_rows or [["None observed", "", ""]])
    lines.extend(
        [
            "",
            "## 4. Comma-Joined / Multi-Institution Affiliation Table",
            "",
            table_row(["Raw Affiliation", "Canonical Institutions", "Paper Count", "Status", "Notes"]),
            table_row(["---", "---", "---", "---", "---"]),
        ]
    )
    lines.extend(table_row(row) for row in multi_rows)
    lines.extend(
        [
            "",
            "## 5. Do-Not-Merge Table",
            "",
            table_row(["Institution A", "Institution B", "Reason"]),
            table_row(["---", "---", "---"]),
        ]
    )
    lines.extend(table_row([x["a"], x["b"], x["reason"]]) for x in do_not_merge)
    lines.extend(
        [
            "",
            "## 6. Ambiguous / Needs Manual Review Table",
            "",
            table_row(["Raw Affiliation", "Paper Count", "Country", "Reason"]),
            table_row(["---", "---", "---", "---"]),
        ]
    )
    lines.extend(table_row([x["affiliation"], x["count"], x["country"], x["reason"]]) for x in ambiguous)
    lines.extend(
        [
            "",
            "## 7. Proposed aff_institution_aliases.json",
            "",
            json_block(aliases),
            "",
            "Potential aliases not observed in the current table are retained in the JSON because they are high-confidence guards from the instruction, but the merge table marks them as potential.",
            "",
            "## 8. Proposed aff_institution_multimap.json",
            "",
            json_block(multimap),
            "",
            "Counting-policy recommendation: full counting with per-paper deduplication. A paper contributes at most one count to each canonical institution after exact multimap splitting and alias canonicalization.",
            "",
            "## 9. Proposed aff_institution_do_not_merge.json",
            "",
            json_block(do_not_merge),
            "",
            "## 10. Implementation Guideline",
            "",
            "Use this order: Unicode NFKC normalization -> whitespace and punctuation normalization -> exact multimap lookup -> exact alias lookup -> suspicious separator detection -> canonical institution name(s) -> canonical institution country lookup -> fallback country hints -> manual review log.",
            "",
            "Do not split commas, slashes, ampersands, semicolons, `and`, or `with` automatically. Split only when the exact raw string is in `aff_institution_multimap.json`.",
            "",
            "## 11. Suggested Tests",
            "",
            "- `ETH Zürich -> ETH Zurich`",
            "- `ETH Zurich, Robotic Systems Lab -> ETH Zurich`",
            "- `University of Zurich -> University of Zurich`",
            "- `Bonn University -> University of Bonn`",
            "- `Technical University of Munich (TUM) -> Technical University of Munich`",
            "- `TUM -> Technical University of Munich`",
            "- `Korea Advanced Institute of Science and Technology (KAIST) -> KAIST`",
            "- `Daegu Gyeongbuk Institute of Science and Technology(DGIST) -> DGIST`",
            "- `NASA-JPL, Caltech -> NASA Jet Propulsion Laboratory + Caltech`",
            "- `University of California, Berkeley -> UC Berkeley`",
            "- `University of Michigan, Ann Arbor -> University of Michigan`",
            "- `Washington University in St. Louis` remains unchanged.",
            "- `Shanghai Jiaotong University -> Shanghai Jiao Tong University`",
            "- `Institute of Automation，Chinese Academy of Sciences -> CASIA`",
            "- `NanyangTechnological University -> Nanyang Technological University`",
            "",
            "## 12. Remaining Risks",
            "",
            "1. Some affiliation strings are compound affiliations and require an explicit split policy.",
            "2. Some company labs can be counted either at lab level or parent-company level.",
            "3. Some campuses can be counted separately or merged into university-system-level entities.",
            "4. Inverted names such as `Bonn University` are handled only by explicit alias mapping.",
            "5. Comma-containing strings are not split automatically.",
            "6. Ambiguous strings are logged instead of silently normalized.",
            "",
        ]
    )
    (CLASSIFICATION_DIR / "aff_institution_review_log.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=Path, default=DEFAULT_PROMPT)
    args = parser.parse_args()

    seed_aliases, seed_multimap, seed_do_not_merge = load_prompt_json_blocks(args.prompt)
    aliases = dict(seed_aliases)
    aliases.update(EXTRA_ALIASES)
    multimap = dict(seed_multimap)
    multimap.update(EXTRA_MULTIMAP)
    do_not_merge = list(seed_do_not_merge)
    existing_pairs = {(x["a"], x["b"]) for x in do_not_merge}
    for item in EXTRA_DO_NOT_MERGE:
        if (item["a"], item["b"]) not in existing_pairs:
            do_not_merge.append(item)

    aff_country = json.loads((CLASSIFICATION_DIR / "aff_country_table.json").read_text(encoding="utf-8"))
    aff_counts = load_affiliation_counts()

    aliases = dict(sorted(aliases.items(), key=lambda kv: (kv[1].lower(), kv[0].lower())))
    multimap = dict(sorted(multimap.items(), key=lambda kv: kv[0].lower()))
    ambiguous = build_ambiguous(aff_counts, aliases, multimap, aff_country)
    institution_country = country_by_canonical(aliases, multimap, aff_country)

    CLASSIFICATION_DIR.mkdir(exist_ok=True)
    (CLASSIFICATION_DIR / "aff_institution_aliases.json").write_text(
        json.dumps(aliases, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (CLASSIFICATION_DIR / "aff_institution_multimap.json").write_text(
        json.dumps(multimap, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (CLASSIFICATION_DIR / "aff_institution_do_not_merge.json").write_text(
        json.dumps(do_not_merge, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (CLASSIFICATION_DIR / "aff_institution_ambiguous.json").write_text(
        json.dumps(ambiguous, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (CLASSIFICATION_DIR / "aff_institution_country_table.json").write_text(
        json.dumps(institution_country, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_review_log(aliases, multimap, do_not_merge, ambiguous, aff_country, aff_counts, institution_country)

    print(f"aliases: {len(aliases)}")
    print(f"multimap: {len(multimap)}")
    print(f"do_not_merge: {len(do_not_merge)}")
    print(f"ambiguous: {len(ambiguous)}")


if __name__ == "__main__":
    main()
