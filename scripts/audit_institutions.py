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
    "Huawei Noah's Ark Lab": "Noah's Ark Lab",
    "Huawei Noah’s Ark Lab": "Noah's Ark Lab",
    "Huawei Research (Noah's Ark Labs)": "Noah's Ark Lab",
    "Noah's Ark Lab": "Noah's Ark Lab",
    "Huawei Technologies Canada": "Huawei Technologies Canada",
    "Huawei Canada": "Huawei Technologies Canada",
    "Bosch China": "Bosch China",
    "Bosch Center for Artificial Intelligence": "Bosch Center for Artificial Intelligence",
    "Bosch Center for AI": "Bosch Center for Artificial Intelligence",
    "Bosch Corporate Research": "Bosch Corporate Research",
    "Robert Bosch GmbH, Corporate Research": "Bosch Corporate Research",
    "Robert Bosch GmbH Corporate Research": "Bosch Corporate Research",
    "Honda Research Institute Europe": "Honda Research Institute Europe",
    "Honda Research Institute Europe GmbH": "Honda Research Institute Europe",
    "Honda Research Institute, USA": "Honda Research Institute USA",
    "Honda Research Institute USA, Inc": "Honda Research Institute USA",
    "Honda Research Institute - USA": "Honda Research Institute USA",
    "Honda R&D Co., Ltd": "Honda R&D",
    "Toyota Motor North America R&D": "Toyota Motor North America R&D",
    "Toyota Motor North America, InfoTech Labs": "Toyota Motor North America R&D",
    "Toyota Motor North America, R&D": "Toyota Motor North America R&D",
    "Toyota Motor East Japan, Inc": "Toyota Motor East Japan",
    "Samsung Research America": "Samsung Research America",
    "AI Center, Samsung Electronics Co. LTD": "Samsung AI Center",
    "GeorgiaTech Lorraine": "Georgia Tech Europe",
    "Georgia Tech Europe - IRL 2958 GT-CNRS": "Georgia Tech Europe",
    "ByteDance Seed Robotics": "ByteDance Seed Robotics",
    "Mitsubishi Electric Research Laboratories": "MERL",
    "Mitsubishi Electric Research Laboratories (MERL)": "MERL",
    "MERL": "MERL",
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
    "Noah's Ark Lab, Huawei Technologies": ["Noah's Ark Lab"],
    "Noah's Ark Lab, Huawei": ["Noah's Ark Lab"],
    "Noah's Ark Lab, Huawei Technologies Canada Inc": ["Noah's Ark Lab"],
    "PICO, ByteDance": ["PICO"],
    "University of Sydney, NVIDIA": ["University of Sydney", "NVIDIA"],
    "Carnegie Mellon University; Vanderbilt University": ["Carnegie Mellon University", "Vanderbilt University"],
    "Allen Institute for AI, University of Washington": ["Allen Institute for AI", "University of Washington"],
}


