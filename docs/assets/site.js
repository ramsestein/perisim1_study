// Page behaviour: theme, top bar, reading progress, contents highlight, reveal on scroll, counters, hero background.
(() => {
  const root = document.documentElement;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // theme toggle (remembered per browser when storage is available)
  const btn = document.getElementById("theme-btn");
  const current = () => root.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  btn && btn.addEventListener("click", () => {
    const next = current() === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    try { localStorage.setItem("theme", next); } catch (e) { /* storage unavailable */ }
    document.dispatchEvent(new CustomEvent("themechange"));
  });

  // top bar + progress
  const bar = document.getElementById("topbar"), prog = document.getElementById("progress");
  const hero = document.querySelector(".hero");
  function onScroll() {
    const y = scrollY, h = document.documentElement.scrollHeight - innerHeight;
    bar.classList.toggle("solid", y > (hero ? hero.offsetHeight - 60 : 10));
    prog.style.width = (h > 0 ? (y / h) * 100 : 0) + "%";
  }
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // contents highlight
  const links = [...document.querySelectorAll(".toc a, .topbar nav a")];
  const targets = [...new Set(links.map(a => a.getAttribute("href")))].map(h => document.querySelector(h)).filter(Boolean);
  const spy = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const id = "#" + e.target.id;
      links.forEach(a => a.classList.toggle("on", a.getAttribute("href") === id));
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  targets.forEach(t => spy.observe(t));

  // reveal on scroll
  const rev = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add("in"); rev.unobserve(e.target); }
  }), { rootMargin: "0px 0px -8% 0px" });
  document.querySelectorAll(".reveal").forEach(el => reduce ? el.classList.add("in") : rev.observe(el));

  // counters in the hero
  document.querySelectorAll("[data-count]").forEach(el => {
    const end = +el.dataset.count, dec = +(el.dataset.dec || 0), pre = el.dataset.prefix || "";
    const fmt = v => pre + v.toFixed(dec);
    if (reduce) { el.textContent = fmt(end); return; }
    const t0 = performance.now(), dur = 1300;
    el.textContent = fmt(0);
    (function tick(t) {
      const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      el.textContent = fmt(end * e);
      if (k < 1) requestAnimationFrame(tick); else el.textContent = fmt(end);
    })(t0);
  });

  // hero background: drifting learning curves (decorative)
  const svg = document.getElementById("hero-bg");
  if (svg) {
    const NS = "http://www.w3.org/2000/svg";
    const W = 1200, H = 640;
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    const cols = ["#7fe0cf", "#9cc1ff", "#ffc58f"];
    const paths = [];
    for (let i = 0; i < 14; i++) {
      const p = document.createElementNS(NS, "path");
      p.setAttribute("fill", "none");
      p.setAttribute("stroke", cols[i % 3]);
      p.setAttribute("stroke-width", i % 5 === 0 ? 1.6 : 0.8);
      p.setAttribute("stroke-opacity", i % 5 === 0 ? 0.55 : 0.22);
      svg.appendChild(p);
      paths.push({ p, a: 30 + i * 18, k: 0.9 + (i % 4) * 0.35, ph: i * 0.7 });
    }
    const draw = t => {
      for (const c of paths) {
        let d = "";
        for (let x = 0; x <= W; x += 24) {
          const u = x / W;
          const y = c.a + (H * 0.45) * (1 - Math.exp(-c.k * 3 * u)) * (1 + 0.05 * Math.sin(u * 9 + c.ph + t / 2600));
          d += (x ? "L" : "M") + x + "," + y.toFixed(1);
        }
        c.p.setAttribute("d", d);
      }
      if (!reduce && !document.hidden) requestAnimationFrame(draw);
    };
    requestAnimationFrame(draw);
    document.addEventListener("visibilitychange", () => { if (!document.hidden && !reduce) requestAnimationFrame(draw); });
  }
})();
