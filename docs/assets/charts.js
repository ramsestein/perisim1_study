// Figures of "Update before you build", drawn from docs/data/study.json (built by site/build_data.py).
(() => {
  const NS = "http://www.w3.org/2000/svg";
  const OUT_ORDER = ["hypo", "t2", "O1", "O2"];
  const OUT_SHORT = { hypo: "Hypotension", t2: "Stay after ICU (T2)", O1: "Vasopressor start (O1)", O2: "ICU discharge 24 h (O2)" };
  const SIZES = [250, 500, 1000, 2000, 4000, 8000];
  const OPT = { adopt: "Adopt (recalibrate)", update: "Update", own: "Build own" };
  const OPT_COLOR = { adopt: "var(--adopt)", update: "var(--update)", own: "var(--own)" };
  const fmtN = n => Number(n).toLocaleString("en-US");
  const fmt = (v, d = 4) => (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v).toFixed(d);

  function el(tag, attrs = {}, parent) {
    const e = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "style") Object.assign(e.style, v); else if (k === "text") e.textContent = v; else e.setAttribute(k, v);
    }
    if (parent) parent.appendChild(e);
    return e;
  }
  const tip = document.createElement("div");
  tip.className = "tip";
  document.body.appendChild(tip);
  function hover(node, html) {
    node.addEventListener("mousemove", ev => {
      tip.innerHTML = html; tip.style.opacity = 1;
      const x = Math.min(ev.clientX + 14, window.innerWidth - 300);
      tip.style.left = x + "px"; tip.style.top = (ev.clientY + 14) + "px";
    });
    node.addEventListener("mouseleave", () => { tip.style.opacity = 0; });
    node.style.cursor = "default";
  }
  const label = u => {
    if (u.destination === "NWICU" && u.outcome !== "O1") return `NWICU ← ${u.source}`;
    return u.destination;
  };
  const byOutcome = units => OUT_ORDER.map(o => [o, units.filter(u => u.outcome === o)]);
  const best = ll => Object.keys(OPT).reduce((a, b) => (ll[b] < ll[a] ? b : a));
  const statusTag = u => (u.status === "confirmatory" ? "pre-registered" : "exploratory");

  // ------------------------------------------------------------------ Figure 2: which option wins
  function decisionMap(root, units) {
    const rowH = 26, left = 238, top = 34, cw = 92;
    const groups = byOutcome(units);
    const rows = groups.reduce((s, [, us]) => s + us.length + 1, 0);
    const W = left + cw * SIZES.length + 10, H = top + rows * rowH + 10;
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Winning option by unit and number of local patients" }, root);
    SIZES.forEach((n, j) => el("text", { x: left + j * cw + cw / 2, y: 20, "text-anchor": "middle", "font-size": 12, style: { fill: "var(--ink-2)" }, text: fmtN(n) }, svg));
    let y = top;
    for (const [o, us] of groups) {
      el("text", { x: 0, y: y + 17, "font-size": 12.5, "font-weight": 700, style: { fill: "var(--ink)" }, text: OUT_SHORT[o] + (us[0].status === "confirmatory" ? "  · pre-registered" : "") }, svg);
      y += rowH;
      for (const u of us) {
        el("text", { x: 12, y: y + 17, "font-size": 12, style: { fill: "var(--ink-2)" }, text: label(u) }, svg);
        if (u.regime === "relation") el("circle", { cx: left - 14, cy: y + 13, r: 4, style: { fill: "var(--accent)" } }, svg);
        SIZES.forEach((n, j) => {
          const c = u.by_n[String(n)];
          const x = left + j * cw;
          if (!c) { el("rect", { x: x + 2, y: y + 2, width: cw - 4, height: rowH - 4, rx: 4, style: { fill: "none", stroke: "var(--grid)" } }, svg); return; }
          const ll = c.logloss, w = best(ll);
          const vals = Object.keys(OPT).map(k => ll[k]).sort((a, b) => a - b);
          const margin = vals[1] - vals[0];
          const op = 0.28 + 0.72 * Math.min(1, margin / 0.01);
          const r = el("rect", { x: x + 2, y: y + 2, width: cw - 4, height: rowH - 4, rx: 4, style: { fill: OPT_COLOR[w], fillOpacity: op } }, svg);
          el("text", { x: x + cw / 2, y: y + 17, "text-anchor": "middle", "font-size": 11, "font-weight": 600, style: { fill: op > 0.6 ? "#fff" : "var(--ink)", pointerEvents: "none" }, text: w === "adopt" ? "adopt" : w === "update" ? "update" : "own" }, svg);
          hover(r, `<b>${OUT_SHORT[o]} · ${label(u)}</b><br>${fmtN(n)} local patients (${statusTag(u)})<br>` +
            Object.keys(OPT).map(k => `${OPT[k]}: ${ll[k].toFixed(4)} nats${k === w ? " ← best" : ""}`).join("<br>") +
            `<br>Margin over runner-up: ${margin.toFixed(4)} nats`);
        });
        y += rowH;
      }
    }
  }

  // ------------------------------------------------------------------ Figure 3: build minus update
  function buildVsUpdate(root, units) {
    const narrow = root.clientWidth < 620;
    const cols = narrow ? 1 : 2, pw = narrow ? 300 : 300, ph = 170, gx = 70, gy = 40, sx = pw + 110, sy = ph + 80;
    const groups = byOutcome(units);
    const W = gx + cols * sx - 20, H = gy + Math.ceil(groups.length / cols) * sy;
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Log-loss of the own model minus the updated external model, by size" }, root);
    const lx = n => Math.log2(n / 250) / 5 * pw;
    const lim = 0.032, ly = v => ph / 2 - Math.max(-lim, Math.min(lim, v)) / lim * (ph / 2);
    groups.forEach(([o, us], i) => {
      const g = el("g", { transform: `translate(${gx + (i % cols) * sx},${gy + Math.floor(i / cols) * sy})` }, svg);
      el("text", { x: 0, y: -14, "font-size": 13, "font-weight": 700, style: { fill: "var(--ink)" }, text: OUT_SHORT[o] + (us[0].status === "confirmatory" ? " · pre-registered" : "") }, g);
      [-0.02, -0.01, 0.01, 0.02].forEach(v => el("line", { x1: 0, x2: pw, y1: ly(v), y2: ly(v), style: { stroke: "var(--grid)" } }, g));
      el("line", { x1: 0, x2: pw, y1: ly(0), y2: ly(0), style: { stroke: "var(--axis)" } }, g);
      [-0.02, 0, 0.02].forEach(v => el("text", { x: -6, y: ly(v) + 4, "text-anchor": "end", "font-size": 11, style: { fill: "var(--ink-3)" }, text: v === 0 ? "0" : fmt(v, 2) }, g));
      SIZES.forEach(n => el("text", { x: lx(n), y: ph + 16, "text-anchor": "middle", "font-size": 11, style: { fill: "var(--ink-3)" }, text: n >= 1000 ? n / 1000 + "k" : n }, g));
      const ordered = [...us].sort((a, b) => (a.regime === "relation") - (b.regime === "relation"));
      for (const u of ordered) {
        const S = Object.entries(u.by_n).map(([n, c]) => ({ n: +n, d: c.own_minus_update, w: c.own_beats_update_share }));
        const rel = u.regime === "relation", col = rel ? "var(--accent)" : "var(--level)";
        el("path", { d: S.map((p, k) => `${k ? "L" : "M"}${lx(p.n)},${ly(p.d)}`).join(" "), style: { fill: "none", stroke: col, strokeWidth: rel ? 2.2 : 1.3, strokeOpacity: rel ? 1 : 0.75 } }, g);
        for (const p of S) {
          const c = el("circle", { cx: lx(p.n), cy: ly(p.d), r: 3.6, style: { fill: col, fillOpacity: p.w >= 0.8 ? 1 : 0, stroke: col, strokeWidth: 1.3 } }, g);
          hover(c, `<b>${OUT_SHORT[o]} · ${label(u)}</b><br>${fmtN(p.n)} patients · ${rel ? "relation shift" : "level shift"}<br>Own − update: ${fmt(p.d)} nats<br>Own model wins in ${Math.round(p.w * 100)}% of simulated hospitals`);
        }
        if (rel) { const last = S[S.length - 1]; el("text", { x: pw + 6, y: ly(last.d) + 4, "font-size": 11, style: { fill: "var(--accent)" }, text: label(u) }, g); }
      }
    });
  }

  // ------------------------------------------------------------------ Figure 4: choosing from the hospital's own sample
  function regretPlot(root, units, which) {
    root.innerHTML = "";
    const P = which === "confirmatory"
      ? [["cv", "Cross-validation", "var(--update)"], ["closed", "Closed test", "var(--own)"], ["rule_v1", "Rule v1", "var(--level)"], ["rule_v2", "Rule v2", "var(--ink-2)"]]
      : [["cv", "Cross-validation", "var(--update)"], ["closed", "Closed test", "var(--own)"], ["rule_v1", "Rule v1", "var(--level)"]];
    const us = units.filter(u => (which === "confirmatory") === (u.status === "confirmatory"));
    const rowH = 28, left = 320, top = 30, pw = 460, xmax = 0.036;
    const W = left + pw + 30, H = top + us.length * rowH + 36;
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Mean regret of each choice procedure with 1,000 or more local patients" }, root);
    const x = v => left + Math.max(0, Math.min(xmax, v)) / xmax * pw;
    [0, 0.01, 0.02, 0.03].forEach(v => {
      el("line", { x1: x(v), x2: x(v), y1: top - 6, y2: H - 30, style: { stroke: "var(--grid)" } }, svg);
      el("text", { x: x(v), y: H - 12, "text-anchor": "middle", "font-size": 11, style: { fill: "var(--ink-3)" }, text: v.toFixed(2) }, svg);
    });
    el("line", { x1: x(0.002), x2: x(0.002), y1: top - 12, y2: H - 30, style: { stroke: "var(--bad)", strokeDasharray: "4 3" } }, svg);
    el("text", { x: x(0.002) + 4, y: top - 14, "font-size": 11, style: { fill: "var(--bad)" }, text: "0.002 nats (H2 bound)" }, svg);
    us.forEach((u, i) => {
      const y = top + i * rowH + 14;
      el("text", { x: 0, y: y + 4, "font-size": 12, style: { fill: "var(--ink-2)" }, text: `${OUT_SHORT[u.outcome].split(" (")[0]} · ${label(u)}` }, svg);
      el("line", { x1: left, x2: left + pw, y1: y, y2: y, style: { stroke: "var(--grid)", strokeDasharray: "1 3" } }, svg);
      const big = Object.entries(u.by_n).filter(([n]) => +n >= 1000);
      P.forEach(([k, name, col]) => {
        const v = big.map(([, c]) => c.regret[k]).filter(z => z !== null && z !== undefined);
        if (!v.length) return;
        const m = v.reduce((a, b) => a + b, 0) / v.length;
        const c = el("circle", { cx: x(m), cy: y, r: k === "cv" ? 6 : 5, style: { fill: col, fillOpacity: k === "cv" ? 1 : 0.85, stroke: "var(--surface)", strokeWidth: 1.5 } }, svg);
        hover(c, `<b>${label(u)} · ${OUT_SHORT[u.outcome]}</b><br>${name}: mean regret ${m.toFixed(4)} nats<br>(sizes ≥ 1,000; ${big.map(([n, cc]) => fmtN(n) + ": " + (cc.regret[k] ?? 0).toFixed(4)).join(", ")})`);
      });
    });
    return P;
  }

  // ------------------------------------------------------------------ Figure 5: Riley vs break-even
  function rileyPlot(root, units) {
    const rowH = 26, left = 300, top = 26, pw = 450;
    const W = left + pw + 90, H = top + units.length * rowH + 40;
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Riley minimum sample size against the observed break-even of the own model" }, root);
    const lo = Math.log10(80), hi = Math.log10(12000);
    const x = v => left + (Math.log10(v) - lo) / (hi - lo) * pw;
    [100, 300, 1000, 3000, 10000].forEach(v => {
      el("line", { x1: x(v), x2: x(v), y1: top - 6, y2: H - 30, style: { stroke: "var(--grid)" } }, svg);
      el("text", { x: x(v), y: H - 12, "text-anchor": "middle", "font-size": 11, style: { fill: "var(--ink-3)" }, text: fmtN(v) }, svg);
    });
    units.forEach((u, i) => {
      const y = top + i * rowH + 12;
      el("text", { x: 0, y: y + 4, "font-size": 12, style: { fill: "var(--ink-2)" }, text: `${OUT_SHORT[u.outcome].split(" (")[0]} · ${label(u)}` }, svg);
      const sizes = Object.keys(u.by_n).map(Number);
      const be = sizes.find(n => u.by_n[String(n)].own_beats_adopt_share >= 0.8);
      const maxN = Math.max(...sizes);
      const r = u.riley_patients;
      const bx = be ? x(be) : x(maxN) + 24;
      if (r) el("line", { x1: x(r), x2: bx, y1: y, y2: y, style: { stroke: "var(--axis)", strokeWidth: 2 } }, svg);
      if (r) { const c = el("circle", { cx: x(r), cy: y, r: 5, style: { fill: "var(--ink-2)" } }, svg); hover(c, `<b>${label(u)}</b><br>Riley et al. (2020) minimum: ${fmtN(r)} patients`); }
      if (be) {
        const c = el("rect", { x: bx - 5, y: y - 5, width: 10, height: 10, style: { fill: u.regime === "relation" ? "var(--accent)" : "var(--level)" } }, svg);
        hover(c, `<b>${label(u)}</b><br>Own model beats adopted in ≥ 80% of hospitals from ${fmtN(be)} patients`);
      } else {
        const t = el("text", { x: bx + 6, y: y + 4, "text-anchor": "start", "font-size": 11, style: { fill: "var(--ink-3)" }, text: `never ≤ ${maxN >= 1000 ? maxN / 1000 + "k" : maxN}` }, svg);
        hover(t, `<b>${label(u)}</b><br>Own model never beat adopted in ≥ 80% of hospitals up to ${fmtN(maxN)} patients`);
      }
    });
  }

  // ------------------------------------------------------------------ table + hypothesis bars
  function unitsTable(root, units) {
    const be = (u, key) => { const s = Object.keys(u.by_n).map(Number).find(n => (u.by_n[String(n)][key] ?? 0) >= 0.8); return s ? fmtN(s) : "never"; };
    const rows = units.map(u => `<tr><td>${OUT_SHORT[u.outcome]}</td><td>${label(u)}</td><td><span class="pill ${u.regime}">${u.regime === "relation" ? "relation" : "level"}</span></td>` +
      `<td class="num-c">${be(u, "update_beats_adopt_share")}</td><td class="num-c">${be(u, "own_beats_adopt_share")}</td><td class="num-c">${be(u, "own_beats_update_share")}</td>` +
      `<td><span class="pill ${u.status === "confirmatory" ? "conf" : "expl"}">${statusTag(u)}</span></td></tr>`).join("");
    root.innerHTML = `<table><thead><tr><th>Outcome</th><th>Destination</th><th>Shift</th><th>Update beats adopt</th><th>Own beats adopt</th><th>Own beats update</th><th>Status</th></tr></thead><tbody>${rows}</tbody></table>`;
  }
  function hypBars(h) {
    for (const k of ["H1", "H2", "H3"]) {
      const card = document.querySelector(`[data-hyp="${k}"]`);
      if (!card) continue;
      const c = h[k], tot = c.hold + c.fail + c["not evaluable"];
      card.querySelector(".bar").innerHTML = `<i style="width:${c.hold / tot * 100}%;background:var(--good)"></i><i style="width:${c.fail / tot * 100}%;background:var(--bad)"></i><i style="width:${c["not evaluable"] / tot * 100}%;background:var(--axis)"></i>`;
      card.querySelector(".counts").textContent = `${c.hold} hold · ${c.fail} fail · ${c["not evaluable"]} not evaluable (of ${tot} units)`;
    }
  }

  fetch("data/study.json").then(r => r.json()).then(d => {
    const U = d.units;
    decisionMap(document.getElementById("fig-map"), U);
    buildVsUpdate(document.getElementById("fig-build"), U);
    const box = document.getElementById("fig-regret");
    const draw = w => { regretPlot(box, U, w); document.querySelectorAll("#regret-tabs button").forEach(b => b.setAttribute("aria-pressed", b.dataset.w === w)); };
    document.querySelectorAll("#regret-tabs button").forEach(b => b.addEventListener("click", () => draw(b.dataset.w)));
    draw("confirmatory");
    rileyPlot(document.getElementById("fig-riley"), U);
    unitsTable(document.getElementById("tbl-units"), U);
    hypBars(d.hypotheses);
  });
})();
