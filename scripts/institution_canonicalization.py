"""Pure functions for affiliation -> canonical institution normalization."""
from __future__ import annotations

import json
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CLASSIFICATION_DIR = ROOT / "classification"


def normalize_affiliation_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", str(text or ""))
    normalized = normalized.replace("，", ",")
    normalized = normalized.replace("；", ";")
    normalized = normalized.replace("＆", "&")
    normalized = " ".join(normalized.split())
    return normalized.strip().rstrip(",").strip()


def normalized_dict(data: dict[str, str]) -> dict[str, str]:
    return {normalize_affiliation_text(k): v for k, v in data.items()}


def normalized_multimap(data: dict[str, list[str]]) -> dict[str, list[str]]:
    return {normalize_affiliation_text(k): list(v) for k, v in data.items()}


def load_alias_map(path: Path | None = None) -> dict[str, str]:
    path = path or CLASSIFICATION_DIR / "aff_institution_aliases.json"
    return normalized_dict(json.loads(path.read_text(encoding="utf-8")))


def load_multimap(path: Path | None = None) -> dict[str, list[str]]:
    path = path or CLASSIFICATION_DIR / "aff_institution_multimap.json"
    return normalized_multimap(json.loads(path.read_text(encoding="utf-8")))


def canonicalize_affiliation(
    raw_affiliation: str,
    alias_map: dict[str, str],
    multimap: dict[str, list[str]],
) -> list[str]:
    normalized = normalize_affiliation_text(raw_affiliation)

    if normalized in multimap:
        return list(multimap[normalized])

    if normalized in alias_map:
        return [alias_map[normalized]]

    return [normalized]


def canonicalize_paper_affiliations(
    raw_affiliations: list[str],
    alias_map: dict[str, str],
    multimap: dict[str, list[str]],
) -> list[str]:
    canonical_institutions: set[str] = set()

    for raw_affiliation in raw_affiliations:
        for institution in canonicalize_affiliation(raw_affiliation, alias_map, multimap):
            canonical_institutions.add(institution)

    return sorted(canonical_institutions)
