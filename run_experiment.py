"""CLI: system-python run_experiment.py experiments/configs/exp_001.yaml [--out ...]"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import yaml
from adapt.runner import run_with_protocol as run


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config))
    res = run(cfg)
    s = json.dumps(res, indent=2, default=str)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        open(args.out, "w").write(s)
        print(f"wrote {args.out}")
    else:
        print(s)
    # one-line human summary (protocol-aware)
    for name, m in res["summary"].items():
        if "accuracy" in m:
            print(f"{name}: acc={m['accuracy']:.3f} "
                  f"[{m['ci95'][0]:.3f},{m['ci95'][1]:.3f}] "
                  f"dTheta={m['mean_persistent_delta']:.4f} "
                  f"dS={m['mean_state_delta']:.4f}")
        elif "retention_A" in m:
            print(f"{name}: A0={m['acc_A_initial']:.3f} "
                  f"B={m['acc_B']:.3f} retA={m['retention_A']:.3f} "
                  f"drop={m['retention_drop']:+.3f}")
        else:  # intervention
            for p, r in m.items():
                print(f"{name}/{p}: base={r['acc_base']:.3f} "
                      f"pert={r['acc_perturbed']:.3f} "
                      f"restored={r['acc_restored']:.3f} "
                      f"drop={r['drop']:+.3f}")


if __name__ == "__main__":
    main()
