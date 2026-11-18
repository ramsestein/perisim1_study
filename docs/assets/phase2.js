// Phase 2 figures (OSF SAJEX), drawn from docs/data/study.json -> phase2 (built by site/build_data.py).
(() => {
  const NS = "http://www.w3.org/2000/svg";
  const fmtN = n => Number(n).toLocaleString("en-US");
  const sgn = (v, d = 4) => (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v).toFixed(d);
  const pct = v => Math.round(v * 100) + "%";
  const SYS = { inspire: "INSPIRE", mimic: "MIMIC-IV", eicu: "eICU-CRD" };
  const OUT = { hypo: "Hypotension", O1: "Vasopressor start", O2: "ICU discharge" };

  function el(tag, attrs = {}, parent) {
    const e = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "style") Object.assign(e.style, v); else if (k === "text") e.textContent = v; else e.setAttribute(k, v);
    }
    if (parent) parent.appendChild(e);
    return e;
  }
  let tip = document.querySelector(".tip");
  if (!tip) { tip = document.createElement("div"); tip.className = "tip"; document.body.appendChild(tip); }
  function hover(node, html) {
    node.addEventListener("mousemove", ev => {
      tip.innerHTML = html; tip.style.opacity = 1;
      tip.style.left = Math.min(ev.clientX + 14, innerWidth - 300) + "px"; tip.style.top = (ev.clientY + 14) + "px";
    });
    node.addEventListener("mouseleave", () => { tip.style.opacity = 0; });
  }
  const txt = (g, x, y, s, o = {}) => el("text", { x, y, "font-size": o.size || 12, "text-anchor": o.anchor || "start",
    "font-weight": o.weight || 400, style: { fill: o.fill || "var(--ink-2)" }, text: s }, g);
  const unitName = id => { const [, o, d] = id.split("_"); return `${OUT[o]} · ${SYS[d]}`; };
  const tabs = (id, draw) => {
    const bs = document.querySelectorAll(`#${id} button`);
    bs.forEach(b => b.addEventListener("click", () => { bs.forEach(x => x.setAttribute("aria-pressed", x === b)); draw(b.dataset.n); }));
    const on = [...bs].find(b => b.getAttribute("aria-pressed") === "true");
    draw(on ? on.dataset.n : bs[0].dataset.n);
  };

  // ------------------------------------------------------------ Figure 4: phase 1 options vs balanced (M0)
  function balanced(root, p2, units, n) {
    root.innerHTML = "";
    const OUTL = { hypo: "Hypotension", t2: "Stay after ICU (T2)", O1: "Vasopressor start (O1)", O2: "ICU discharge (O2)" };
    const rows = p2.balanced.map(r => ({ ...r, bal: r.by_n[n] || null, p1: r.phase1[n] ?? null }));
    const vals = rows.flatMap(r => [r.p1, r.bal && r.bal.d]).filter(v => v !== null && v !== undefined);
    const lim = Math.max(0.004, ...vals.map(Math.abs)) * 1.12;
    const left = 270, pw = 450, rowH = 26, top = 30;
    let nrow = rows.length + 4;
    const W = left + pw + 40, H = top + nrow * rowH + 30;
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Build minus update with phase 1 options and with balanced options, 17 units" }, root);
    const x = v => left + (v + lim) / (2 * lim) * pw;
    const step = lim > 0.02 ? 0.01 : lim > 0.008 ? 0.004 : 0.002;
    for (let v = -Math.floor(lim / step) * step; v <= lim; v += step) {
      const vv = +v.toFixed(4);
      el("line", { x1: x(vv), x2: x(vv), y1: top - 8, y2: H - 26, style: { stroke: Math.abs(vv) < 1e-9 ? "var(--axis)" : "var(--grid)" } }, svg);
      txt(svg, x(vv), H - 8, Math.abs(vv) < 1e-9 ? "0" : sgn(vv, 3), { anchor: "middle", size: 11, fill: "var(--ink-3)" });
    }
    txt(svg, x(-lim) + 2, top - 14, "← building better", { size: 11, fill: "var(--own)" });
    txt(svg, x(lim) - 2, top - 14, "updating better →", { size: 11, fill: "var(--update)", anchor: "end" });
    let y = top, last = null;
    rows.forEach(r => {
      if (r.outcome !== last) {
        txt(svg, 0, y + 15, OUTL[r.outcome], { size: 12.5, weight: 700, fill: "var(--ink)" });
        y += rowH; last = r.outcome;
      }
      const yc = y + 12;
      txt(svg, 12, yc + 4, r.label, { size: 12, fill: r.bal ? "var(--ink-2)" : "var(--ink-3)" });
      if (r.regime === "relation") el("circle", { cx: left - 14, cy: yc, r: 4, style: { fill: "var(--accent)" } }, svg);
      if (!r.bal) {
        txt(svg, x(0) + 8, yc + 4, `not evaluated at ${fmtN(n)} patients`, { size: 11, fill: "var(--ink-3)" });
      } else {
        if (r.p1 !== null) {
          el("line", { x1: x(r.p1), x2: x(r.bal.d), y1: yc, y2: yc, style: { stroke: "var(--axis)", strokeWidth: 2 } }, svg);
          const c0 = el("circle", { cx: x(r.p1), cy: yc, r: 5, style: { fill: "var(--surface)", stroke: "var(--ink-3)", strokeWidth: 2 } }, svg);
          hover(c0, `<b>${OUTL[r.outcome]} · ${r.label}</b><br>${fmtN(n)} patients · phase 1 options<br>Build − update: ${sgn(r.p1)} nats`);
        }
        const win = r.bal.share >= 0.8;
        const c = el("circle", { cx: x(r.bal.d), cy: yc, r: 6, style: { fill: win ? "var(--own)" : "var(--update)", stroke: "var(--surface)", strokeWidth: 1.5 } }, svg);
        hover(c, `<b>${OUTL[r.outcome]} · ${r.label}</b><br>${fmtN(n)} patients · balanced options<br>Build − update: ${sgn(r.bal.d)} nats<br>Build wins in ${pct(r.bal.share)} of samples<br>Update beats recalibrate in ${pct(r.bal.upd_adopt)}`);
      }
      y += rowH;
    });
  }

  // ------------------------------------------------------------ G cards
  function gcards(h) {
    const set = (g, k, v) => { const e = document.querySelector(`[data-g="${g}"] [data-k="${k}"]`); if (e) e.textContent = v; };
    set("G1", "units", h.G1.units); set("G1", "exceptions", h.G1.exceptions);
    set("G2", "rd", h.G2.rd.toFixed(2)); set("G2", "ci", `${h.G2.ci[0].toFixed(2)} to ${h.G2.ci[1].toFixed(2)}`);
    set("G3", "m0", pct(h.G3.share_by_level.M0)); set("G3", "m1", pct(h.G3.share_by_level.M1));
    set("G4", "median", h.G4.median.toFixed(4)); set("G4", "p90", h.G4.p90.toFixed(4));
  }

  // ------------------------------------------------------------ Figure 5: harmonization ladder
  function harm(root, p2) {
    const L = ["M0", "M1", "M2", "M3"], lab = p2.level_labels;
    const left = 52, pw = 600, ph = 260, top = 18, W = left + pw + 140, H = top + ph + 56;
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Share of samples where the own model wins, by harmonization error" }, root);
    const x = i => left + 30 + i * (pw - 60) / 3, y = v => top + (1 - v) * ph;
    [0, 0.25, 0.5, 0.75, 1].forEach(v => {
      el("line", { x1: left, x2: left + pw, y1: y(v), y2: y(v), style: { stroke: "var(--grid)" } }, svg);
      txt(svg, left - 8, y(v) + 4, pct(v), { anchor: "end", size: 11, fill: "var(--ink-3)" });
    });
    L.forEach((k, i) => {
      txt(svg, x(i), H - 26, k, { anchor: "middle", size: 12.5, weight: 700, fill: "var(--ink)" });
      txt(svg, x(i), H - 10, lab[k], { anchor: "middle", size: 11.5, fill: "var(--ink-3)" });
    });
    const ids = Object.keys(p2.levels.M0.by_unit);
    ids.forEach(id => {
      const pts = L.map((k, i) => [x(i), y(p2.levels[k].by_unit[id])]);
      const pth = el("path", { d: pts.map((p, j) => (j ? "L" : "M") + p.join(",")).join(" "), style: { fill: "none", stroke: "var(--axis)", strokeWidth: 1.4, strokeOpacity: 0.8 } }, svg);
      const hit = el("path", { d: pth.getAttribute("d"), style: { fill: "none", stroke: "transparent", strokeWidth: 10 } }, svg);
      hover(hit, `<b>${unitName(id)}</b><br>` + L.map(k => `${k} (${lab[k]}): ${pct(p2.levels[k].by_unit[id])}`).join("<br>"));
      hit.addEventListener("mouseenter", () => { pth.style.stroke = "var(--ink-2)"; pth.style.strokeWidth = 2.2; });
      hit.addEventListener("mouseleave", () => { pth.style.stroke = "var(--axis)"; pth.style.strokeWidth = 1.4; });
    });
    // band
    const up = L.map((k, i) => [x(i), y(p2.levels[k].ci[1])]), lo = L.map((k, i) => [x(i), y(p2.levels[k].ci[0])]).reverse();
    el("path", { d: [...up, ...lo].map((p, j) => (j ? "L" : "M") + p.join(",")).join(" ") + "Z", style: { fill: "var(--own)", fillOpacity: 0.14 } }, svg);
    const pts = L.map((k, i) => [x(i), y(p2.levels[k].share)]);
    el("path", { d: pts.map((p, j) => (j ? "L" : "M") + p.join(",")).join(" "), style: { fill: "none", stroke: "var(--own)", strokeWidth: 3.2, strokeLinejoin: "round" } }, svg);
    L.forEach((k, i) => {
      const v = p2.levels[k];
      const c = el("circle", { cx: x(i), cy: y(v.share), r: 7, style: { fill: "var(--own)", stroke: "var(--surface)", strokeWidth: 2 } }, svg);
      txt(svg, i === 0 ? x(i) - 12 : x(i) + 12, i === 0 ? y(v.share) + 5 : y(v.share) - 12, pct(v.share), { size: 14, weight: 700, fill: "var(--own)", anchor: i === 0 ? "end" : "start" });
      hover(c, `<b>${k} · ${lab[k]}</b><br>Best own beats best external in ${pct(v.share)} of samples<br>Unit-clustered 95 % CI ${pct(v.ci[0])} to ${pct(v.ci[1])}`);
    });
    txt(svg, left + pw + 14, y(0.5), "8 rotation units,", { size: 11.5, fill: "var(--ink-3)" });
    txt(svg, left + pw + 14, y(0.5) + 15, "250 to 4,000 patients", { size: 11.5, fill: "var(--ink-3)" });
  }

  // ------------------------------------------------------------ Figure 6: single hospitals
  function hospitals(root, p2, n) {
    root.innerHTML = "";
    const rows = [["hypo", "Hypotension"], ["O2", "ICU discharge"]];
    const HS = p2.hospitals.filter(h => h.by_n[n]);
    const all = HS.map(h => h.by_n[n].build_minus_update);
    const lo = Math.min(-0.004, ...all) * 1.1, hi = Math.max(0.01, ...all) * 1.06;
    const left = 120, pw = 640, band = 92, top = 24, W = left + pw + 20, H = top + rows.length * band + 40;
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Build minus update in single eICU-CRD hospitals" }, root);
    const x = v => left + (v - lo) / (hi - lo) * pw;
    const step = (hi - lo) > 0.04 ? 0.01 : 0.005;
    for (let v = Math.ceil(lo / step) * step; v <= hi; v += step) {
      const vv = +v.toFixed(4);
      el("line", { x1: x(vv), x2: x(vv), y1: top - 6, y2: H - 30, style: { stroke: Math.abs(vv) < 1e-9 ? "var(--axis)" : "var(--grid)", strokeWidth: Math.abs(vv) < 1e-9 ? 1.5 : 1 } }, svg);
      txt(svg, x(vv), H - 12, Math.abs(vv) < 1e-9 ? "0" : sgn(vv, 3), { anchor: "middle", size: 11, fill: "var(--ink-3)" });
    }
    txt(svg, x(0) + 6, top - 10, "updating better →", { size: 11, fill: "var(--update)" });
    rows.forEach(([o, name], r) => {
      const yc = top + r * band + band / 2;
      txt(svg, 0, yc + 4, name, { size: 13, weight: 650, fill: "var(--ink)" });
      txt(svg, 0, yc + 20, `${HS.filter(h => h.outcome === o).length} hospitals`, { size: 11, fill: "var(--ink-3)" });
      const hs = HS.filter(h => h.outcome === o).map(h => ({ h, v: h.by_n[n].build_minus_update })).sort((a, b) => a.v - b.v);
      // simple beeswarm: alternate offsets for neighbours closer than the dot size
      const placed = [];
      hs.forEach(d => {
        const cx = x(d.v);
        let off = 0, k = 0;
        while (placed.some(p => Math.abs(p.cx - cx) < 13 && Math.abs(p.off - off) < 13)) { k++; off = (k % 2 ? 1 : -1) * Math.ceil(k / 2) * 13; }
        placed.push({ cx, off });
        const c = d.h.by_n[n];
        const upd = c.update_beats_adopt_share >= 0.8;
        const dot = el("circle", { cx, cy: yc + off, r: 6, style: { fill: upd ? "var(--update)" : "var(--surface)", stroke: upd ? "var(--surface)" : "var(--adopt)", strokeWidth: upd ? 1.5 : 2 } }, svg);
        hover(dot, `<b>eICU-CRD hospital ${d.h.hospital} · ${name}</b><br>${fmtN(d.h.patients)} patients, prevalence ${(d.h.prevalence * 100).toFixed(1)}%<br>${fmtN(n)} local patients:<br>Build − update: ${sgn(c.build_minus_update)} nats (build wins in ${pct(c.build_beats_update_share)})<br>Update beats recalibrate in ${pct(c.update_beats_adopt_share)} of samples<br>Diagnostic flagged ${pct(c.flag_share)} of samples`);
      });
    });
  }

  // ------------------------------------------------------------ Figure 7: diagnostic by scenario
  function diag(root, p2) {
    const S = p2.scenarios, g2 = p2.hypotheses.G2;
    const rows = [
      ["H", "Single hospitals (H)", S.H], ["T", "Over time (T)", S.T], ["M0", "No harmonization error (M0)", S.M0],
      ["M1-M3", "Harmonization errors (M1–M3)", S["M1-M3"]], ["H+T+M0", "All without induced error", S["H+T+M0"]],
      ["G2", "All pooled · registered G2", { rd: g2.rd, ci: g2.ci, npv: g2.npv, base_rate: null, units: 41 + 24, samples: g2.samples }],
    ];
    const left = 230, pw = 330, gap = 40, pw2 = 190, rowH = 34, top = 30;
    const W = left + pw + gap + pw2 + 20, H = top + rows.length * rowH + 34;
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Shift diagnostic accuracy by scenario" }, root);
    const lo = -0.3, hi = 0.6, x = v => left + (v - lo) / (hi - lo) * pw;
    const x2 = v => left + pw + gap + (v - 0.6) / 0.4 * pw2;
    [-0.2, 0, 0.2, 0.4, 0.6].forEach(v => {
      el("line", { x1: x(v), x2: x(v), y1: top - 6, y2: H - 28, style: { stroke: v === 0 ? "var(--axis)" : "var(--grid)", strokeWidth: v === 0 ? 1.5 : 1 } }, svg);
      txt(svg, x(v), H - 10, v === 0 ? "0" : v.toFixed(1), { anchor: "middle", size: 11, fill: "var(--ink-3)" });
    });
    [0.6, 0.8, 1].forEach(v => {
      el("line", { x1: x2(v), x2: x2(v), y1: top - 6, y2: H - 28, style: { stroke: "var(--grid)" } }, svg);
      txt(svg, x2(v), H - 10, v.toFixed(1), { anchor: "middle", size: 11, fill: "var(--ink-3)" });
    });
    txt(svg, x(lo), top - 14, "Risk difference (flagged − unflagged)", { size: 11.5, weight: 650, fill: "var(--ink-2)" });
    txt(svg, x2(0.6), top - 14, "NPV", { size: 11.5, weight: 650, fill: "var(--ink-2)" });
    rows.forEach(([k, name, s], i) => {
      const y = top + i * rowH + 14;
      if (k === "G2") el("line", { x1: 0, x2: W, y1: y - 18, y2: y - 18, style: { stroke: "var(--rule)" } }, svg);
      txt(svg, 0, y + 4, name, { size: 12.5, weight: k === "G2" ? 700 : 400, fill: k === "G2" ? "var(--ink)" : "var(--ink-2)" });
      const weak = k === "T";
      el("line", { x1: x(Math.max(lo, s.ci[0])), x2: x(Math.min(hi, s.ci[1])), y1: y, y2: y, style: { stroke: "var(--accent)", strokeWidth: 2.4, strokeDasharray: weak ? "3 3" : "", strokeOpacity: weak ? 0.6 : 1 } }, svg);
      const c = el("circle", { cx: x(s.rd), cy: y, r: 6, style: { fill: weak ? "var(--surface)" : "var(--accent)", stroke: "var(--accent)", strokeWidth: 2 } }, svg);
      hover(c, `<b>${name}</b><br>${s.units} units · ${fmtN(s.samples)} samples<br>Risk difference ${s.rd.toFixed(3)} (95 % CI ${s.ci[0].toFixed(3)} to ${s.ci[1].toFixed(3)})` +
        (s.base_rate !== null ? `<br>Own model wins in ${pct(s.base_rate)} of samples · PPV ${s.ppv} · NPV ${s.npv}` : "") + (weak ? "<br><i>3 units: the clustered interval is not interpretable.</i>" : ""));
      if (s.base_rate !== null && s.base_rate !== undefined) {
        const b = 1 - s.base_rate;
        if (b >= 0.6) el("rect", { x: x2(0.6), y: y - 7, width: Math.max(0, x2(Math.min(1, b)) - x2(0.6)), height: 14, rx: 3, style: { fill: "var(--grid)", stroke: "var(--axis)" } }, svg);
        if (s.npv >= 0.6) {
          const m = el("rect", { x: x2(Math.min(1, s.npv)) - 2, y: y - 10, width: 4, height: 20, rx: 2, style: { fill: "var(--accent)" } }, svg);
          hover(m, `<b>${name}</b><br>NPV ${s.npv} vs ${b.toFixed(2)} with no diagnostic at all`);
        } else {
          txt(svg, x2(0.6) + 4, y + 4, `NPV ${s.npv} (base ${b.toFixed(2)})`, { size: 11, fill: "var(--ink-3)" });
        }
      }
    });
  }

  // ------------------------------------------------------------ Figure 9: G4 cells
  function g4(root, p2) {
    const cells = p2.g4_cells;
    const mx = Math.max(...cells.flatMap(c => [c[0], c[1]])) * 1.05;
    const left = 64, ps = 380, top = 16, W = left + ps + 200, H = top + ps + 50;
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Cross-validation regret against closed-test regret" }, root);
    const s = v => Math.sqrt(Math.max(0, v) / mx) * ps;
    const X = v => left + s(v), Y = v => top + ps - s(v);
    [0, 0.0005, 0.002, 0.005, 0.01, 0.02, 0.04].filter(v => v <= mx).forEach(v => {
      el("line", { x1: X(v), x2: X(v), y1: top, y2: top + ps, style: { stroke: "var(--grid)" } }, svg);
      el("line", { x1: left, x2: left + ps, y1: Y(v), y2: Y(v), style: { stroke: "var(--grid)" } }, svg);
      txt(svg, X(v), top + ps + 16, String(v), { anchor: "middle", size: 10.5, fill: "var(--ink-3)" });
      txt(svg, left - 6, Y(v) + 4, String(v), { anchor: "end", size: 10.5, fill: "var(--ink-3)" });
    });
    el("line", { x1: X(0), y1: Y(0), x2: X(mx), y2: Y(mx), style: { stroke: "var(--axis)", strokeDasharray: "5 4" } }, svg);
    txt(svg, left + ps / 2, H - 8, "Closed-test regret (nats)", { anchor: "middle", size: 12, fill: "var(--ink-2)" });
    const yl = el("text", { x: 14, y: top + ps / 2, "font-size": 12, "text-anchor": "middle", transform: `rotate(-90 14 ${top + ps / 2})`, style: { fill: "var(--ink-2)" }, text: "Cross-validation regret (nats)" }, svg);
    cells.forEach(([cv, ct, set]) => {
      const c = el("circle", { cx: X(ct), cy: Y(cv), r: 5, style: { fill: set === "T" ? "var(--accent)" : "var(--own)", fillOpacity: 0.78, stroke: "var(--surface)", strokeWidth: 1 } }, svg);
      hover(c, `<b>Set ${set}</b><br>Cross-validation ${cv.toFixed(4)} nats<br>Closed test ${ct.toFixed(4)} nats`);
    });
    const below = cells.filter(c => c[0] <= c[1]).length;
    const g = p2.hypotheses.G4;
    const bx = left + ps + 26;
    txt(svg, bx, top + 40, `${below} of ${cells.length}`, { size: 26, weight: 700, fill: "var(--ink)" });
    txt(svg, bx, top + 60, "cells with cross-validation", { size: 12, fill: "var(--ink-2)" });
    txt(svg, bx, top + 75, "no worse than the closed test", { size: 12, fill: "var(--ink-2)" });
    txt(svg, bx, top + 120, g.median.toFixed(4), { size: 22, weight: 700, fill: "var(--update)" });
    txt(svg, bx, top + 138, "median regret (nats)", { size: 12, fill: "var(--ink-2)" });
    txt(svg, bx, top + 178, g.p90.toFixed(4), { size: 22, weight: 700, fill: "var(--update)" });
    txt(svg, bx, top + 196, "90th percentile", { size: 12, fill: "var(--ink-2)" });
    void yl;
  }

  fetch("data/study.json").then(r => r.json()).then(d => {
    const p2 = d.phase2;
    gcards(p2.hypotheses);
    tabs("bal-tabs", n => balanced(document.getElementById("fig-balanced"), p2, d.units, n));
    harm(document.getElementById("fig-harm"), p2);
    tabs("hosp-tabs", n => hospitals(document.getElementById("fig-hosp"), p2, n));
    diag(document.getElementById("fig-diag"), p2);
    g4(document.getElementById("fig-g4"), p2);
  });
})();
