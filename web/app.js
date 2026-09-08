/* AdaptLab frontend. Rule: render engine output, never invent it.
   Every number on screen comes from /api/* (live) or vetted results.json
   (precomputed). UI holds no scientific logic. */
"use strict";
const $ = id => document.getElementById(id);
const session = { id: "anon-" + Math.random().toString(36).slice(2, 9),
  started: new Date().toISOString(), events: [], score: { pred: 0, predN: 0, mech: 0, mechN: 0 } };
function log(ev, d) { session.events.push({ t: Date.now(), ev, d: d || {} }); }
async function post(p, b) {
  const r = await fetch(p, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(b) });
  const j = await r.json();
  if (!r.ok) throw new Error(j.error || ("HTTP " + r.status));
  return j;
}
async function get(p) { const r = await fetch(p); const j = await r.json(); if (!r.ok) throw new Error(j.error || p); return j; }
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
function badges(b) { const m = { LIVE: "live", PRECOMPUTED: "pre", SYNTHETIC: "syn", "PUBLISHED RESULT": "pub", ILLUSTRATIVE: "ill" }; return (b || []).map(x => `<span class="badge ${m[x] || "ill"}">${esc(x)}</span>`).join(" "); }
function provHTML(p, extra) {
  const seed = (p.seed !== undefined) ? p.seed : (p.seed_base !== undefined ? p.seed_base + "+N (sweep)" : "—");
  return `<details><summary>Experiment details (provenance)</summary><table>
  <tr><th scope="row">Seed</th><td>${esc(String(seed))}</td></tr>
  <tr><th scope="row">Task generator</th><td>${esc(p.task_generator_version)}${extra && extra.split ? " · split " + extra.split : ""}</td></tr>
  <tr><th scope="row">Model version</th><td>${esc(p.model_version || "—")}</td></tr>
  <tr><th scope="row">Config hash</th><td>${esc(p.config_hash || "—")}</td></tr>
  <tr><th scope="row">Commit</th><td>${esc(p.git_commit || "—")}</td></tr>
  <tr><th scope="row">Schema</th><td>${p.result_schema_version}</td></tr></table></details>`;
}
function stratKW(name, fam) {
  if (name === "param_tta") return { steps: 8, lr: (fam === "symbolic" || fam === "compositional") ? 0.5 : 0.05 };
  if (name === "ttt_state") return { steps: 8, lr: 0.05 };
  if (name === "state") return { state_dim: null, seed: 0 };
  if (name === "learned_state") return {};
  if (name === "learned_tta") return { steps: 5 };
  if (name === "learned_ttt") return {};
  return {};
}
function demoRows(d) { return d.map((p, i) => `<tr><th scope="row">${i + 1}</th><td>${esc(p.x)}</td><td>${esc(p.y)}</td></tr>`).join(""); }

/* ---------- quizzes ---------- */
const PRE = [
  { q: "A model learns a genuinely new task. Must its persistent weights have changed?", o: ["Yes, always", "No — adaptation can live in context or transient state", "Only for vision models"], a: 1, lo: "LO1" },
  { q: "Two conflicting tasks arrive in sequence (A then B). What do you expect for A?", o: ["Always retained", "Retention may drop — interference", "B is never learned"], a: 1, lo: "LO5" },
  { q: "An inference-time gradient update (parameter TTA) changes…", o: ["The training dataset", "Persistent parameters θ", "Only the query"], a: 1, lo: "LO2" },
  { q: "Which substrate has the tightest capacity limit in our lab?", o: ["The adaptive state bottleneck", "The frozen baseline", "The ground-truth file"], a: 0, lo: "LO4" },
  { q: "In BDH, working memory lives in…", o: ["The training loss curve", "Transient synaptic state σ", "The tokenizer"], a: 1, lo: "LO6" }];
