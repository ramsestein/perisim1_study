"""Pure helpers shared by the review-7 scripts (adopt, update or build): no project imports, so the T2 script can
use them next to its own frozen code (docs/DECISIONS.md, 2026-11-17)."""

from __future__ import annotations

import numpy as np

OPTIONS = ("adopt", "update", "own")
EXTRA = ("adopt_isotonic", "lr_base", "lr_logistic", "pram_lgbm", "pram_lgbm_iso", "pram_lr", "pram_lr_iso",
         "lgbm_base")
SLOPE_THR, GAP_THR, N_UPDATE = 0.8, 0.03, 500          # the rule fixed in DECISIONS 2026-11-17 (after reading)
INNER = 3


def rule_choice(diag: dict, n: int) -> str:
    rel = diag["slope"] < SLOPE_THR or diag["auroc_gap"] > GAP_THR
    return "update" if (rel and n >= N_UPDATE) else "adopt"


def spearman(a, b) -> float | None:
    a, b = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 5:
        return None
    from scipy.stats import spearmanr
    return float(spearmanr(a[ok], b[ok]).correlation)


def summarise(samples: list[dict], sizes: list) -> dict:
    """Readings fixed in DECISIONS 2026-11-17 from the per-sample records (one per draw × fold or draw)."""
    by_n, breakeven = {}, {}
    pairs = (("own", "adopt"), ("update", "adopt"), ("own", "update"))
    for n in sizes:
        S = [s for s in samples if s["n"] == n]
        if not S:
            continue
        o = {"samples": len(S)}
        arms = [a for a in OPTIONS + EXTRA if all(a in s["ll"] for s in S)]
        o["logloss_mean"] = {a: float(np.mean([s["ll"][a] for s in S])) for a in arms}
        o["auroc_mean"] = {a: float(np.nanmean([s["auc"][a] for s in S])) for a in arms}
        for a, b in pairs:
            d = np.array([s["ll"][a] - s["ll"][b] for s in S])
            o[f"{a}_vs_{b}"] = {"mean": float(d.mean()), "share_wins": float((d < 0).mean())}
        best = [min(OPTIONS, key=lambda a: s["ll"][a]) for s in S]
        o["best_option_share"] = {a: float(np.mean([b == a for b in best])) for a in OPTIONS}
        pol = {"cv": [s["cv_choice"] for s in S], "rule": [s["rule_choice"] for s in S]}
        pol.update({f"always_{a}": [a] * len(S) for a in OPTIONS})
        o["policies"] = {}
        for name, ch in pol.items():
            reg = [s["ll"][c] - s["ll"][b] for s, c, b in zip(S, ch, best)]
            o["policies"][name] = {"regret_mean": float(np.mean(reg)), "regret_p90": float(np.percentile(reg, 90)),
                                   "correct_share": float(np.mean([c == b for c, b in zip(ch, best)])),
                                   "chosen_share": {a: float(np.mean([c == a for c in ch])) for a in OPTIONS}}
        o["diagnostics_mean"] = {k: float(np.nanmean([s["diag"][k] for s in S])) for k in ("slope", "auroc_gap")}
        if "pram_lr" in arms:
            o["pram"] = {}
            for a, b in (("pram_lr", "lr_base"), ("pram_lr", "lr_logistic"), ("pram_lr_iso", "lr_logistic"),
                         ("pram_lgbm", "lgbm_base"), ("pram_lgbm", "adopt"), ("pram_lgbm_iso", "adopt"),
                         ("pram_lr_iso", "own"), ("pram_lgbm_iso", "own")):
                d = np.array([s["ll"][a] - s["ll"][b] for s in S])
                o["pram"][f"{a}_vs_{b}"] = {"mean": float(d.mean()), "share_wins": float((d < 0).mean())}
            o["pram"]["alpha_mean"] = {k: float(np.mean([s["alpha"][k] for s in S])) for k in ("lgbm", "lr")}
        by_n[str(n)] = o
    for a, b in pairs:
        key = f"{a}_vs_{b}"
        mean_ok = [n for n in sizes if str(n) in by_n and by_n[str(n)][key]["mean"] < 0]
        rel_ok = [n for n in sizes if str(n) in by_n and by_n[str(n)][key]["share_wins"] >= 0.8]
        breakeven[key] = {"first_n_mean": mean_ok[0] if mean_ok else None, "first_n_80pct": rel_ok[0] if rel_ok else None}
    gap = [s["ll"]["own"] - s["ll"]["adopt"] for s in samples]
    pred = {"spearman_slope_vs_gap": spearman([s["diag"]["slope"] for s in samples], gap),
            "spearman_aurocgap_vs_gap": spearman([s["diag"]["auroc_gap"] for s in samples], gap)}
    return {"by_n": by_n, "breakeven": breakeven, "predictors": pred}