SITE_COUNTRY_OVERRIDES = {
    "Huawei Technologies Canada": "Canada",
    "Huawei Canada": "Canada",
    "Huawei Noah's Ark Lab": "Canada",
    "Huawei Noah’s Ark Lab": "Canada",
    "Huawei Research (Noah's Ark Labs)": "Canada",
    "Noah's Ark Lab": "Canada",
    "Noah's Ark Lab, Huawei Technologies": "Canada",
    "Noah's Ark Lab, Huawei": "Canada",
    "Noah's Ark Lab, Huawei Technologies Canada Inc": "Canada",
    "University of Toronto, Noah's Ark Lab": "Canada",
    "Samsung Research America": "USA",
    "Honda Research Institute Europe": "Germany",
    "Honda Research Institute Europe GmbH": "Germany",
    "Honda Research Institute USA": "USA",
    "Honda Research Institute, USA": "USA",
    "Honda Research Institute USA, Inc": "USA",
    "Honda Research Institute - USA": "USA",
    "Honda R&D Co., Ltd": "Japan",
    "Honda R&D": "Japan",
    "Toyota Motor North America": "USA",
    "Toyota Motor North America R&D": "USA",
    "Toyota Motor North America, InfoTech Labs": "USA",
    "Toyota Motor North America, R&D": "USA",
    "Toyota Motor East Japan": "Japan",
    "Toyota Motor East Japan, Inc": "Japan",
    "Toyota Research Institute": "USA",
    "Bosch China": "China",
    "Bosch Center for Artificial Intelligence": "Germany",
    "Bosch Center for AI": "Germany",
    "Bosch Corporate Research": "Germany",
    "Robert Bosch GmbH, Corporate Research": "Germany",
    "Robert Bosch GmbH Corporate Research": "Germany",
    "Georgia Tech Europe": "France",
    "GeorgiaTech Lorraine": "France",
    "Georgia Tech Europe - IRL 2958 GT-CNRS": "France",
    "MERL": "USA",
    "Mitsubishi Electric Research Laboratories": "USA",
    "Mitsubishi Electric Research Laboratories (MERL)": "USA",
}


PARENT_ORG = {
    "Noah's Ark Lab": {
        "parent_org": "Huawei",
        "parent_country": "China",
        "institution_country": "Canada",
        "policy": "site-aware",
    },
    "Huawei Technologies Canada": {
        "parent_org": "Huawei",
        "parent_country": "China",
        "institution_country": "Canada",
        "policy": "regional-branch",
    },
    "Bosch China": {
        "parent_org": "Bosch",
        "parent_country": "Germany",
        "institution_country": "China",
        "policy": "regional-branch",
    },
    "Bosch Center for Artificial Intelligence": {
        "parent_org": "Bosch",
        "parent_country": "Germany",
        "institution_country": "Germany",
        "policy": "research-lab",
    },
    "Bosch Corporate Research": {
        "parent_org": "Bosch",
        "parent_country": "Germany",
        "institution_country": "Germany",
        "policy": "research-lab",
    },
    "Honda Research Institute Europe": {
        "parent_org": "Honda",
        "parent_country": "Japan",
        "institution_country": "Germany",
        "policy": "regional-research-lab",
    },
    "Honda Research Institute USA": {
        "parent_org": "Honda",
        "parent_country": "Japan",
        "institution_country": "USA",
        "policy": "regional-research-lab",
    },
    "Honda R&D": {
        "parent_org": "Honda",
        "parent_country": "Japan",
        "institution_country": "Japan",
        "policy": "regional-branch",
    },
    "Toyota Research Institute": {
        "parent_org": "Toyota",
        "parent_country": "Japan",
        "institution_country": "USA",
        "policy": "research-institute",
    },
    "Toyota Motor North America": {
        "parent_org": "Toyota",
        "parent_country": "Japan",
        "institution_country": "USA",
        "policy": "regional-branch",
    },
    "Toyota Motor North America R&D": {
        "parent_org": "Toyota",
        "parent_country": "Japan",
        "institution_country": "USA",
        "policy": "regional-branch",
    },
    "Toyota Motor East Japan": {
        "parent_org": "Toyota",
        "parent_country": "Japan",
        "institution_country": "Japan",
        "policy": "regional-branch",
    },
    "Samsung Research America": {
        "parent_org": "Samsung",
        "parent_country": "South Korea",
        "institution_country": "USA",
        "policy": "regional-research-lab",
    },
    "Samsung AI Center": {
        "parent_org": "Samsung",
        "parent_country": "South Korea",
        "institution_country": "South Korea",
        "policy": "site-aware",
    },
    "Georgia Tech Europe": {
        "parent_org": "Georgia Tech",
        "parent_country": "USA",
        "institution_country": "France",
        "policy": "overseas-campus",
    },
    "PICO": {
        "parent_org": "ByteDance",
        "parent_country": "China",
        "institution_country": "China",
        "policy": "subsidiary",
    },
    "ByteDance Seed Robotics": {
        "parent_org": "ByteDance",
        "parent_country": "China",
        "institution_country": "China",
        "policy": "research-lab",
    },
    "Alibaba DAMO Academy": {
        "parent_org": "Alibaba",
        "parent_country": "China",
        "institution_country": "China",
        "policy": "research-lab",
    },
    "MERL": {
        "parent_org": "Mitsubishi Electric",
        "parent_country": "Japan",
        "institution_country": "USA",
        "policy": "research-lab",
    },
}