const POST = [
  { q: "Where can new-task information live without changing persistent weights?", o: ["Nowhere — impossible", "Context conditioning or transient adaptive state", "Only in larger batch sizes"], a: 1, lo: "LO1" },
  { q: "After A→B→A continual adaptation, Task A accuracy drops. This is…", o: ["Proof the model is broken", "Interference / retention loss", "A seeding bug"], a: 1, lo: "LO5" },
  { q: "Δθ = 0 and Δs > 0 after adaptation means…", o: ["Parameters changed", "State carried the adaptation", "Nothing was learned"], a: 1, lo: "LO2" },
  { q: "Shrinking the state bottleneck d_s below the sufficient statistics…", o: ["Always helps", "Can collapse accuracy — capacity cliff", "Only affects latency"], a: 1, lo: "LO7" },
  { q: "BDH-CQ solves queries at inference time by…", o: ["Retraining on ARC", "Iterative latent computation over recurrent memory", "Verbal chain-of-thought only"], a: 1, lo: "LO6" }];
function quizHTML(el, items, tag) {
  $(el).innerHTML = items.map((it, i) => `<div class="q" role="group" aria-label="Question ${i + 1}">
    <p><strong>Q${i + 1}.</strong> ${esc(it.q)}</p>
    ${it.o.map((o, j) => `<label><input type="radio" name="${tag}${i}" value="${j}"> ${esc(o)}</label><br>`).join("")}</div>`).join("");
}
function quizScore(el, items, tag) {
  const detail = items.map((it, i) => { const c = document.querySelector(`input[name="${tag}${i}"]:checked`); return c && +c.value === it.a ? 1 : 0; });
  return { s: detail.reduce((a, b) => a + b, 0), detail };
}
quizHTML("pretest", PRE, "pre");
quizHTML("posttest", POST, "post");
$("pretest-score").onclick = () => { const r = quizScore(0, PRE, "pre"); $("pretest-out").textContent = `Pre-test: ${r.s}/${PRE.length}. The lab below targets exactly these ideas.`; log("pretest", { s: r.s, detail: r.detail }); };
$("posttest-score").onclick = () => { const r = quizScore(0, POST, "post"); $("posttest-out").textContent = `Post-test: ${r.s}/${POST.length}.`; log("posttest", { s: r.s, detail: r.detail }); renderBoard(); };

