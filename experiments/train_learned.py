"""Meta-train Phase 2B learned trio (numpy ES).

Train split -> ES updates; val split -> checkpoint selection; test
split -> final eval (never touched here). model_seed governs init +
ES sampling; task identity comes from task_seeds (separate RNG stream).

Usage: system-python experiments/train_learned.py [--steps 200] [--seeds 0,1]
Writes checkpoints/learned_{rec,ptt,ttt}_s<seed>.npz
"""
import argparse
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from adapt.tasks import generate_task
from adapt.learned import es_train

CKPT = Path(__file__).parent.parent / "checkpoints"
CKPT.mkdir(exist_ok=True)


def extra_queries(rule, rng, n=3):
    a, b = rule["a"], rule["b"]
    xs = rng.uniform(-5, 5, size=n)
    return [(float(x), float(a * x + b)) for x in xs]


def make_episode_fn(n_demos=4, split="train"):
    def fn(rng, n):
        eps = []
        for _ in range(n):
            ts = int(rng.randint(0, 10 ** 6))
            t = generate_task("linear", ts, n_demos=n_demos, noise=0.0, split=split)
            eps.append((t.demonstrations, extra_queries(t.hidden_rule, rng)))
        return eps
    return fn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=200)
    ap.add_argument("--seeds", default="0")
    ap.add_argument("--pop", type=int, default=40)
    ap.add_argument("--sigma", type=float, default=0.01)
    ap.add_argument("--meta-lr", type=float, default=0.1)
    ap.add_argument("--kinds", default="rec,ptt,ttt")
    args = ap.parse_args()
    rng = np.random.RandomState(999)
    val_eps = make_episode_fn()(rng, 32)
    # val episodes must come from VAL split:
    val_eps = make_episode_fn(split="val")(np.random.RandomState(1000), 32)
    for ms in [int(s) for s in args.seeds.split(",")]:
        for kind in args.kinds.split(","):
            print(f"=== training {kind} model_seed={ms} ===", flush=True)
            best = es_train(kind, make_episode_fn(split="train"), val_eps,
                            model_seed=ms, steps=args.steps, pop=args.pop,
                            sigma=args.sigma, meta_lr=args.meta_lr)
            out = CKPT / f"learned_{kind}_s{ms}.npz"
            np.savez(out, vec=best,
                     meta=dict(kind=kind, model_seed=ms, steps=args.steps))
            print(f"wrote {out}", flush=True)


if __name__ == "__main__":
    main()
