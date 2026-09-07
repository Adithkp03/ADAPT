# D3.12 — Deployment (clean-environment reproduction)

## 1. Requirements

- Python 3.11+ with `numpy`, `pyyaml`, `matplotlib`, `pytest`
  (`requirements.txt`). No Node, no build step, no CDN, no network.
- Checkpoints ship in-repo (`checkpoints/*.npz`, learned trio s0).

## 2. End-to-end (clone → flagship), no developer intervention

```bash
git clone <repo> && cd <repo>
pip install -r requirements.txt
python server.py --port 8001
# open http://127.0.0.1:8001 in any modern browser
```

Then, without touching a terminal: flagship Run → N_D sweep → compare →
bottleneck/compute/noise sweeps → A→B→A → intervention → BDH quiz →
challenge deal + reveal → Lab run (try a Learned strategy) →
precomputed load → post-test → export session.

## 3. Offline verification

Disconnect network (or firewall-block the browser). Confirm: page + CSS +
JS load, live episode/compare/sweep run, precomputed + figures load, no
console error mentioning a remote host. There are no remote references in
`web/` (checked: `grep -rn "https\?://" web/` is empty); the server is
stdlib-only (`http.server`, no framework).

## 4. Mobile / accessibility smoke

- Widths: 360 / 390 / 430 / tablet / desktop. Single column ≤700px;
  tables scroll horizontally inside cards; buttons full-width ≤430px.
- Keyboard only: skip link → stages → prediction input → Run → drawers
  (`<details>` natively keyboard-operable) → sliders (arrow keys) →
  export. Visible `:focus-visible` outline throughout.
- Screen reader: stage headings, `aria-live="polite"` result regions,
  labeled sliders, chart data tables adjacent to every canvas,
  `prefers-reduced-motion` disables transitions.

## 5. API bounds (robustness)

Unknown family/strategy/perturbation/var → 400. Numerics clamped
(n_demos 1–16, noise 0–1, steps 0–64, lr 0–5, episodes ≤ 50, values ≤ 8,
seeds 0–999999). Bodies > 1 MiB rejected. Static handler confines reads
to `web/` (path-traversal guarded). Learned strategies default to vetted
in-repo checkpoints and reject non-linear families.

## 6. Tests

```bash
python -m pytest tests/ -q
```

Portable: the spawned-server fixture uses `sys.executable` — no
machine-specific paths. Live endpoint tests boot `server.py` on port 8123.