def render(res: dict) -> str:
    L = ["# Adopt, update or build? and a PRAM replica (post hoc, exploratory; internal review 7)", "",
         "Log-loss per landmark on each fold's test landmarks; one sample = one draw of n local patients in one fold.", ""]
    for name, r in res.items():
        L += [f"## {name}", "", f"Break-even: {r['breakeven']}", f"Predictors of own − adopt: {r['predictors']}", "",
              "| n | adopt | update | own | own<adopt (share) | best: adopt/update/own | regret cv | regret rule | "
              "regret always-adopt | always-update | always-own | cv correct |", "|---|" + "---|" * 11]
        for n, o in r["by_n"].items():
            lm, po = o["logloss_mean"], o["policies"]
            b = o["best_option_share"]
            L.append(f"| {n} | {lm['adopt']:.4f} | {lm['update']:.4f} | {lm['own']:.4f} | "
                     f"{o['own_vs_adopt']['share_wins']:.2f} | {b['adopt']:.2f}/{b['update']:.2f}/{b['own']:.2f} | "
                     f"{po['cv']['regret_mean']:.4f} | {po['rule']['regret_mean']:.4f} | "
                     f"{po['always_adopt']['regret_mean']:.4f} | {po['always_update']['regret_mean']:.4f} | "
                     f"{po['always_own']['regret_mean']:.4f} | {po['cv']['correct_share']:.2f} |")
        if any("pram" in o for o in r["by_n"].values()):
            L += ["", "PRAM replica (Δ log-loss mean, share of samples with a lower log-loss):", ""]
            for n, o in r["by_n"].items():
                if "pram" in o:
                    L.append(f"- n = {n}: " + "; ".join(
                        f"{k} {v['mean']:+.4f} ({v['share_wins']:.2f})" for k, v in o["pram"].items() if k != "alpha_mean")
                        + f"; α {o['pram']['alpha_mean']}")
        L.append("")
    return "\n".join(L) + "\n"


# =========================================================================== review 8 (DECISIONS 2026-11-17, R5–R7)
ALPHA_CT = 0.05
OWN_VARIANTS = ("own", "own_tuned", "own_lr")


def better(l_new, l_old, code, alpha: float = ALPHA_CT) -> bool:
    """One-sided test that the new candidate has the lower log-loss: z of the per-patient sums of row differences
    (as `roll`'s closed test)."""
    from scipy.stats import norm
    code = np.asarray(code)
    _, inv = np.unique(code, return_inverse=True)
    d = np.bincount(inv, weights=np.asarray(l_new, dtype=np.float64) - np.asarray(l_old, dtype=np.float64))
    if d.size < 2 or d.std(ddof=1) == 0:
        return False
    z = float(d.mean() / (d.std(ddof=1) / np.sqrt(d.size)))
    return z < norm.ppf(alpha)


def closed_choice(L: dict, code, alpha: float = ALPHA_CT) -> str:
    """Vergouwe et al. (2017) top-down among the nested recalibrations, then update, then own (R5). `L` maps
    keep, intercept, logistic, update, own to per-row validation log-losses."""
    choice = "keep"
    if better(L["logistic"], L["keep"], code, alpha):
        choice = "logistic" if better(L["logistic"], L["intercept"], code, alpha) else "intercept"
    if better(L["update"], L[choice], code, alpha):
        choice = "update"
    if better(L["own"], L[choice], code, alpha):
        choice = "own"
    return choice


def net_benefit(p, y, t: float) -> float:
    """Net benefit per prediction at threshold t (Vickers and Elkin, 2006)."""
    p, y = np.asarray(p, dtype=np.float64), np.asarray(y, dtype=np.float64)
    pos = p >= t
    n = max(y.size, 1)
    return float(((pos & (y == 1)).sum() - (pos & (y == 0)).sum() * t / (1 - t)) / n)