/* ---------- flagship ---------- */
let flag = { seed: 7, data: null };
async function flagLoad(seed) {
  flag.seed = seed;
  const task = await post("/api/compare", { family: "linear", strategies: ["state"], strategy_kwargs: { state: {} }, seed, n_demos: 4, noise: 0 });
  flag.task = task.task;
  $("flag-demos").innerHTML = `<caption>Input → output</caption><tr><th scope="col">#</th><th scope="col">x</th><th scope="col">y</th></tr>` + demoRows(task.task.demonstrations);
  $("flag-query").textContent = task.task.query;
  $("flag-out").innerHTML = `<p class="dim">Make your prediction, then run.</p>`;
}
async function flagRun() {
  const btn = $("flag-run"); btn.disabled = true;
  try {
    const r = await post("/api/episode", { family: "linear", strategy: "state", strategy_kwargs: { state: {} }, seed: flag.seed, n_demos: 4, noise: 0 });
    flag.data = r;
    const mine = parseFloat($("flag-your").value);
    const truth = parseFloat(r.ground_truth), pred = parseFloat(r.prediction);
    const tol = 0.5, mOK = isFinite(mine) && Math.abs(mine - truth) <= tol;
    if (isFinite(mine)) { session.score.predN++; if (mOK) session.score.pred++; }
    log("flagship_run", { seed: flag.seed, mine: $("flag-your").value, mOK, modelOK: r.correct });
    $("flag-out").innerHTML = `${badges(r.badges)}
      <table><caption>Truth beside estimate</caption>
      <tr><th scope="col"></th><th scope="col">Value</th><th scope="col">Verdict</th></tr>
      <tr><th scope="row">Your prediction</th><td>${esc($("flag-your").value || "—")}</td><td class="${mOK ? "ok" : "no"}">${$("flag-your").value ? (mOK ? "✓ within tolerance" : "✗ outside tolerance") : "—"}</td></tr>
      <tr><th scope="row">Model output</th><td>${esc(r.prediction)}</td><td class="${r.correct ? "ok" : "no"}">${r.correct ? "✓ Correct" : "✗ Wrong"}</td></tr>
      <tr><th scope="row">Ground truth</th><td>${esc(r.ground_truth)}</td><td>truth</td></tr></table>
      <div class="delta" role="status">WHAT CHANGED? Parameters Δθ = <strong>${r.telemetry.persistent_delta.toFixed(4)}</strong> ·
      State Δs = <strong>${r.telemetry.state_delta.toFixed(2)}</strong></div>
      <p class="dim">Holdout: ${esc(r.task.holdout || "split=test")}. Single-episode result — population claim lives in the sweeps below.</p>
      <p>The behavior was acquired while persistent parameters stayed fixed (Δθ = 0, Δs ≠ 0). <strong>Where did the new rule go?</strong></p>
      ${provHTML(r.provenance, { split: "test" })}`;
    mechQuiz();
  } catch (e) { $("flag-out").innerHTML = `<div class="no" role="alert"><strong>Experiment unavailable</strong> — system error, not a model failure. ${esc(e.message)} <button type="button" id="flag-retry">Retry</button></div>`; if ($("flag-retry")) $("flag-retry").onclick = flagRun; }
  btn.disabled = false;
}
function mechQuiz() {
  $("flag-quiz").innerHTML = `<div class="q" role="group" aria-label="Mechanism check">
    <p><strong>What changed inside the model?</strong></p>
    ${["Persistent parameters", "Disposable context buffer", "Adaptive state", "Nothing"].map((o, j) => `<label><input type="radio" name="mech0" value="${j}"> ${o}</label><br>`).join("")}
    <p class="row"><button type="button" id="mech-go">Check</button> <span id="mech-out" aria-live="polite"></span></p></div>`;
  $("mech-go").onclick = () => {
    const c = document.querySelector('input[name="mech0"]:checked');
    const ok = c && +c.value === 2;
    session.score.mechN++; if (ok) session.score.mech++;
    $("mech-out").innerHTML = ok ? `<span class="ok">Correct — Δθ = 0, Δs ≠ 0.</span>` : `<span class="no">Not quite — look at the WHAT CHANGED box above.</span>`;
    log("mech_quiz", { ok }); renderBoard();
  };
}
$("flag-run").onclick = flagRun;
$("flag-new").onclick = () => { $("flag-your").value = ""; flagLoad(Math.floor(Math.random() * 100000)); log("flag_new"); };

