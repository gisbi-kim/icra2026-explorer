"""Smoke tests for the institution canonicalization layer."""
from __future__ import annotations

from institution_canonicalization import (
    canonicalize_affiliation,
    load_alias_map,
    load_multimap,
)


def main() -> None:
    aliases = load_alias_map()
    multimap = load_multimap()

    cases = {
        "ETH Zürich": ["ETH Zurich"],
        "ETH Zurich, Robotic Systems Lab": ["ETH Zurich"],
        "University of Zurich": ["University of Zurich"],
        "Bonn University": ["University of Bonn"],
        "University of Bonn": ["University of Bonn"],
        "Technical University of Munich (TUM)": ["Technical University of Munich"],
        "TUM": ["Technical University of Munich"],
        "Korea Advanced Institute of Science and Technology (KAIST)": ["KAIST"],
        "Daegu Gyeongbuk Institute of Science and Technology(DGIST)": ["DGIST"],
        "NASA-JPL, Caltech": ["NASA Jet Propulsion Laboratory", "Caltech"],
        "University of California, Berkeley": ["UC Berkeley"],
        "University of Michigan, Ann Arbor": ["University of Michigan"],
        "Washington University in St. Louis": ["Washington University in St. Louis"],
        "University of Washington": ["University of Washington"],
        "Shanghai Jiaotong University": ["Shanghai Jiao Tong University"],
        "ShangHai Jiao Tong University": ["Shanghai Jiao Tong University"],
        "Nankai University,": ["Nankai University"],
        "Institute of Automation，Chinese Academy of Sciences": ["CASIA"],
        "NanyangTechnological University": ["Nanyang Technological University"],
    }

    for raw, expected in cases.items():
        actual = canonicalize_affiliation(raw, aliases, multimap)
        assert actual == expected, f"{raw!r}: expected {expected!r}, got {actual!r}"

    false_pairs = [
        ("ETH Zurich", "University of Zurich"),
        ("University of Washington", "Washington University in St. Louis"),
        ("Queensland University of Technology", "The University of Queensland"),
        ("ShanghaiTech University", "Shanghai University"),
        ("Zhejiang University", "Zhejiang University of Technology"),
        ("CUHK", "CUHK Shenzhen"),
        ("HKUST", "HKUST Guangzhou"),
    ]
    for left, right in false_pairs:
        assert canonicalize_affiliation(left, aliases, multimap) != canonicalize_affiliation(
            right, aliases, multimap
        ), f"false merge detected: {left!r} == {right!r}"

    print(f"passed {len(cases)} positive cases and {len(false_pairs)} false-merge guards")


if __name__ == "__main__":
    main()
