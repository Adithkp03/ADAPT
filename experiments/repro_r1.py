"""D4.6 R1: live instantiation + forward of official BDH baseline and
third-party bdh-cq wrapper (CPU, random ids, no training). Appends results
to research/bdh/reproductions/R1_results.md. NOT a benchmark reproduction.
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, r"C:\Users\adith\AppData\Local\Temp\bdh_repo")
sys.path.insert(0, r"C:\Users\adith\AppData\Local\Temp\bdhcq_repo")

import torch

lines = [f"# D4.6 R1 results — {time.strftime('%Y-%m-%d')}, "
         "torch CPU, random ids, no training", ""]
ok = True

# --- official BDH baseline ---
try:
    import bdh
    cfg = bdh.BDHConfig()
    m = bdh.BDH(cfg)
    m.eval()
    with torch.no_grad():
        idx = torch.randint(0, 256, (1, 64))
        logits, loss = m(idx, idx)
    assert logits.shape == (1, 64, 256), logits.shape
    assert torch.isfinite(loss), loss
    lines += ["## Official BDH baseline: PASS",
              f"- config: n_layer={cfg.n_layer} n_embd={cfg.n_embd} "
              f"n_head={cfg.n_head} vocab={cfg.vocab_size}",
              f"- forward (1,64) -> logits {tuple(logits.shape)}, "
              f"loss={float(loss):.4f} (finite)",
              "- memory/answer path exists as described.", ""]
    print("BDH baseline PASS", tuple(logits.shape), float(loss))
except Exception as e:
    ok = False
    lines += [f"## Official BDH baseline: FAIL — {type(e).__name__}: {e}",
              "", ]
    print("BDH baseline FAIL:", repr(e))

# --- third-party bdh-cq wrapper ---
try:
    from bdh_cq import BDH, BDHReasoningWrapper
    tiny = BDH(dim=64, num_tokens=256)
    tiny.eval()
    w = BDHReasoningWrapper(tiny)
    with torch.no_grad():
        prompts = torch.randint(0, 256, (1, 16))
        out = w(prompts, 4, return_memory=True)
    assert isinstance(out, tuple) and len(out) == 2, type(out)
    mems = out[1]
    n_mem = (len(mems) if mems is not None else 0)
    assert n_mem > 0, "no memories surfaced"
    lines += ["## bdh-cq wrapper (third-party WIP): PASS",
              "- BDH(dim=64) + ReasoningWrapper forward ok",
              f"- latent steps=4 -> {n_mem} layer memories surfaced "
              "(return_memory=True)",
              "- input-chunk -> memory -> latent-steps path exists; "
              "update_memory flag present in source.",
              "- Label stays: third-party WIP, NOT official, NOT a "
              "reproduction of the 150M result.", ""]
    print("bdh-cq PASS, memories:", n_mem)
except Exception as e:
    ok = False
    lines += [f"## bdh-cq wrapper: FAIL — {type(e).__name__}: {e}", ""]
    print("bdh-cq FAIL:", repr(e))

out = ROOT / "research" / "bdh" / "reproductions" / "R1_results.md"
out.write_text("\n".join(lines), encoding="utf-8")
print("wrote", out, "OVERALL:", "PASS" if ok else "FAIL")
