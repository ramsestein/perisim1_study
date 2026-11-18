"""Post hoc, EXPLORATORY: internal review 8 on T2 (docs/DECISIONS.md, 2026-11-17, R5–R7).

R2/R3's draws and test set: the options from R2's cached predictions, the closed testing procedure with the
multinomial recalibrations as the nested steps, net benefit for death and for long stay or death, events, two more
own-model arms (multiclass LightGBM tuned by inner CV; multinomial L2 logistic regression) and the Riley et al. (2020)
minimum sample size (binary death against the rest and long stay or death against the rest).

Usage:  python scripts/posthoc_r8_t2.py [--profile local] [--threads 8]
Outputs (aggregates only): <workdir>/experiments/t2/results/posthoc/r8_t2.json and reports/r8_t2.md
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
import warnings
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import posthoc_t2_ladder as LD  # noqa: E402  (sets the frozen src on sys.path)
import posthoc_t2_own as TO  # noqa: E402
import own_ext_common as C  # noqa: E402

PT = LD.PT
LOG = logging.getLogger("r8_t2")
NB_DEATH = (0.02, 0.05, 0.10)
NB_SEVERE = (0.30, 0.40, 0.50)
GRID = [(nl, md) for nl in (7, 15, 31) for md in (20, 100)]
C_GRID = (0.01, 0.1, 1.0)
EPS = LD.EPS


def rows_ll(P, y):
    return -np.log(np.clip(P[np.arange(len(y)), y], EPS, 1.0))


def lgbm_multi_p(X, y, subj, X_te, Cn, seed, threads, num_leaves, min_data):
    import lightgbm as lgb
    if np.unique(y).size < 2:
        return np.tile(np.bincount(y, minlength=Cn) / len(y), (X_te.shape[0], 1))
    uniq = np.unique(subj)
    va = np.isin(subj, np.random.default_rng(seed).choice(uniq, size=max(1, int(round(0.2 * uniq.size))), replace=False))
    params = {"objective": "multiclass", "num_class": Cn, "learning_rate": 0.05, "num_leaves": num_leaves,
              "min_data_in_leaf": min_data, "bagging_fraction": 0.8, "bagging_freq": 1, "feature_fraction": 0.8,
              "deterministic": True, "force_col_wise": True, "num_threads": threads, "seed": seed, "verbose": -1}
    dtr = lgb.Dataset(X[~va], y[~va], free_raw_data=False)
    dva = lgb.Dataset(X[va], y[va], reference=dtr)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        b = lgb.train(params, dtr, 2000, valid_sets=[dva], callbacks=[lgb.early_stopping(50, verbose=False)])
    raw = b.predict(X_te, num_iteration=int(b.best_iteration or b.current_iteration()), raw_score=True)
    return LD.softmax(raw.reshape(X_te.shape[0], Cn))


def own_tuned(Xm, y, sX, fit, q, Cn, seed, threads):
    from sklearn.model_selection import GroupKFold
    score = {}
    for g in GRID:
        s = 0.0
        for i, (a, b) in enumerate(GroupKFold(C.INNER).split(fit, groups=sX[fit])):
            P = lgbm_multi_p(Xm[fit[a]], y[fit[a]], sX[fit[a]], Xm[fit[b]], Cn, seed + 7 * i, threads, *g)
            s += float(rows_ll(P, y[fit[b]]).sum())
        score[g] = s
    g = min(score, key=score.get)
    return lgbm_multi_p(Xm[fit], y[fit], sX[fit], Xm[q], Cn, seed, threads, *g), {"num_leaves": g[0], "min_data": g[1]}


def own_lr(Xm, y, sX, fit, q, Cn):
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    def fitpred(a, b, c):
        sc = StandardScaler().fit(np.nan_to_num(Xm[a]))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            m = LogisticRegression(C=c, max_iter=3000).fit(sc.transform(np.nan_to_num(Xm[a])), y[a])
        out = np.full((b.size, Cn), EPS)
        out[:, m.classes_] = m.predict_proba(sc.transform(np.nan_to_num(Xm[b])))
        return out / out.sum(1, keepdims=True)
    score = {}
    for c in C_GRID:
        score[c] = sum(float(rows_ll(fitpred(fit[a], fit[b], c), y[fit[b]]).sum())
                       for a, b in GroupKFold(C.INNER).split(fit, groups=sX[fit]))
    c = min(score, key=score.get)
    return fitpred(fit, q, c), {"C": c}


def closed_test(P_all, Xm, y, sX, fit, Cn, seed, threads) -> str:
    pats = np.unique(sX[fit])
    rng = np.random.default_rng(seed + 11)
    fp = np.isin(sX[fit], rng.permutation(pats)[:int(round(2 / 3 * pats.size))])
    f, v = fit[fp], fit[~fp]
    a0, _ = PT.fit_recal(P_all[f], y[f], slope=False)
    a1, b1 = PT.fit_recal(P_all[f], y[f], slope=True)
    O = TO.t2_options(P_all, Xm, y, sX, Cn, f, v, seed + 13, threads)
    P = {"keep": P_all[v], "intercept": PT.apply_recal(P_all[v], a0, 1.0), "logistic": PT.apply_recal(P_all[v], a1, b1),
         "update": O["update"], "own": O["own"]}
    return C.closed_choice({k: rows_ll(p, y[v]) for k, p in P.items()}, sX[v])


def nb_all(P, y):
    out = {}
    death = (y == 3).astype(float)
    severe = (y >= 2).astype(float)
    for t in NB_DEATH:
        out[f"death_t{t:.2f}"] = C.net_benefit(P[:, 3], death, t)
    for t in NB_SEVERE:
        out[f"severe_t{t:.2f}"] = C.net_benefit(P[:, 2] + P[:, 3], severe, t)
    return out


def riley_t2(P_test, y_test, p_par) -> dict:
    out = {}
    for name, pp, yy in (("death", P_test[:, 3], (y_test == 3)), ("severe", P_test[:, 2] + P_test[:, 3], (y_test >= 2))):
        yy = yy.astype(float)
        phi = float(yy.mean())
        ll_null = float(-(phi * np.log(phi) + (1 - phi) * np.log(1 - phi)))
        ll_m = float(-np.mean(yy * np.log(np.clip(pp, EPS, 1)) + (1 - yy) * np.log(np.clip(1 - pp, EPS, 1))))
        out[name] = C.riley_n(p_par, phi, C.r2cs_from_logloss(ll_m, ll_null))
    out["n_max"] = max(out["death"]["n"], out["severe"]["n"])
    return out


def run(pipe, threads: int) -> int:
    cfg, ws = pipe.cfg, pipe.ws
    t = "t2"
    dev = cfg.experiment["cohorts"]["development"]
    externals = [c for c in cfg.experiment["cohorts"]["external"] if c in pipe.available_cohorts()]
    args = {"names": pipe.feature_names(), "dev": dev, "externals": externals, "threads": threads}
    lcache = ws.predictions("posthoc", t) / "ladder"
    ocache = ws.predictions("posthoc", t) / "own"
    cache = ws.predictions("posthoc", t) / "r8"
    cache.mkdir(parents=True, exist_ok=True)
    fm = PT._load(ws.predictions("external", t) / "final_model.pkl")
    enc = fm["enc"]
    out = {"note": "Exploratory, post hoc (internal review 8, 2026-11-17).", "cohorts": {}}
    nb_keys = [f"death_t{x:.2f}" for x in NB_DEATH] + [f"severe_t{x:.2f}" for x in NB_SEVERE]
    for c in externals:
        if PT._eval_target_for(t, c, cfg) != t:
            continue
        ctx = PT.context(cfg, ws, t, c, args)
        X, Cn, y, split = ctx["X"], ctx["C"], ctx["lab"]["own"], ctx["split"]
        q, pool = (v[y[v] >= 0] for v in (split["test"], split["pool"]))
        sX = X.ft.subjects.astype(str)
        Xm = enc.transform_model(X.ft)[0]
        P_all = np.load(lcache / f"{c}_P_transported.npy")
        pats = np.unique(sX[pool])
        sizes = [n for n in TO.SIZES if n < pats.size]
        samples = []
        for n in sizes:
            for r in range(LD.DRAWS[n]):
                path = cache / f"{c}_n{n}_r{r}.json"
                if path.exists():
                    samples.append(json.loads(path.read_text(encoding="utf-8")))
                    continue
                t0 = time.perf_counter()
                seed = int(ctx["seed"]) + 1000 * r + int(n)
                pick = np.random.default_rng(seed).choice(pats, size=int(n), replace=False)
                fit = pool[np.isin(sX[pool], pick)]
                z = np.load(lcache / f"{c}_n{n}_r{r}.npz", allow_pickle=True)
                P = {o: z[a] for o, a in TO.MAP.items()}
                a0, _ = PT.fit_recal(P_all[fit], y[fit], slope=False)
                P["keep"], P["intercept"], P["logistic"] = P_all[q], PT.apply_recal(P_all[q], a0, 1.0), P["adopt"]
                P["own_tuned"], tuned = own_tuned(Xm, y, sX, fit, q, Cn, seed, threads)
                P["own_lr"], lrinfo = own_lr(Xm, y, sX, fit, q, Cn)
                o7 = json.loads((ocache / f"{c}_n{n}_r{r}.json").read_text(encoding="utf-8"))
                ct = closed_test(P_all, Xm, y, sX, fit, Cn, seed, threads)
                L = {a: LD.logloss(p, y[q]) for a, p in P.items()}
                L["own_best"] = min(L[v] for v in C.OWN_VARIANTS)
                bestv = min(C.OWN_VARIANTS, key=lambda v: L[v])
                nbs = {a: nb_all(P[a], y[q]) for a in ("adopt", "update", "own")}
                nbs["own_best"] = nb_all(P[bestv], y[q])
                nb = {k: {a: nbs[a][k] for a in nbs} for k in nb_keys}
                rec = {"n": n, "r": r, "ll": L, "cv_choice": o7["cv_choice"], "rule_choice": o7["rule_choice"],
                       "closed_choice": ct, "nb": nb,
                       "events": {"deaths": int((y[fit] == 3).sum()), "long_or_death": int((y[fit] >= 2).sum())},
                       "tuned": tuned, "lr": lrinfo, "seconds": time.perf_counter() - t0}
                path.write_text(json.dumps(rec), encoding="utf-8")
                samples.append(rec)
                LOG.info("r8 t2 %s n=%d r=%d: closed→%s (%.0f s)", c, n, r, ct, rec["seconds"])
        res = C.summarise_r8(samples, sizes, nb_keys)
        Pz = np.load(lcache / f"{c}_n{sizes[-1]}_r0.npz", allow_pickle=True)          # not used for Riley
        full = lcache / f"{c}_nall_r0.npz"
        P_adopt_all = np.load(full, allow_pickle=True)["offsets_slope"] if full.exists() else Pz["offsets_slope"]
        res.update({"sizes": sizes, "riley": riley_t2(P_adopt_all, y[q], int(Xm.shape[1])),
                    "test_prevalence": {"death": float((y[q] == 3).mean()), "long_or_death": float((y[q] >= 2).mean())}})
        out["cohorts"][c] = res
        LOG.info("r8 t2 %s done", c)
    rd = ws.root / "results" / "posthoc"
    rd.mkdir(parents=True, exist_ok=True)
    (rd / "r8_t2.json").write_text(json.dumps(out, indent=1, default=float), encoding="utf-8")
    L = ["# Internal review 8 on T2 (post hoc, exploratory)", ""]
    for c, r in out["cohorts"].items():
        L += [f"## {c}", "", f"Break-even (≥ 80 % of samples): {r['breakeven_80pct']}",
              f"Riley et al. (2020): death n = {r['riley']['death']['n']:.0f} (events {r['riley']['death']['events']:.0f}); "
              f"long stay or death n = {r['riley']['severe']['n']:.0f}; test prevalences {r['test_prevalence']}", "",
              "| n | regret cv / closed / rule | correct cv / closed / rule | closed choice | own, own_tuned, own_lr, best − adopt | "
              "ΔNB own − adopt /100 (death 0.05; severe 0.40) | events (deaths, long or death) |", "|---|---|---|---|---|---|---|"]
        for n, o in r["by_n"].items():
            po, nb = o["policies"], o["net_benefit"]
            L.append(f"| {n} | {po['cv']['regret_mean']:.4f} / {po['closed_test']['regret_mean']:.4f} / {po['rule']['regret_mean']:.4f} | "
                     f"{po['cv']['correct_share']:.2f} / {po['closed_test']['correct_share']:.2f} / {po['rule']['correct_share']:.2f} | "
                     f"{po['closed_test']['chosen_share']} | "
                     + ", ".join(f"{o[f'{v}_vs_adopt']['mean']:+.4f} ({o[f'{v}_vs_adopt']['share_wins']:.2f})"
                                 for v in C.OWN_VARIANTS + ('own_best',)) + " | "
                     f"{nb['death_t0.05|own_vs_adopt']['mean_per_100']:+.2f}; {nb['severe_t0.40|own_vs_adopt']['mean_per_100']:+.2f} | "
                     f"{o['events_mean']['deaths']:.0f}, {o['events_mean']['long_or_death']:.0f} |")
        L.append("")
    (ws.reports / "r8_t2.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    LOG.info("r8 t2: %s", rd / "r8_t2.json")
    return 0


def main(argv=None) -> int:
    from perisim.config import load_config
    from perisim.pipeline import Pipeline
    from perisim.utils import now_iso, setup_logging

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--profile", default=None)
    ap.add_argument("--workdir", default=None)
    ap.add_argument("--threads", type=int, default=8)
    a = ap.parse_args(argv)
    over = {"experiment": {"paths": {"workdir": str(Path(a.workdir).resolve())}}} if a.workdir else {}
    pipe = Pipeline(load_config(None, a.profile, over))
    setup_logging(pipe.ws.logs / f"r8_t2_{now_iso().replace(':', '')}.log")
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    return run(pipe, a.threads)


if __name__ == "__main__":
    raise SystemExit(main())
