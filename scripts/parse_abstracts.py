"""Parse abstracts and keywords from PaperPlaza saved HTML pages.

For each paper:
  - Find viewAbstract('N') to get the abstract DIV id
  - Locate <div id="AbN">…</div>
  - Inside: <strong>Keywords:</strong> followed by <a>...</a>, ... (text of anchors)
  - Followed by <strong>Abstract:</strong> {abstract text} until end of div
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from html import unescape

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "raw" / "program_html"
PAPERS_JSON = ROOT / "output" / "papers.json"
OUT = ROOT / "output" / "papers.json"  # overwrite

FILES = {
    "Tuesday":   DATA / "tuesday.html",
    "Wednesday": DATA / "wednesday.html",
    "Thursday":  DATA / "thursday.html",
}

# Match a paper-anchor block. The page uses code anchors like
#  <a name="TuI1I.1"></a> or similar before viewAbstract.
# Cleaner approach: find every viewAbstract id, walk back to find paper code
# and walk forward to find <div id="Ab{id}">.

PAPER_HEADER_RE = re.compile(
    r"""<a\s+name=["'][^"']+["'][^>]*>[^<]*Paper\s+([A-Z][a-z][A-Za-z0-9]+\.\d+)\s*</a>""",
    re.I,
)
VIEW_ABS_RE = re.compile(r"viewAbstract\(\s*(?:['\"]|&#39;|&quot;)(\d+)(?:['\"]|&#39;|&quot;)")
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
SOFT_HYPHEN_RE = re.compile(r"­")

def strip_tags(html: str) -> str:
    text = unescape(TAG_RE.sub(" ", html))
    # Remove control characters and soft hyphens that came from PDF source
    text = CTRL_RE.sub("", text)
    text = SOFT_HYPHEN_RE.sub("", text)
    return WS_RE.sub(" ", text).strip()


def parse_file(path: Path) -> dict[str, dict]:
    text = path.read_text(encoding="cp1252", errors="replace")

    # Find all paper code anchors with their positions
    anchors = [(m.group(1), m.start()) for m in PAPER_HEADER_RE.finditer(text)]
    print(f"  [{path.name}] anchors found: {len(anchors)}")
    # Debug: check first viewAbstract and Ab div presence
    va = re.search(VIEW_ABS_RE, text)
    print(f"  first viewAbstract: id={va.group(1) if va else None}")
    div_count = len(re.findall(r'<div id="Ab\d+"', text))
    print(f"  Ab div count: {div_count}")
    # Find all Ab divs by id -> (start, end)
    ab_divs = {}
    for m in re.finditer(r'<div id="Ab(\d+)"[^>]*>', text):
        ab_id = m.group(1)
        start = m.end()
        # Find matching </div> by scanning balanced divs
        depth = 1
        i = start
        while i < len(text) and depth > 0:
            n_open = text.find("<div", i)
            n_close = text.find("</div>", i)
            if n_close == -1:
                break
            if n_open != -1 and n_open < n_close:
                depth += 1
                i = n_open + 4
            else:
                depth -= 1
                i = n_close + 6
        ab_divs[ab_id] = (start, i - 6 if depth == 0 else i)

    # Walk anchors in order; for each, find the next viewAbstract before the next anchor
    out = {}
    for idx, (code, pos) in enumerate(anchors):
        next_pos = anchors[idx + 1][1] if idx + 1 < len(anchors) else len(text)
        seg = text[pos:next_pos]
        m = VIEW_ABS_RE.search(seg)
        if not m:
            continue
        ab_id = m.group(1)
        if ab_id not in ab_divs:
            continue
        a, b = ab_divs[ab_id]
        block = text[a:b]
        # Extract keyword anchor texts that precede "Abstract:"
        # Split on <strong>Abstract:</strong>
        parts = re.split(r"<strong>\s*Abstract\s*:\s*</strong>", block, maxsplit=1, flags=re.I)
        kw_part = parts[0]
        ab_part = parts[1] if len(parts) > 1 else ""
        keywords = []
        for am in re.finditer(r"<a [^>]*>(.*?)</a>", kw_part, re.DOTALL | re.I):
            kw = strip_tags(am.group(1))
            if kw and kw.lower() != "click to go to the keyword index":
                keywords.append(kw)
        abstract = strip_tags(ab_part)
        out[code] = {"keywords": keywords, "abstract": abstract, "ab_id": ab_id}
    return out


def main():
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    data = json.loads(PAPERS_JSON.read_text(encoding="utf-8"))
    papers = data["papers"]
    by_code = {p["code"]: p for p in papers}

    parsed = {}
    for day, fp in FILES.items():
        d = parse_file(fp)
        print(f"{day}: {len(d)} papers with abstracts (file: {fp.name})")
        # Print first key for debugging
        if d:
            sample = next(iter(d))
            print(f"  sample code: {sample}, kw count: {len(d[sample]['keywords'])}, abs len: {len(d[sample]['abstract'])}")
        parsed.update(d)

    matched = 0
    no_abs = 0
    for code, p in by_code.items():
        if code in parsed:
            p["keywords"] = parsed[code]["keywords"]
            p["abstract"] = parsed[code]["abstract"]
            matched += 1
        else:
            p["keywords"] = []
            p["abstract"] = ""
            no_abs += 1
    print(f"matched: {matched} / {len(by_code)}, missing: {no_abs}")

    # Sample (write to file to avoid console encoding crashes)
    sample_path = ROOT / "output" / "abstract_sample.txt"
    sample_path.parent.mkdir(parents=True, exist_ok=True)
    with sample_path.open("w", encoding="utf-8") as f:
        for p in papers[:5]:
            f.write(f"\n{p['code']} - {p['title']}\n")
            f.write(f"  keywords: {p['keywords']}\n")
            abst = p["abstract"][:300] + ("..." if len(p["abstract"]) > 300 else "")
            f.write(f"  abstract: {abst}\n")
    print(f"sample written to {sample_path}")

    OUT.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {OUT} ({OUT.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
