# ICRA 2026 Paper Explorer

> 🌐 **Live demo:** <https://gisbi-kim.github.io/icra2026-explorer/>

ICRA 2026 프로그램(2026-06-02 ~ 06-04, 2,964개 논문)을 파싱해서 단일 HTML 파일로
탐색·필터링·시각화할 수 있게 만든 파이프라인입니다.

브라우저에서 바로 보기는 위 라이브 링크, 오프라인으로 보고 싶으면
[`output/icra2026_explorer.html`](output/icra2026_explorer.html) — JS/CSS/데이터까지 전부
인라인된 self-contained 파일이라 더블클릭해서 열면 됩니다.

## What's inside

| 항목 | 수치 |
|---|---|
| Papers | 2,964 (Tue 991 / Wed 992 / Thu 981) |
| Unique affiliations | 2,690 |
| Top countries | China 758 · USA 437 · Germany 211 · South Korea 175 · France 133 · Italy 119 · Japan 100 · UK 86 |

탐색기 안에서 가능한 것:
- 키워드 / 저자 / 소속 / 국가 / 세션 / 일자별 필터
- 논문별 abstract + keywords (PaperPlaza에서 추출)
- 국가별 / 토픽별 통계 차트

## Pipeline

```
raw/paper_titles/{tue,wed,thu}.txt        ─┐
                                            ├─► scripts/parse_papers.py        ─► output/papers.json
                                            │
raw/program_html/{tuesday,...}.html        ─┴─► scripts/parse_abstracts.py    ─► output/papers.json (+abstract,keywords)
                                            
output/papers.json                         ───► scripts/dump_affiliations.py  ─► classification/affiliations_classified.json
                                                                                  (휴리스틱 국가 분류 + Other 후보)

classification/fullaff_*_classified.json   ───► scripts/merge_classifications.py ─► classification/aff_country_table.json
       (LLM이 분류한 5개 청크, 권위 테이블의 원천)

output/papers.json + classification/*      ───► scripts/build_html.py         ─► output/icra2026_explorer.html
```

## Usage

```bash
# 처음부터 다 빌드 (Python 3.10+, 표준 라이브러리만 사용)
python3 scripts/parse_papers.py        # 1) titles → papers.json
python3 scripts/parse_abstracts.py     # 2) HTML 에서 abstract+keywords 머지
python3 scripts/dump_affiliations.py   # 3) 소속 덤프 + 휴리스틱 분류
python3 scripts/merge_classifications.py  # 4) LLM 분류 5청크 → aff_country_table.json
python3 scripts/build_html.py          # 5) 최종 HTML 생성

# 그냥 결과만 보기
open output/icra2026_explorer.html
```

`scripts/parse_papers.py` 와 `scripts/dump_affiliations.py` 안에는 도시·기관·기업명을 기반으로 한
국가 추정 휴리스틱(`COUNTRY_HINTS`)이 들어 있습니다. LLM이 분류한 `aff_country_table.json` 이
권위 테이블이고, 휴리스틱은 fallback 입니다.

## Layout

```
.
├── scripts/             # 5단계 파이프라인 전부
├── raw/
│   ├── paper_titles/    # PaperPlaza 일정표 텍스트 덤프 (3개)
│   └── program_html/    # PaperPlaza Program 페이지 저장본 (3개, abstract 추출용)
├── classification/      # LLM이 분류한 affiliation → country 테이블 + 작업물
└── output/
    ├── papers.json              # 구조화된 논문 데이터
    └── icra2026_explorer.html   # 🎯 최종 산출물
```

## Data sources

- 일정표 텍스트: <https://ras.papercept.net/conferences/conferences/ICRA26/program/>
- Abstract / keywords: 각 일자별 Program HTML 페이지를 저장해서 파싱

## Notes

- 홍콩/마카오 소속은 자료 일관성을 위해 China로 폴딩되어 있습니다 (`merge_classifications.py` /
  `build_html.py` 양쪽에서 처리).
- 휴리스틱만으로는 22% 정도 논문이 "Other"로 빠집니다. 그래서 LLM 분류 단계가 추가되었고
  실제 탐색기에서는 LLM 테이블이 우선 적용됩니다.