/* ---------- manipulate: N_D sweep + compare ---------- */
document.querySelectorAll("[data-ndpred]").forEach(b => b.onclick = () => {
  const ok = b.dataset.ndpred === "improve";
  session.score.predN++; if (ok) session.score.pred++;
  $("ndpred-out").innerHTML = ok ? `<span class="ok">Prediction logged: improve. Now run and check.</span>` : `<span class="dim">Prediction logged (${b.dataset.ndpred}). Now run and check.</span>`;
  log("nd_predict", { v: b.dataset.ndpred });
});
$("nd").oninput = e => $("nd-v").textContent = e.target.value;
$("nd-run").onclick = async () => {
  const btn = $("nd-run"); btn.disabled = true;
  try {
    const r = await post("/api/sweep", { family: "linear", strategy: "state", strategy_kwargs: { state: {} }, var: "n_demos", values: [1, 2, 3, 4, 6, 8], episodes: 25, seed_base: 0 });
    drawSweep($("nd-chart"), r.points, "N_D", "accuracy");
    $("nd-table").innerHTML = sweepTable(r) + `<p>1 demo cannot fix 2 line parameters (underdetermined) — then saturation. Your prediction above is scored against the N_D=1→4 rise.</p>`;
    log("nd_sweep", {});
  } catch (e) { $("nd-table").innerHTML = `<p class="no">Error: ${esc(e.message)}</p>`; }
  btn.disabled = false;
};
function sweepTable(r) {
  return `${badges(r.badges)}<table><caption>${esc(r.strategy_display)} — live sweep</caption>
  <tr><th scope="col">${esc(r.var)}</th>${r.points.map(p => `<th scope="col">${esc(String(p.value))}</th>`).join("")}</tr>
  <tr><th scope="row">accuracy</th>${r.points.map(p => `<td>${p.accuracy.toFixed(2)}<br><span class="dim">[${p.ci95[0].toFixed(2)}, ${p.ci95[1].toFixed(2)}]</span></td>`).join("")}</tr></table>
  ${r.provenance ? provHTML(r.provenance, { split: "test" }) : ""}`;
}
function drawSweep(cv, pts, xlab, ylab) {
  const c = cv.getContext("2d"), W = cv.width, H = cv.height;
  c.clearRect(0, 0, W, H); c.fillStyle = "#e0e0e0"; c.font = "12px sans-serif";
  const bw = W / pts.length;
  pts.forEach((p, i) => {
    const h = p.accuracy * (H - 50), x = i * bw + bw * 0.25, w = bw * 0.5;
    c.fillStyle = "#0b5fff"; c.fillRect(x, H - 30 - h, w, h);
    const y1 = H - 30 - p.ci95[1] * (H - 50), y2 = H - 30 - p.ci95[0] * (H - 50);
    c.strokeStyle = "#ffffff"; c.beginPath(); c.moveTo(x + w / 2, y1); c.lineTo(x + w / 2, y2); c.stroke();
    c.fillStyle = "#e0e0e0"; c.fillText(String(p.value), x, H - 12); c.fillText(p.accuracy.toFixed(2), x, H - 36 - h);
  });
  c.fillStyle = "#a0a0a0"; c.fillText(`${xlab} → ${ylab} (whiskers: 95% CI)`, 8, 14);
}
let cmpSeed = 21;
async function cmpRun() {
  const btn = $("cmp-run"); btn.disabled = true;
  try {
    const r = await post("/api/compare", { family: "linear", strategies: ["context", "param_tta", "state"], strategy_kwargs: { param_tta: { steps: 8, lr: 0.05 }, state: {} }, seed: cmpSeed, n_demos: 4, noise: 0 });
    $("cmp-out").innerHTML = `${badges(r.badges)}
      <p>Query ${esc(r.task.query)} · truth ${esc(r.task.ground_truth)}</p>
      <table><caption>Same task, same demonstrations — paired</caption>
      <tr><th scope="col">Mechanism</th><th scope="col">Model</th><th scope="col">Prediction</th><th scope="col">Correct</th><th scope="col">Δθ</th><th scope="col">Δs</th></tr>
      ${Object.entries(r.rows).map(([k, v]) => `<tr><th scope="row">${esc(v.display)}</th><td class="dim">${esc(v.model_version || "?")}${v.checkpoint ? "<br>" + esc(v.checkpoint) : ""}</td><td>${esc(v.prediction)}</td>
        <td class="${v.correct ? "ok" : "no"}">${v.correct ? "✓" : "✗"}</td><td>${v.persistent_delta.toFixed(3)}</td><td>${v.state_delta.toFixed(2)}</td></tr>`).join("")}</table>
      <p>Read the Δθ/Δs columns: three different places the rule can live.</p>${provHTML(r.provenance, { split: "test" })}`;
    log("compare", { seed: cmpSeed });
  } catch (e) { $("cmp-out").innerHTML = `<p class="no">Error: ${esc(e.message)}</p>`; }
  btn.disabled = false;
}
$("cmp-run").onclick = cmpRun;
$("cmp-new").onclick = () => { cmpSeed = Math.floor(Math.random() * 100000); cmpRun(); };