DO_NOT_COLLAPSE = [
    {
        "child": "Noah's Ark Lab",
        "parent": "Huawei",
        "reason": "Noah's Ark Lab may be affiliated with Huawei, but its site/country should not be replaced by Huawei's parent-country.",
    },
    {
        "child": "Huawei Technologies Canada",
        "parent": "Huawei",
        "reason": "Regional branch in Canada; do not collapse to Huawei China for country attribution.",
    },
    {
        "child": "Bosch China",
        "parent": "Bosch",
        "reason": "Regional branch in China; do not collapse to Bosch Germany.",
    },
    {
        "child": "Honda Research Institute Europe",
        "parent": "Honda",
        "reason": "Regional research lab in Germany; do not collapse to Honda Japan.",
    },
    {
        "child": "Honda Research Institute USA",
        "parent": "Honda",
        "reason": "Regional research lab in USA; do not collapse to Honda Japan.",
    },
    {
        "child": "Toyota Research Institute",
        "parent": "Toyota",
        "reason": "Research institute in USA; do not collapse to Toyota Japan.",
    },
    {
        "child": "Toyota Motor North America",
        "parent": "Toyota",
        "reason": "Regional branch in USA; do not collapse to Toyota Japan.",
    },
    {
        "child": "Samsung Research America",
        "parent": "Samsung",
        "reason": "Regional research lab in USA; do not collapse to Samsung Korea.",
    },
    {
        "child": "Georgia Tech Europe",
        "parent": "Georgia Tech",
        "reason": "European campus/site in France; do not collapse to Georgia Tech USA for country attribution.",
    },
    {
        "child": "MERL",
        "parent": "Mitsubishi Electric",
        "reason": "Research lab in USA; do not collapse to Mitsubishi Electric Japan.",
    },
]


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
    site_country_overrides: dict[str, str],
    parent_org: dict[str, dict[str, str]],
) -> dict[str, str]:
    votes: dict[str, Counter[str]] = defaultdict(Counter)
    site_overrides = normalized_dict(site_country_overrides)
    for raw, country in aff_country.items():
        raw_normalized = normalize_affiliation_text(raw)
        for inst in canonicalize_affiliation(raw, aliases, multimap):
            country = site_overrides.get(raw_normalized)
            if not country:
                country = site_overrides.get(inst)
            if not country:
                country = fold_country(aff_country.get(raw, "Other"))
            if country == "Unknown":
                continue
            votes[inst][country] += 1

    out: dict[str, str] = {}
    for institution, counter in votes.items():
        if len(counter) == 1:
            out[institution] = next(iter(counter))
        else:
            winner, _ = counter.most_common(1)[0]
            out[institution] = winner

    for raw, country in site_country_overrides.items():
        for inst in canonicalize_affiliation(raw, aliases, multimap):
            out[inst] = country

    for institution, meta in parent_org.items():
        if "institution_country" in meta:
            out[institution] = meta["institution_country"]

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
    site_country_overrides: dict[str, str],
    parent_org: dict[str, dict[str, str]],
    do_not_collapse: list[dict[str, str]],
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
            "Use this order: Unicode NFKC normalization -> whitespace and punctuation normalization -> raw affiliation exact site-country override -> exact multimap lookup -> exact alias lookup -> canonical institution site-country override -> canonical institution country lookup -> parent-org metadata institution_country fallback -> fallback country hints -> manual review log.",
            "",
            "Do not split commas, slashes, ampersands, semicolons, `and`, or `with` automatically. Split only when the exact raw string is in `aff_institution_multimap.json`.",
            "",
            "Parent organization metadata is not a primary country-attribution source. For example, `Noah's Ark Lab` keeps Canada as the site-aware institution country while storing Huawei as parent metadata.",
            "",
            "## 10.1 Proposed aff_institution_site_country_overrides.json",
            "",
            json_block(site_country_overrides),
            "",
            "## 10.2 Proposed aff_institution_parent_org.json",
            "",
            json_block(parent_org),
            "",
            "## 10.3 Proposed aff_institution_do_not_collapse.json",
            "",
            json_block(do_not_collapse),
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
            "- `Huawei Noah's Ark Lab -> Noah's Ark Lab`, country Canada, parent Huawei.",
            "- `Noah's Ark Lab, Huawei Technologies -> Noah's Ark Lab`, country Canada, parent Huawei.",
            "- `Huawei Technologies Canada -> Huawei Technologies Canada`, country Canada, parent Huawei.",
            "- `Huawei Technologies -> Huawei`, country China.",
            "- `Bosch China -> Bosch China`, country China, parent Bosch.",
            "- `Honda Research Institute Europe -> Honda Research Institute Europe`, country Germany, parent Honda.",
            "- `Toyota Research Institute -> Toyota Research Institute`, country USA, parent Toyota.",
            "- `Georgia Tech Europe - IRL 2958 GT-CNRS -> Georgia Tech Europe`, country France, parent Georgia Tech.",
            "- `Mitsubishi Electric Research Laboratories -> MERL`, country USA, parent Mitsubishi Electric.",
            "",
            "## 12. Remaining Risks",
            "",
            "1. Some affiliation strings are compound affiliations and require an explicit split policy.",
            "2. Some company labs can be counted either at lab level or parent-company level.",
            "3. Some campuses can be counted separately or merged into university-system-level entities.",
            "4. Inverted names such as `Bonn University` are handled only by explicit alias mapping.",
            "5. Comma-containing strings are not split automatically.",
            "6. Ambiguous strings are logged instead of silently normalized.",
            "7. Parent-organization roll-up charts should be separate from institution-level ranking charts.",
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
    site_country_overrides = dict(sorted(SITE_COUNTRY_OVERRIDES.items(), key=lambda kv: kv[0].lower()))
    parent_org = dict(sorted(PARENT_ORG.items(), key=lambda kv: kv[0].lower()))
    do_not_collapse = sorted(DO_NOT_COLLAPSE, key=lambda x: (x["parent"].lower(), x["child"].lower()))
    ambiguous = build_ambiguous(aff_counts, aliases, multimap, aff_country)
    institution_country = country_by_canonical(
        aliases,
        multimap,
        aff_country,
        site_country_overrides,
        parent_org,
    )

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
    (CLASSIFICATION_DIR / "aff_institution_site_country_overrides.json").write_text(
        json.dumps(site_country_overrides, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (CLASSIFICATION_DIR / "aff_institution_parent_org.json").write_text(
        json.dumps(parent_org, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (CLASSIFICATION_DIR / "aff_institution_do_not_collapse.json").write_text(
        json.dumps(do_not_collapse, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_review_log(
        aliases,
        multimap,
        do_not_merge,
        ambiguous,
        aff_country,
        aff_counts,
        institution_country,
        site_country_overrides,
        parent_org,
        do_not_collapse,
    )

    print(f"aliases: {len(aliases)}")
    print(f"multimap: {len(multimap)}")
    print(f"do_not_merge: {len(do_not_merge)}")
    print(f"ambiguous: {len(ambiguous)}")
    print(f"site_country_overrides: {len(site_country_overrides)}")
    print(f"parent_org: {len(parent_org)}")
    print(f"do_not_collapse: {len(do_not_collapse)}")


if __name__ == "__main__":
    main()