def riley_n(p_par: int, phi: float, r2cs: float, shrink: float = 0.9, delta: float = 0.05, margin: float = 0.05) -> dict:
    """Riley et al. (2020) minimum sample size for developing a binary-outcome regression model, criteria 1–3."""
    lnl0 = phi * np.log(phi) + (1 - phi) * np.log(1 - phi)
    max_r2 = 1 - np.exp(2 * lnl0)
    n1 = p_par / ((shrink - 1) * np.log(1 - r2cs / shrink))
    s_vh = r2cs / (r2cs + delta * max_r2)
    n2 = p_par / ((s_vh - 1) * np.log(1 - r2cs / s_vh))
    n3 = (1.96 / margin) ** 2 * phi * (1 - phi)
    n = float(np.ceil(max(n1, n2, n3)))
    return {"n1": float(n1), "n2": float(n2), "n3": float(n3), "n": n, "events": float(n * phi), "r2cs": float(r2cs),
            "max_r2cs": float(max_r2), "p": int(p_par), "prevalence": float(phi)}


def r2cs_from_logloss(ll_model: float, ll_null: float) -> float:
    return float(1 - np.exp(-2 * (ll_null - ll_model)))


def summarise_r8(samples: list[dict], sizes: list, nb_keys: list) -> dict:
    """R5–R7 readings from the per-sample records."""
    by_n, breakeven = {}, {}
    for n in sizes:
        S = [s for s in samples if s["n"] == n]
        if not S:
            continue
        best = [min(OPTIONS, key=lambda a: s["ll"][a]) for s in S]
        o = {"samples": len(S), "logloss_mean": {a: float(np.mean([s["ll"][a] for s in S]))
                                                 for a in S[0]["ll"]}}
        pol = {"cv": [s["cv_choice"] for s in S], "rule": [s["rule_choice"] for s in S],
               "closed_test": [s["closed_choice"] for s in S]}
        o["policies"] = {}
        for name, ch in pol.items():
            reg = [s["ll"][c] - s["ll"][b] for s, c, b in zip(S, ch, best)]
            o["policies"][name] = {"regret_mean": float(np.mean(reg)), "regret_p90": float(np.percentile(reg, 90)),
                                   "correct_share": float(np.mean([c == b for c, b in zip(ch, best)])),
                                   "chosen_share": {c: float(np.mean([x == c for x in ch])) for c in sorted(set(ch))}}
        for v in OWN_VARIANTS + ("own_best",):
            d = np.array([s["ll"][v] - s["ll"]["adopt"] for s in S])
            o[f"{v}_vs_adopt"] = {"mean": float(d.mean()), "share_wins": float((d < 0).mean())}
            d2 = np.array([s["ll"][v] - s["ll"]["update"] for s in S])
            o[f"{v}_vs_update"] = {"mean": float(d2.mean()), "share_wins": float((d2 < 0).mean())}
        o["net_benefit"] = {}
        for k in nb_keys:
            for a in ("own", "update", "own_best"):
                d = np.array([100 * (s["nb"][k][a] - s["nb"][k]["adopt"]) for s in S])
                o["net_benefit"][f"{k}|{a}_vs_adopt"] = {"mean_per_100": float(d.mean()), "share_above_0": float((d > 0).mean())}
        o["events_mean"] = {k: float(np.mean([s["events"][k] for s in S])) for k in S[0]["events"]}
        by_n[str(n)] = o
    for v in OWN_VARIANTS + ("own_best",):
        for ref in ("adopt", "update"):
            key = f"{v}_vs_{ref}"
            rel = [n for n in sizes if str(n) in by_n and by_n[str(n)][key]["share_wins"] >= 0.8]
            breakeven[key] = rel[0] if rel else None
    return {"by_n": by_n, "breakeven_80pct": breakeven}


# =========================================================================== phase 1 (docs/prereg_third_outcome.md)
N_OWN_V2, N_UPDATE_V2 = 1000, 4000                    # rule v2, fixed in the registration (OSF 10.17605/OSF.IO/YPBVH)
TOL = 0.002


def relation_shift(diag: dict) -> bool:
    return bool(diag["slope"] < SLOPE_THR or diag["auroc_gap"] > GAP_THR)


def rule_v2_choice(diag: dict, n: int) -> str:
    if relation_shift(diag):
        return "own" if n >= N_OWN_V2 else "adopt"
    return "update" if n >= N_UPDATE_V2 else "adopt"


def add_policy(out: dict, samples: list[dict], name: str, key: str) -> None:
    """Adds a policy read from `key` of each sample to summarise_r8's by_n (regret against the best option)."""
    for n, o in out["by_n"].items():
        S = [s for s in samples if str(s["n"]) == n]
        best = [min(OPTIONS, key=lambda a: s["ll"][a]) for s in S]
        ch = [s[key] for s in S]
        reg = [s["ll"][c] - s["ll"][b] for s, c, b in zip(S, ch, best)]
        o["policies"][name] = {"regret_mean": float(np.mean(reg)), "regret_p90": float(np.percentile(reg, 90)),
                               "correct_share": float(np.mean([c == b for c, b in zip(ch, best)])),
                               "chosen_share": {c: float(np.mean([x == c for x in ch])) for c in sorted(set(ch))}}