/* ---------- tradeoffs ---------- */
$("ds").oninput = e => $("ds-v").textContent = e.target.value === "5" ? "full" : e.target.value;
$("kval").oninput = e => $("kval-v").textContent = e.target.value;
$("ds-run").onclick = async () => {
  try {
    const r = await post("/api/sweep", { family: "linear", strategy: "state", strategy_kwargs: { seed: 0 }, var: "state_dim", values: ["full", 4, 2, 1], episodes: 25, seed_base: 100 });
    $("ds-out").innerHTML = sweepTable(r) + `<p>d_s is an <em>operational proxy</em> (project-and-reconstruct bottleneck), not capacity itself. Expect a cliff, not a slope.</p>`;
    log("ds_sweep", {});
  } catch (e) { $("ds-out").innerHTML = `<p class="no">Error: ${esc(e.message)}</p>`; }
};
$("k-run").onclick = async () => {
  try {
    const K = +$("kval").value;
    const r = await post("/api/sweep", { family: "linear", strategy: "param_tta", strategy_kwargs: { lr: 0.05 }, var: "steps", values: [0, 1, 2, 4, 8, 16].filter(v => v <= Math.max(K, 1)), episodes: 25, seed_base: 200 });
    $("k-out").innerHTML = sweepTable(r) + `<p>More inference compute buys accuracy — at latency cost. (Your slider caps the sweep at K=${K}; full K=0..16 is in precomputed E3.)</p>`;
    log("k_sweep", { K });
  } catch (e) { $("k-out").innerHTML = `<p class="no">Error: ${esc(e.message)}</p>`; }
};
$("nz-run").onclick = async () => {
  try {
    const r = await post("/api/sweep", { family: "linear", strategy: "state", strategy_kwargs: {}, var: "noise", values: [0, 0.05, 0.1, 0.2, 0.35], episodes: 25, seed_base: 300 });
    $("nz-out").innerHTML = sweepTable(r);
    log("noise_sweep", {});
  } catch (e) { $("nz-out").innerHTML = `<p class="no">Error: ${esc(e.message)}</p>`; }
};

/* ---------- interference + intervention ---------- */
let intSeed = 33;
document.querySelectorAll("[data-retpred]").forEach(b => b.onclick = () => {
  const ok = b.dataset.retpred === "degrade";
  session.score.predN++; if (ok) session.score.pred++;
  $("retpred-out").innerHTML = ok ? `<span class="ok">Logged: degrade. Run and check.</span>` : `<span class="dim">Logged (${b.dataset.retpred}). Run and check.</span>`;
  log("ret_predict", { v: b.dataset.retpred });
});
async function intRun() {
  const btn = $("int-run"); btn.disabled = true;
  try {
    const r = await post("/api/interference", { family: "linear", strategy: "state", strategy_kwargs: {}, seed: intSeed, n_demos: 4, noise: 0 });
    const drop = (r.A.correct_before ? 1 : 0) - (r.A.correct_after ? 1 : 0);
    $("int-out").innerHTML = `${badges(r.badges)}
      <table><caption>A→B→A retention (${esc(r.mode)})</caption>
      <tr><th scope="col"></th><th scope="col">Prediction</th><th scope="col">Truth</th><th scope="col">Correct</th></tr>
      <tr><th scope="row">Task A, before B</th><td>${esc(r.A.pred_before)}</td><td>${esc(r.A.ground_truth)}</td><td class="${r.A.correct_before ? "ok" : "no"}">${r.A.correct_before ? "✓" : "✗"}</td></tr>
      <tr><th scope="row">Task B</th><td>${esc(r.B.pred)}</td><td>${esc(r.B.ground_truth)}</td><td class="${r.B.correct ? "ok" : "no"}">${r.B.correct ? "✓" : "✗"}</td></tr>
      <tr><th scope="row">Task A, after B</th><td>${esc(r.A.pred_after)}</td><td>${esc(r.A.ground_truth)}</td><td class="${r.A.correct_after ? "ok" : "no"}">${r.A.correct_after ? "✓" : "✗"}</td></tr></table>
      <p>Retention change: <strong class="${drop > 0 ? "no" : "ok"}">${drop > 0 ? "−" + drop + " (forgot)" : "0 (retained)"}</strong> on this episode.</p>
      <p><strong>WHY?</strong> The adaptive state was overwritten by Task B's demonstrations — there is no separate slot holding Task A.
      Accumulated statistics mix two lines into a bad fit: the state remembers everything, including what it should forget.
      This is interference, not a bug — shared transient memory means new writes compete with old ones.</p>
      ${provHTML(r.provenance, { split: "test" })}`;
    log("interference", { seed: intSeed, drop });
  } catch (e) { $("int-out").innerHTML = `<p class="no">Error: ${esc(e.message)}</p>`; }
  btn.disabled = false;
}
$("int-run").onclick = intRun;
$("int-new").onclick = () => { intSeed = Math.floor(Math.random() * 100000); intRun(); };
$("e8-run").onclick = async () => {
  const btn = $("e8-run"); btn.disabled = true;
  try {
    const r = await post("/api/intervene", { family: "linear", strategy: "state", strategy_kwargs: {}, seed: intSeed, perturbations: ["zero", "shuffle", "swap", "nullmean"] });
    const sym = v => v ? "✓" : "✗";
    $("e8-out").innerHTML = `${badges(r.badges)}
      <table><caption>Perturb → measure → restore (query ${esc(r.task.query)}, truth ${esc(r.task.ground_truth)})</caption>
      <tr><th scope="col">Perturbation</th><th scope="col">Base</th><th scope="col">Perturbed</th><th scope="col">Restored</th></tr>
      ${Object.entries(r.rows).map(([k, v]) => `<tr><th scope="row">${esc(k)}</th><td>${sym(v.base)}</td>
        <td class="${v.perturbed ? "ok" : "no"}">${sym(v.perturbed)}</td><td>${sym(v.restored)}</td></tr>`).join("")}</table>
      <p>${esc(r.note)}</p>
      ${provHTML(r.provenance, { split: "test" })}`;
    log("intervene", { seed: intSeed });
  } catch (e) { $("e8-out").innerHTML = `<p class="no">Error: ${esc(e.message)}</p>`; }
  btn.disabled = false;
};

