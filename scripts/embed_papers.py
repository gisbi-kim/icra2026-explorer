"""Compute SPECTER2 embeddings for every ICRA 2026 paper, then pre-compute the
top-K most similar papers per paper (cosine similarity).

Why pre-compute? At 2,964 papers × 768 dims × float32 = ~8.7 MB of raw
embeddings. Shipping just the top-10 lookup table is ~250 KB and means the
browser does zero ML work — only an O(1) dictionary lookup.

Why SPECTER2? It's trained on title+abstract pairs of academic papers,
specifically optimized for paper similarity. Generic embedders (MiniLM, BGE,
etc.) treat "manipulation" and "grasping" as semantically distant, while
SPECTER2 understands them as closely related robotics concepts.

Output:
  classification/similar_papers.json
    { "<paper_code>": [
        { "code": "<other_code>", "sim": 0.876 },
        ...  // top-K
      ], ... }

Usage:
  pip install transformers torch numpy
  python3 scripts/embed_papers.py            # full run, ~10-30 min on CPU
  python3 scripts/embed_papers.py --limit 50 # smoke test on first 50 papers
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS_JSON = ROOT / "output" / "papers.json"
OUT_JSON = ROOT / "classification" / "similar_papers.json"
EMB_NPY = ROOT / "classification" / "specter2_embeddings.npy"  # cache
CODES_JSON = ROOT / "classification" / "specter2_codes.json"   # parallel order

MODEL_NAME = "allenai/specter2_base"
TOP_K = 10
MAX_LEN = 512  # SPECTER2 input limit


def build_inputs(papers: list[dict], sep_token: str) -> list[str]:
    out = []
    for p in papers:
        title = (p.get("title") or "").strip()
        abstract = (p.get("abstract") or "").strip()
        # SPECTER2 expected input format: "<title>[SEP]<abstract>"
        out.append(title + sep_token + abstract if abstract else title)
    return out


def embed(papers: list[dict], batch_size: int = 8) -> "np.ndarray":
    import numpy as np
    import torch
    from transformers import AutoTokenizer, AutoModel

    print(f"Loading {MODEL_NAME} ...", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME)
    model.eval()
    device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"  device: {device}", flush=True)
    model.to(device)

    texts = build_inputs(papers, tokenizer.sep_token)

    all_emb = np.zeros((len(texts), model.config.hidden_size), dtype=np.float32)
    n_batches = (len(texts) + batch_size - 1) // batch_size
    with torch.no_grad():
        for bi, start in enumerate(range(0, len(texts), batch_size)):
            chunk = texts[start:start + batch_size]
            enc = tokenizer(chunk, padding=True, truncation=True,
                            return_tensors="pt", max_length=MAX_LEN).to(device)
            out = model(**enc)
            cls = out.last_hidden_state[:, 0, :]   # SPECTER2 uses CLS pooling
            all_emb[start:start + len(chunk)] = cls.cpu().numpy()
            if (bi + 1) % 10 == 0 or bi == n_batches - 1:
                print(f"  batch {bi+1}/{n_batches}  ({start + len(chunk)}/{len(texts)})", flush=True)
    # L2-normalize so dot-product == cosine similarity
    norms = np.linalg.norm(all_emb, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return all_emb / norms


def topk_similar(emb_norm, k: int = TOP_K):
    """For each row, return the indices and scores of the top-k most similar
    OTHER rows. Uses chunked matmul to avoid building the full N×N matrix in
    one go (saves memory at the cost of a few extra Python loops)."""
    import numpy as np
    n = emb_norm.shape[0]
    chunk = 256
    top_idx = np.zeros((n, k), dtype=np.int32)
    top_sim = np.zeros((n, k), dtype=np.float32)
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        for s in range(0, n, chunk):
            e_idx = min(s + chunk, n)
            sims = emb_norm[s:e_idx] @ emb_norm.T  # (chunk, n)
            # Mask self-similarity
            for i in range(e_idx - s):
                sims[i, s + i] = -2.0
            # argpartition is O(n) and gets us the top-k with no sort cost.
            part = np.argpartition(-sims, k, axis=1)[:, :k]
            # Then sort just those k.
            for i in range(e_idx - s):
                row = part[i]
                order = np.argsort(-sims[i, row])
                top_idx[s + i] = row[order]
                top_sim[s + i] = sims[i, row[order]]
    return top_idx, top_sim


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0,
                    help="Smoke test: only embed the first N papers")
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--reuse-cache", action="store_true",
                    help="Skip embedding if a cached .npy exists with matching paper codes")
    args = ap.parse_args()

    import numpy as np

    data = json.loads(PAPERS_JSON.read_text(encoding="utf-8"))
    papers = data["papers"]
    if args.limit:
        papers = papers[:args.limit]
    codes = [p["code"] for p in papers]
    print(f"papers to embed: {len(papers)}")

    if args.reuse_cache and EMB_NPY.exists() and CODES_JSON.exists():
        cached_codes = json.loads(CODES_JSON.read_text(encoding="utf-8"))
        if cached_codes == codes:
            print(f"reusing cached embeddings: {EMB_NPY}")
            emb_norm = np.load(EMB_NPY)
        else:
            print("cache code list mismatch, re-embedding")
            emb_norm = None
    else:
        emb_norm = None

    if emb_norm is None:
        emb_norm = embed(papers, batch_size=args.batch_size)
        EMB_NPY.parent.mkdir(parents=True, exist_ok=True)
        np.save(EMB_NPY, emb_norm)
        CODES_JSON.write_text(json.dumps(codes), encoding="utf-8")
        print(f"wrote {EMB_NPY} ({emb_norm.nbytes/1024/1024:.1f} MB)")

    print(f"computing top-{TOP_K} similar per paper ...", flush=True)
    top_idx, top_sim = topk_similar(emb_norm, k=TOP_K)

    out = {}
    for i, code in enumerate(codes):
        out[code] = [
            {"code": codes[int(j)], "sim": round(float(s), 4)}
            for j, s in zip(top_idx[i], top_sim[i])
        ]

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")),
                        encoding="utf-8")
    print(f"wrote {OUT_JSON} ({OUT_JSON.stat().st_size/1024:.1f} KB)")

    # Print a sanity sample
    print(f"\nsample — top similar to '{codes[0]}' ({papers[0]['title'][:80]}):")
    for hit in out[codes[0]][:5]:
        title = next((p["title"] for p in papers if p["code"] == hit["code"]), "?")
        print(f"  {hit['sim']:.4f}  {hit['code']}  {title[:90]}")


if __name__ == "__main__":
    main()
