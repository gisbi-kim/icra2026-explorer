"""Smoke tests for the institution canonicalization layer."""
from __future__ import annotations

from institution_canonicalization import (
    canonicalize_affiliation,
    infer_country_for_institution,
    load_alias_map,
    load_institution_country_table,
    load_multimap,
    load_parent_org,
    load_site_country_overrides,
)


def main() -> None:
    aliases = load_alias_map()
    multimap = load_multimap()
    site_country = load_site_country_overrides()
    institution_country = load_institution_country_table()
    parent_org = load_parent_org()

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
        "Huawei Noah's Ark Lab": ["Noah's Ark Lab"],
        "Noah's Ark Lab, Huawei Technologies": ["Noah's Ark Lab"],
        "Huawei Technologies Canada": ["Huawei Technologies Canada"],
        "Huawei Technologies": ["Huawei"],
        "Bosch China": ["Bosch China"],
        "Bosch Center for Artificial Intelligence": ["Bosch Center for Artificial Intelligence"],
        "Honda Research Institute Europe": ["Honda Research Institute Europe"],
        "Honda Research Institute, USA": ["Honda Research Institute USA"],
        "Toyota Motor East Japan, Inc": ["Toyota Motor East Japan"],
        "Toyota Motor North America, InfoTech Labs": ["Toyota Motor North America R&D"],
        "Samsung Research America": ["Samsung Research America"],
        "GeorgiaTech Lorraine": ["Georgia Tech Europe"],
        "Mitsubishi Electric Research Laboratories": ["MERL"],
        "PICO, ByteDance": ["PICO"],
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

    country_cases = {
        "Huawei Noah's Ark Lab": ("Noah's Ark Lab", "Canada", "Huawei"),
        "Noah's Ark Lab, Huawei Technologies": ("Noah's Ark Lab", "Canada", "Huawei"),
        "Huawei Technologies Canada": ("Huawei Technologies Canada", "Canada", "Huawei"),
        "Huawei Technologies": ("Huawei", "China", None),
        "Bosch China": ("Bosch China", "China", "Bosch"),
        "Bosch Center for Artificial Intelligence": (
            "Bosch Center for Artificial Intelligence",
            "Germany",
            "Bosch",
        ),
        "Honda Research Institute Europe": ("Honda Research Institute Europe", "Germany", "Honda"),
        "Honda Research Institute USA": ("Honda Research Institute USA", "USA", "Honda"),
        "Toyota Research Institute": ("Toyota Research Institute", "USA", "Toyota"),
        "Toyota Motor Corporation": ("Toyota Motor Corporation", "Japan", None),
        "Samsung Research America": ("Samsung Research America", "USA", "Samsung"),
        "Georgia Tech Europe - IRL 2958 GT-CNRS": ("Georgia Tech Europe", "France", "Georgia Tech"),
        "Mitsubishi Electric Research Laboratories": ("MERL", "USA", "Mitsubishi Electric"),
    }
    for raw, (canonical, expected_country, expected_parent) in country_cases.items():
        actual_canonical = canonicalize_affiliation(raw, aliases, multimap)[0]
        assert actual_canonical == canonical, f"{raw!r}: expected canonical {canonical!r}, got {actual_canonical!r}"
        actual_country = infer_country_for_institution(
            raw,
            actual_canonical,
            site_country,
            institution_country,
            parent_org,
        )
        assert actual_country == expected_country, f"{raw!r}: expected country {expected_country!r}, got {actual_country!r}"
        actual_parent = parent_org.get(actual_canonical, {}).get("parent_org")
        assert actual_parent == expected_parent, f"{raw!r}: expected parent {expected_parent!r}, got {actual_parent!r}"

    print(
        f"passed {len(cases)} positive cases, {len(false_pairs)} false-merge guards, "
        f"and {len(country_cases)} site-aware country cases"
    )


if __name__ == "__main__":
    main()