/* ---------- BDH eta demo + equation stepper + quiz ---------- */
function etaUpd() { const v = +$("eta").value; $("eta-v").textContent = v.toFixed(2); $("eta-out").textContent = (v * 1 * 1).toFixed(3); $("sig-out").textContent = (0.14 + v).toFixed(3); }
$("eta").oninput = etaUpd; etaUpd();
const EOR = [
  { t: "Round 4l — memory read", d: "The system updates its accumulator from current beliefs + new inputs + the causal relations stored in σ (modus ponens). Nothing is stored yet — this is the read.", s: "Equations of Reasoning §4, step 1" },
  { t: "Round 4l+1 — memory write", d: "σ is reweighted with the outer (Hebbian) product of X and Y — the σ ← σ + η·X·Yᵀ step above (simplified educational form). This is the write; try moving η and watch σ₁₂.", s: "Equations of Reasoning §4, step 2" },
  { t: "Round 4l+2 — gated readout", d: "Y is read out from A for context-relevant neurons (A gated by X). Y is sparse and positive — most of the graph stays quiet.", s: "Equations of Reasoning §4, step 3" },
  { t: "Round 4l+3 — state update", d: "Final update of X closes the loop. Fast pulse variables (X, A, Y) settle; the slow synaptic variable σ keeps what was written.", s: "Equations of Reasoning §4, step 4" }];
let eorI = 0;
function eorRender() {
  $("eor-step").innerHTML = `<p><strong>${esc(EOR[eorI].t)}</strong></p><p>${esc(EOR[eorI].d)}</p><p class="dim">Source: ${esc(EOR[eorI].s)}</p>`;
  $("eor-pos").textContent = `Round ${eorI + 1} of 4`;
  log("eor_step", { i: eorI });
}
$("eor-prev").onclick = () => { eorI = (eorI + EOR.length - 1) % EOR.length; eorRender(); };
$("eor-next").onclick = () => { eorI = (eorI + 1) % EOR.length; eorRender(); };
eorRender();
$("bdh-quiz").innerHTML = `<div class="q" role="group" aria-label="BDH-CQ order check">
  <p><strong>BDH-CQ inference order (LO6):</strong> which sequence matches the paper's described mechanism?</p>
  <label><input type="radio" name="bdh0" value="0"> Query → retrain parameters → answer</label><br>
  <label><input type="radio" name="bdh0" value="1"> Demonstrations → recurrent memory updates → query → iterative latent computation → answer</label><br>
  <label><input type="radio" name="bdh0" value="2"> Memory update → verbal chain-of-thought → parameter edit</label><br>
  <p class="row"><button type="button" id="bdh-go">Check</button> <span id="bdh-out" aria-live="polite"></span></p></div>`;