def hypotheses(samples: list[dict], out: dict, sizes: list, tol: float = TOL) -> dict:
    """H1–H3 of the registration, per unit. A claim the unit's sizes cannot decide is 'not evaluable'."""
    flags = [relation_shift(s["diag"]) for s in samples if s["n"] <= 1000]
    share = float(np.mean(flags)) if flags else float("nan")
    regime = "relation shift" if share >= 0.5 else "level shift"
    top = max(sizes) if sizes else 0
    be = out["breakeven_80pct"]
    if regime == "relation shift":
        b = be["own_vs_adopt"]
        h1 = "hold" if (b is not None and b <= 2000) else ("not evaluable" if top < 2000 else "fail")
    else:
        b = be["own_vs_update"]
        h1 = "fail" if (b is not None and b <= 4000) else ("not evaluable" if top < 4000 else "hold")
    big = [n for n in out["by_n"] if int(n) >= 1000]
    po = {n: out["by_n"][n]["policies"] for n in big}
    reg_cv = {n: po[n]["cv"]["regret_mean"] for n in big}
    excess = {n: po[n]["rule_v2"]["regret_mean"] - po[n]["cv"]["regret_mean"] for n in big}
    h2 = "not evaluable" if not big else ("hold" if all(v <= tol for v in reg_cv.values()) else "fail")
    h3 = "not evaluable" if not big else ("hold" if all(v <= tol for v in excess.values()) else "fail")
    return {"regime": regime, "flag_share": share, "H1": h1, "H2": h2, "H3": h3, "largest_n": top,
            "cv_regret_n_ge_1000": reg_cv, "rule_v2_excess_regret_n_ge_1000": excess}


def verdicts(hs: list[dict]) -> dict:
    """Registration section 4: H1 holds if it holds in all units, one exception = partial failure, two or more =
    failure; H2 and H3 hold if they hold in every unit. Units that cannot decide a claim are counted apart."""
    out = {}
    for k in ("H1", "H2", "H3"):
        c = {s: sum(h[k] == s for h in hs) for s in ("hold", "fail", "not evaluable")}
        if c["hold"] + c["fail"] == 0:
            v = "not evaluable"
        elif k == "H1":
            v = "holds" if c["fail"] == 0 else ("partial failure" if c["fail"] == 1 else "failure")
        else:
            v = "holds" if c["fail"] == 0 else "fails"
        out[k] = {"hold": c["hold"], "fail": c["fail"], "not_evaluable": c["not evaluable"], "verdict": v}
    return out


def logistic_guarded(x, y, w, slope=True, iters=200):
    """The recalibration fit of posthoc_paper._logistic (offset x [+ slope]) with step-halving on the weighted
    log-likelihood: the same maximum whenever plain Newton converges, and no divergence when it does not
    (DECISIONS 2026-11-18, phase 1 deviation). Returns (intercept, slope) or (CITL, 1)."""
    x, y, w = (np.asarray(v, dtype=np.float64) for v in (x, y, w))

    def ll(a, b):
        eta = a + b * x if slope else a + x
        return float((w * (y * eta - np.logaddexp(0.0, eta))).sum())

    a, b = 0.0, 1.0
    cur = ll(a, b)
    for _ in range(iters):
        eta = a + b * x if slope else a + x
        mu = 0.5 * (1.0 + np.tanh(0.5 * eta))
        r, v = w * (y - mu), w * mu * (1 - mu)
        if slope:
            g = np.array([r.sum(), (r * x).sum()])
            H = np.array([[v.sum(), (v * x).sum()], [(v * x).sum(), (v * x * x).sum()]])
            step = np.linalg.solve(H + 1e-12 * np.eye(2), g)
        else:
            step = np.array([r.sum() / max(v.sum(), 1e-12), 0.0])
        t = 1.0
        while t > 1e-8:
            na, nb = a + t * step[0], (b + t * step[1]) if slope else 1.0
            new = ll(na, nb)
            if np.isfinite(new) and new >= cur - 1e-12:
                break
            t *= 0.5
        else:
            break
        a, b, cur = na, nb, new
        if np.max(np.abs(t * step)) < 1e-10:
            break
    return a, b