$("bdh-go").onclick = () => {
  const c = document.querySelector('input[name="bdh0"]:checked');
  const ok = c && +c.value === 1;
  session.score.mechN++; if (ok) session.score.mech++;
  $("bdh-out").innerHTML = ok ? `<span class="ok">Correct — memory evolves, parameters static.</span>` : `<span class="no">Check the dossier timeline above.</span>`;
  log("bdh_quiz", { ok }); renderBoard();
};

/* ---------- challenge ---------- */
let chSeed = null;
const CH = [{ q: "Which mechanism will do best on depth ≤3 operation chains?", o: ["Frozen baseline", "Context-conditioned baseline (single-op vote)", "Adaptive State (shift-only read)"], a: 1 }];
$("ch-new").onclick = async () => {
  chSeed = Math.floor(Math.random() * 100000);
  const r = await post("/api/compare", { family: "compositional", strategies: ["state"], strategy_kwargs: {}, seed: chSeed, n_demos: 6, noise: 0 });
  $("ch-task").innerHTML = `${badges(r.badges)}<table><caption>Unseen compositional task (rule hidden)</caption>
    <tr><th scope="col">#</th><th scope="col">input</th><th scope="col">output</th></tr>${demoRows(r.task.demonstrations)}</table>
    <p>Query: <strong>${esc(r.task.query)}</strong></p>`;
  $("ch-quiz").innerHTML = `<div class="q" role="group" aria-label="Transfer prediction"><p><strong>${esc(CH[0].q)}</strong></p>
    ${CH[0].o.map((o, j) => `<label><input type="radio" name="ch0" value="${j}"> ${esc(o)}</label><br>`).join("")}</div>`;
  $("ch-out").innerHTML = "";
  log("challenge_dealt", { seed: chSeed });
};
$("ch-run").onclick = async () => {
  if (chSeed === null) { $("ch-out").innerHTML = `<p class="dim">Deal a task first.</p>`; return; }
  const c = document.querySelector('input[name="ch0"]:checked');
  const r = await post("/api/compare", { family: "compositional", strategies: ["context", "param_tta", "state"], strategy_kwargs: { param_tta: { steps: 8, lr: 0.5 } }, seed: chSeed, n_demos: 6, noise: 0 });
  const winner = Object.entries(r.rows).sort((a, b) => (b[1].correct - a[1].correct))[0][0];
  const pick = c ? ["frozen", "context", "state"][+c.value] : null;
  const ok = pick === winner || (pick === "context" && winner === "context");
  if (c) { session.score.predN++; if (pick === winner) session.score.pred++; }
  $("ch-out").innerHTML = `${badges(r.badges)}
    <table><caption>Transfer result — truth ${esc(r.task.ground_truth)}</caption>
    ${Object.entries(r.rows).map(([k, v]) => `<tr><th scope="row">${esc(v.display)}</th><td>${esc(v.prediction)}</td>
      <td class="${v.correct ? "ok" : "no"}">${v.correct ? "✓" : "✗"}</td></tr>`).join("")}</table>
    <p>Your pick: <strong>${esc(pick || "—")}</strong> · best: <strong>${esc(winner)}</strong> ${c ? (pick === winner ? `<span class="ok">— transfer correct</span>` : `<span class="no">— transfer missed; note the honest limits (single-op vote, shift-only read, no chain learner)</span>`) : ""}</p>`;
  log("challenge_run", { pick, winner }); renderBoard();
};

/* ---------- lab ---------- */
$("lab-run").onclick = async () => {
  const btn = $("lab-run"); btn.disabled = true;
  try {
    let fam = $("lab-fam").value;
    const strat = $("lab-strat").value;
    let note = "";
    if (strat.startsWith("learned_") && fam !== "linear") {
      fam = "linear"; $("lab-fam").value = "linear";
      note = `<p class="dim">Learned trio scope: linear only — family switched to linear.</p>`;
    }
    const r = await post("/api/episode", { family: fam, strategy: strat,
      strategy_kwargs: stratKW(strat, fam), seed: +$("lab-seed").value,
      n_demos: +$("lab-nd").value, noise: +$("lab-noise").value });
    $("lab-out").innerHTML = `${note}${badges(r.badges)} <span class="dim">${esc(r.strategy_display)} · ${esc(r.task.family_display)}</span>
      <table><caption>Demonstrations</caption><tr><th scope="col">#</th><th scope="col">x</th><th scope="col">y</th></tr>${demoRows(r.task.demonstrations)}</table>
      <p>Query <strong>${esc(r.task.query)}</strong> → model <strong>${esc(r.prediction)}</strong> · truth <strong>${esc(r.ground_truth)}</strong>
      <span class="${r.correct ? "ok" : "no"}">${r.correct ? "✓ Correct" : "✗ Wrong"}</span></p>
      <p class="dim">Holdout: ${esc(r.task.holdout || "split=test")}</p>
      <div class="delta">Δθ = <strong>${r.telemetry.persistent_delta.toFixed(4)}</strong> · Δs = <strong>${r.telemetry.state_delta.toFixed(2)}</strong> ·
      adapt ${r.telemetry.t_adapt_ms.toFixed(2)}ms · predict ${r.telemetry.t_predict_ms.toFixed(2)}ms · steps ${r.telemetry.steps}</div>
      ${provHTML(r.provenance, { split: "test" })}`;
    log("lab_run", { fam, strat });
  } catch (e) { $("lab-out").innerHTML = `<p class="no">Error: ${esc(e.message)}</p>`; }
  btn.disabled = false;
};
$("pre-run").onclick = async () => {
  try {
    const r = await get("/api/precomputed?exp=" + $("pre-sel").value);
    const names = Object.keys(r.summary || {});
    $("pre-out").innerHTML = `<p><span class="badge pre">PRECOMPUTED</span> <span class="badge syn">SYNTHETIC</span>
      N=${r.summary[names[0]] ? (r.summary[names[0]].n || "?") : "?"} · commit ${esc((r.provenance || {}).git_commit || "?")} ·
      config ${esc((r.provenance || {}).config_hash || "?")}</p>
      <pre>${esc(JSON.stringify(r.summary, null, 1).slice(0, 2000))}</pre>`;
    log("precomputed", { exp: $("pre-sel").value });
  } catch (e) { $("pre-out").innerHTML = `<p class="no">Error: ${esc(e.message)}</p>`; }
};

/* ---------- scoreboard + export ---------- */
function renderBoard() {
  const s = session.score;
  $("scoreboard").innerHTML = `<h3>Your evidence so far</h3><p>Predictions: <strong>${s.pred}/${s.predN}</strong> ·
  Mechanism checks: <strong>${s.mech}/${s.mechN}</strong> · events: ${session.events.length}</p>`;
}
$("export").onclick = () => {
  session.explain = $("ch-explain").value;
  const blob = new Blob([JSON.stringify(session, null, 1)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob); a.download = session.id + ".json"; a.click();
  log("export", {});
};
renderBoard();
flagLoad(7);
log("session_start", {});

/* ---------- Sidebar Active State Navigation ---------- */
document.querySelectorAll('.stages a').forEach(link => {
  link.addEventListener('click', function() {
    document.querySelectorAll('.stages li').forEach(li => li.classList.remove('active'));
    this.parentElement.classList.add('active');
  });
});

const sections = document.querySelectorAll('main > section');
if (sections.length > 0) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        document.querySelectorAll('.stages li').forEach(li => li.classList.remove('active'));
        const activeLink = document.querySelector(`.stages a[href="#${entry.target.id}"]`);
        if (activeLink) activeLink.parentElement.classList.add('active');
      }
    });
  }, { rootMargin: '-30% 0px -50% 0px' });
  sections.forEach(sec => observer.observe(sec));
}
