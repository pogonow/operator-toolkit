#!/usr/bin/env python3
"""AI Shortlist Check: build the weekly HTML report from the run files.

    python3 build_report.py --workdir [working folder] [--date YYYY-MM-DD] [--out file.html]

Reads   [workdir]/config.json
Reads   [workdir]/runs/YYYY-MM-DD.json   (this run, plus every earlier one for the trend charts)
Reads   [workdir]/analysis/YYYY-MM-DD.json if it exists (Claude's changes, actions, pricing flags)
Updates [workdir]/data/history.json      (copies the analysis into this week's entry)
Writes  [workdir]/report-YYYY-MM-DD.html (self-contained, opens offline by double click)

Every brand count is recomputed from the stored answers each time, so a competitor swapped
into config.json gets its history back from the older runs. Standard library only.
"""
import argparse
import collections
import glob
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run_prompts import AIO, brand_patterns, classify, clean_url, domain_of, load_json, save_json  # noqa: E402

CSS_PATH = os.path.join(HERE, "..", "templates", "report.css")
ENG = {"chatgpt": "ChatGPT", "gemini": "Gemini", "perplexity": "Perplexity", "claude": "Claude",
       "proxy": "Claude's web search (approximation)", AIO: "AI Overviews"}
DATE_FILE = re.compile(r"^\d{4}-\d{2}-\d{2}\.json$")
PRICE = re.compile(r"[$€£]\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:/|per)\s?(?:mo|month|year|yr))?", re.I)
ROUTE = {"api": "API via OpenRouter and SerpApi", "no-key": "Claude's web search (approximation) plus your pastes",
         "paste-all": "pasted by you"}
GREYS = ["#8A8078", "#B5ACA2", "#5E5650"]


def esc(x):
    return html.escape(str(x or ""), quote=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--workdir", default=".")
    ap.add_argument("--date", default=None, help="run date (default: latest runs/YYYY-MM-DD.json)")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    wd = os.path.abspath(args.workdir)

    cfg = load_json(os.path.join(wd, "config.json"), None)
    if not cfg:
        sys.exit(f"No config.json in {wd}.")
    files = sorted(f for f in glob.glob(os.path.join(wd, "runs", "*.json")) if DATE_FILE.match(os.path.basename(f)))
    if not files:
        sys.exit("No runs/YYYY-MM-DD.json yet. Run the prompts first.")
    date = args.date or os.path.basename(files[-1])[:10]
    d = load_json(os.path.join(wd, "runs", f"{date}.json"), None)
    if not d:
        sys.exit(f"No run file for {date}.")
    analysis = load_json(os.path.join(wd, "analysis", f"{date}.json"), {}) or {}

    P, COMP = cfg["product"], cfg.get("competitors", [])
    OTHER = cfg.get("other_brands", [])
    resolved = d.get("resolved_urls") or {}
    prompts = {p.get("id", f"P{i}"): p for i, p in enumerate(cfg.get("prompts", []), 1)}
    gq = {q.get("id", f"G{i}"): q for i, q in enumerate(cfg.get("google_queries", []), 1)}

    brands = [(P["name"], brand_patterns(P), "you")]
    brands += [(c["name"], brand_patterns(c), "tracked") for c in COMP]
    brands += [(b["name"], brand_patterns(b), "untracked") for b in OTHER]
    tracked = [P["name"]] + [c["name"] for c in COMP]

    def named(text):
        return [n for n, pats, _ in brands if any(p.search(text or "") for p in pats)]

    def clean(u):
        return clean_url(resolved.get(u) or u)

    def stype(u):
        return classify(u, P, COMP, cfg)

    def is_branded(pid, text, table):
        item = table.get(pid) or {}
        return bool(item.get("branded")) or any(p.search(text or "") for p in brand_patterns(P))

    def fmt(text):
        t = esc(text)
        t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
        t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", lambda m: '<a href="%s" target="_blank" rel="noopener">%s</a>' % (
            esc(clean(html.unescape(m.group(2)))), m.group(1)), t)
        t = re.sub(r"^#{1,6}\s*(.+)$", r"<b>\1</b>", t, flags=re.M)
        t = re.sub(r"^\s*[-*]\s+", "• ", t, flags=re.M)
        for pat in brand_patterns(P):
            t = pat.sub(lambda m: "<mark>%s</mark>" % m.group(0), t)
        return "".join("<p>%s</p>" % p.replace("\n", "<br>") for p in re.split(r"\n{2,}", t) if p.strip())

    def path_of(u):
        return domain_of(u) + re.sub(r"^https?://[^/]+", "", u)

    def links(urls):
        seen, out = set(), []
        for u in urls:
            c = clean(u)
            if c in seen:
                continue
            seen.add(c)
            out.append('<li><a href="%s" target="_blank" rel="noopener">%s</a> <span class="t">%s</span></li>' % (
                esc(c), esc(path_of(c)[:110]), stype(c)))
        return '<ul class="links">%s</ul>' % "".join(out) if out else '<p class="muted">No sources returned.</p>'

    R = d["results"]
    chat = [x for x in R if x["engine"] != AIO]
    aio = [x for x in R if x["engine"] == AIO]
    chat_engines = list(dict.fromkeys(x["engine"] for x in chat))
    engines = chat_engines + ([AIO] if aio else [])

    def ok_runs(x):
        return [r for r in x.get("runs", []) if not r.get("error")]

    # ---- share of voice, non-branded
    sov = {}
    for e in chat_engines:
        runs = [r for x in chat if x["engine"] == e and not is_branded(x["prompt_id"], x["prompt"], prompts) for r in ok_runs(x)]
        sov[e] = (len(runs), collections.Counter(n for r in runs for n in set(named(r["answer"]))))
    aio_nb = [x for x in aio if x.get("aio_shown") and not is_branded(x["prompt_id"], x["prompt"], gq)]
    if aio:
        sov[AIO] = (len(aio_nb), collections.Counter(n for x in aio_nb for n in set(named(x.get("answer", "")))))

    def pct(a, b):
        return round(100 * a / b) if b else 0

    cards = "".join('<div class="card"><div class="k">%s</div><div class="big">%d<span>%%</span></div><div class="muted">%s</div></div>' % (
        ENG.get(e, e), pct(sov[e][1][P["name"]], sov[e][0]),
        ("named in %d of %d non-branded runs" if e != AIO else "named in %d of %d non-branded queries that showed an AI Overview")
        % (sov[e][1][P["name"]], sov[e][0])) for e in engines)

    rows_b = []
    for n, _, k in brands:
        vals = [pct(sov[e][1][n], sov[e][0]) for e in engines]
        if k == "untracked" and max(vals or [0]) < 10:
            continue
        rows_b.append((k, n, vals))
    order = {"you": 0, "tracked": 1, "untracked": 2}
    rows_b.sort(key=lambda r: (order[r[0]], -max(r[2] or [0])))
    btab = "".join('<tr class="%s"><td>%s%s</td>%s</tr>' % (
        k, esc(n), ' <span class="tag">not tracked</span>' if k == "untracked" else "",
        "".join('<td class="num">%d%%<i style="width:%d%%"></i></td>' % (v, v) for v in vals)) for k, n, vals in rows_b)
    bhead = "".join("<th>%s</th>" % ENG.get(e, e) for e in engines)

    # ---- pages cited when the founder is missing
    pages = collections.defaultdict(lambda: {"n": 0, "eng": set(), "prompts": set()})
    for x in chat:
        if is_branded(x["prompt_id"], x["prompt"], prompts):
            continue
        for r in ok_runs(x):
            if P["name"] in named(r["answer"]):
                continue
            for u in set(clean(u) for u in r.get("cited_urls", [])):
                pages[u]["n"] += 1
                pages[u]["eng"].add(ENG.get(x["engine"], x["engine"]))
                pages[u]["prompts"].add(x["prompt_id"])
    for x in aio_nb:
        if P["name"] in named(x.get("answer", "")):
            continue
        for u in set(clean(u) for u in x.get("cited_urls", [])):
            pages[u]["n"] += 1
            pages[u]["eng"].add("AI Overviews")
            pages[u]["prompts"].add(x["prompt_id"])

    def idkey(s):
        m = re.match(r"([A-Za-z]+)(\d+)", s)
        return (m.group(1), int(m.group(2))) if m else (s, 0)

    top = sorted(pages.items(), key=lambda kv: -kv[1]["n"])[:30]
    ptab = "".join('<tr><td><a href="%s" target="_blank" rel="noopener">%s</a><div class="muted">%s</div></td><td class="num">%d</td><td>%s</td><td class="muted">%s</td></tr>' % (
        esc(u), esc(path_of(u)[:90]), stype(u), v["n"], ", ".join(sorted(v["eng"])),
        ", ".join(sorted(v["prompts"], key=idkey))) for u, v in top)

    # ---- chat prompts, run by run
    def status(k, n):
        if n == 0:
            return "none", "No answer"
        if k == 0:
            return "lost", "Lost"
        return ("won", "Won") if 2 * k >= n else ("mixed", "Mixed")

    pblocks = []
    for pid in list(dict.fromkeys(x["prompt_id"] for x in chat)):
        text = next(x["prompt"] for x in chat if x["prompt_id"] == pid)
        p = prompts.get(pid, {})
        chips, bodies = [], []
        for e in chat_engines:
            x = next((y for y in chat if y["engine"] == e and y["prompt_id"] == pid), None)
            if not x:
                continue
            runs = ok_runs(x)
            k = sum(1 for r in runs if P["name"] in named(r["answer"]))
            cls, lab = status(k, len(runs))
            chips.append('<span class="chip %s">%s %s %d/%d</span>' % (cls, ENG.get(e, e), lab, k, len(runs)))
            rb = []
            for i, r in enumerate(runs, 1):
                nm = named(r["answer"])
                pr = sorted(set(m.group(0) for m in PRICE.finditer(r["answer"] or "")))[:8]
                rb.append('<details class="run"><summary><b>Run %d</b> · %s · named: %s%s · %d sources</summary><div class="ans">%s</div><div class="src"><div class="k">Cited</div>%s</div></details>' % (
                    i, '<span class="y">you named</span>' if P["name"] in nm else '<span class="n">you not named</span>',
                    esc(", ".join(nm) or "no tracked brands"), (" · prices: " + esc(", ".join(pr))) if pr else "",
                    len(set(clean(u) for u in r.get("cited_urls", []))), fmt(r["answer"]), links(r.get("cited_urls", []))))
            errs = len(x.get("runs", [])) - len(runs)
            model = next((r.get("model") for r in runs if r.get("model")), "")
            bodies.append('<div class="eng"><h4>%s <span class="muted">%s</span></h4>%s%s</div>' % (
                ENG.get(e, e), esc(model), "".join(rb), ('<p class="muted">%d run(s) failed and were not counted.</p>' % errs) if errs else ""))
        br = is_branded(pid, text, prompts)
        pblocks.append('<details class="prompt"><summary><div class="pt">%s</div><div class="meta">%s · %s · %s · %s</div><div class="chips">%s</div></summary>%s</details>' % (
            esc(text), pid, "branded" if br else "non-branded", esc(p.get("intent", "")), esc(p.get("niche") or "-"),
            "".join(chips), "".join(bodies)))

    # ---- AI Overviews
    ablocks, no_aio = [], []
    for x in aio:
        q = gq.get(x["prompt_id"], {})
        alts = [a.get("query") if isinstance(a, dict) else a for a in x.get("alternatives", [])]
        alts = [a for a in alts if a]
        if x.get("aio_shown") is None:
            st, cls = "Could not be read", "none"
        elif not x.get("aio_shown"):
            st, cls = "No AI Overview", "none"
            no_aio.append((x["prompt"], alts[:3]))
        else:
            nm = P["name"] in named(x.get("answer", ""))
            cited = any(domain_of(clean(u)).endswith(P.get("domain") or "~") for u in x.get("cited_urls", []))
            st, cls = (("Named and cited", "won") if nm and cited else ("Named, not cited", "won") if nm
                       else ("Cited, not named", "mixed") if cited else ("Missing", "lost"))
        comps = [n for n in named(x.get("answer", "")) if n != P["name"]]
        ablocks.append('<details class="prompt"><summary><div class="pt">%s</div><div class="meta">%s · %s · %s</div><div class="chips"><span class="chip %s">%s</span> <span class="muted">brands named: %s</span></div></summary><div class="eng"><div class="ans">%s</div><div class="src"><div class="k">Cited in the AI Overview</div>%s</div>%s</div></details>' % (
            esc(x["prompt"]), x["prompt_id"], "branded" if is_branded(x["prompt_id"], x["prompt"], gq) else "non-branded",
            esc(q.get("intent", "")), cls, st, esc(", ".join(comps) or "none"),
            fmt(x.get("answer", "")) if x.get("aio_shown") else '<p class="muted">Google showed no AI Overview for this query.</p>',
            links(x.get("cited_urls", [])), ('<p class="muted">Related searches: %s</p>' % esc(", ".join(alts[:6]))) if alts else ""))
    no_aio_html = ('<ul class="ch">%s</ul>' % "".join("<li>%s%s</li>" % (esc(q), (" → try: " + esc(" / ".join(a))) if a else "") for q, a in no_aio)
                   if no_aio else '<p class="muted">Every query showed an AI Overview this run.</p>')

    # ---- trend series from every run file, recomputed with today's brand list
    current_synth = bool(d.get("synthetic"))
    series = {e: {} for e in engines}
    marks = {}
    for rf in files:
        rd = load_json(rf, {}) or {}
        if bool(rd.get("synthetic")) != current_synth or rd.get("date", "9999") > date:
            continue
        rdate = rd["date"]
        marks[rdate] = {"mode": rd.get("run_mode", "full")}
        for e in engines:
            if e == AIO:
                rows_ = [x for x in rd.get("results", []) if x["engine"] == AIO and x.get("aio_shown")
                         and not is_branded(x["prompt_id"], x["prompt"], gq)]
                if rows_:
                    c = collections.Counter(n for x in rows_ for n in set(named(x.get("answer", ""))))
                    series[e][rdate] = {"n": len(rows_), "named": {b: c[b] for b in tracked}}
                continue
            runs_ = [r for x in rd.get("results", []) if x["engine"] == e and not is_branded(x["prompt_id"], x["prompt"], prompts)
                     for r in x.get("runs", []) if not r.get("error")]
            if runs_:
                c = collections.Counter(n for r in runs_ for n in set(named(r["answer"])))
                series[e][rdate] = {"n": len(runs_), "named": {b: c[b] for b in tracked}}
    trend_json = json.dumps({"engines": {e: ENG.get(e, e) for e in engines}, "brands": tracked, "you": P["name"],
                             "series": series, "marks": marks, "greys": GREYS}).replace("</", "<\\/")

    # ---- facts line
    mode = d.get("run_mode", "full")
    models = {}
    for x in chat:
        for r in ok_runs(x):
            if r.get("model"):
                models.setdefault(x["engine"], set()).add(r["model"])
    model_txt = "; ".join("%s: %s" % (ENG.get(e, e), ", ".join(sorted(m))) for e, m in models.items())
    cost = d.get("cost_usd") or {}
    cost_txt = ("$%.2f on OpenRouter (%s)" % (sum(cost.values()), ", ".join("%s $%.2f" % (ENG.get(e, e), v) for e, v in cost.items()))) if cost else "not recorded"
    if mode == "full":
        runs_txt = "%s per non-branded prompt, %s per branded prompt" % (d.get("runs_per_prompt", "?"), d.get("runs_branded", d.get("runs_per_prompt", "?")))
        mode_txt = "Full run: every prompt, ChatGPT through its own chat model."
    else:
        runs_txt = "%s per prompt" % d.get("runs_per_prompt", "?")
        mode_txt = ("Weekly run: non-branded prompts only, ChatGPT through a cheaper OpenAI model. "
                    "Branded prompts and ChatGPT's own model come back in the full run.")

    # ---- Claude's analysis
    week = analysis
    hist_path = os.path.join(wd, "data", "history.json")
    history = load_json(hist_path, None)
    if history is not None and analysis:
        wk = next((w for w in history.setdefault("weeks", []) if w.get("date") == date), None)
        if wk is None:
            wk = {"date": date}
            history["weeks"].append(wk)
        wk.update({k: analysis[k] for k in ("changes", "actions", "do_today", "pricing_flags") if k in analysis})
        save_json(hist_path, history)
    elif history is not None:
        week = next((w for w in history.get("weeks", []) if w.get("date") == date), {}) or {}

    changes = "".join("<li>%s</li>" % esc(c) for c in week.get("changes", [])) or "<li>Nothing moved enough to act on.</li>"
    flags = "".join("<li>%s</li>" % esc(f if isinstance(f, str) else f.get("text", "")) for f in week.get("pricing_flags", [])) or "<li>No wrong prices this run.</li>"
    acts = "".join('<li><div class="n">%d</div><div><div class="at">%s</div><div class="muted">For %s on %s. Cited instead: %s. %s pile.</div></div></li>' % (
        i, esc(a.get("action")), esc(a.get("prompt")),
        esc(", ".join(ENG.get(e.strip(), e.strip()) for e in str(a.get("engines", a.get("engine", ""))).split(",") if e.strip())),
        esc(a.get("cited_instead")), esc(str(a.get("pile", "control")).capitalize())) for i, a in enumerate(week.get("actions", []), 1))
    if not acts:
        acts = '<li><div class="n">–</div><div class="muted">Claude adds the actions after reading the answers. Ask for them if this is empty.</div></li>'

    labels = []
    if d.get("synthetic"):
        labels.append("SYNTHETIC: a dry run with fake answers. Use it to test the setup only.")
    if any(x["engine"] == "proxy" for x in chat):
        labels.append("APPROXIMATION: some answers come from Claude's own web search, not from ChatGPT or Gemini.")
    label_html = "".join('<div class="note"><b>%s</b></div>' % esc(lab) for lab in labels)

    css = open(CSS_PATH, encoding="utf-8").read()
    route = ROUTE.get(cfg.get("run_route", "api"), cfg.get("run_route", ""))
    sub = ("Full run" if mode == "full" else "Weekly run") + ", " + date + ", " + cfg.get("category", "")
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(P['name'])} in AI answers, {date}</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600&family=Newsreader:ital,wght@0,500;1,400&display=swap" rel="stylesheet">
<style>{css}</style></head><body><main>
<div class="kicker">AI Shortlist Check</div><h1>{esc(P['name'])} in AI answers</h1>
<div class="sub">{esc(sub)}</div>
{label_html}
<div class="facts">Answers <b>{esc(route)}</b> · Engines <b>{esc(', '.join(ENG.get(e, e) for e in engines))}</b> · Prompts this run <b>{len(pblocks)}</b> · Runs <b>{esc(runs_txt)}</b> · Google queries <b>{len(aio)}</b> · SerpApi searches <b>{d.get('serpapi_searches', 0)}</b> · Cost <b>{esc(cost_txt)}</b><br>Models <b>{esc(model_txt or '-')}</b></div>
<div class="note">{esc(mode_txt)} API answers are the closest you get without the apps. A logged-in buyer can still see a different answer. Click any prompt or query to open every run, the full answer and every cited link.</div>

<section><h2>Share of voice this run</h2><p class="muted">Non-branded prompts only. A run counts when the answer names you. Read it across weeks, since one run is mostly dice.</p><div class="cards">{cards}</div></section>

<section><h2>Share of voice over time</h2><p class="muted">You next to your tracked competitors, non-branded prompts only, recounted from the stored answers with today's competitor list. Weekly shows the last 12 runs, monthly the last 12 months. Hollow points are full runs, where ChatGPT answers through its own chat model, so a jump on a full-run week can be the model.</p>
<div class="toggle"><button data-g="week" class="on">Weekly</button><button data-g="month">Monthly</button></div>
<div class="charts" id="charts"></div><p class="muted" id="trendnote"></p></section>

<section><h2>Who gets named instead</h2><p class="muted">Share of non-branded runs that name each brand. "Not tracked" brands come from the other_brands list in config.json. One that keeps beating your tracked competitors is worth swapping in.</p>
<table><thead><tr><th>Brand</th>{bhead}</tr></thead><tbody>{btab}</tbody></table></section>

<section><h2>Pages cited when you're missing</h2><p class="muted">Every link opens the exact page. Counted across non-branded runs and AI Overviews that left you out.</p>
<table><thead><tr><th>Page</th><th>Times</th><th>Engines</th><th>Prompts</th></tr></thead><tbody>{ptab or '<tr><td class="muted">None this run.</td></tr>'}</tbody></table></section>

<section><h2>Changes worth acting on</h2><ul class="ch">{changes}</ul></section>
<section><h2>Pricing flags</h2><ul class="ch">{flags}</ul></section>

<section><h2>This week's actions</h2><p class="muted">At most five, the work you control first. You decide which ones ship.</p><ol class="acts">{acts}</ol>
{('<p class="today">Do today: %s</p>' % esc(week.get('do_today'))) if week.get('do_today') else ''}</section>

<section><h2>Chat prompts, run by run</h2><p class="muted">Won: named in at least half the runs. Mixed: fewer. Lost: none. Your name is highlighted in the answers.</p>{''.join(pblocks)}</section>

<section><h2>AI Overviews, query by query</h2><p class="muted">Each query checked once. Named: the AI Overview text mentions you. Cited: your site is one of its sources.</p>{''.join(ablocks) or '<p class="muted">No Google queries this run.</p>'}
<h3>No AI Overview this run</h3>{no_aio_html}</section>

<footer>AI Shortlist Check, from The Anti-Grind SaaS Manual by Paul Ogonowski. Built from runs/{date}.json.</footer>
</main>
<script id="trend" type="application/json">{trend_json}</script>
<script>{TREND_JS}</script></body></html>"""
    out = args.out or os.path.join(wd, f"report-{date}.html")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(page)
    print(f"Wrote {out}" + ("  (SYNTHETIC data)" if d.get("synthetic") else ""))


TREND_JS = r"""
(function(){
 const T=JSON.parse(document.getElementById('trend').textContent);
 const css=n=>getComputedStyle(document.documentElement).getPropertyValue(n).trim();
 function points(eng,g){
  const s=T.series[eng]||{}; const buckets={};
  Object.keys(s).sort().forEach(d=>{const k=g==='month'?d.slice(0,7):d; const b=buckets[k]||(buckets[k]={n:0,named:{},full:false});
   b.n+=s[d].n; if((T.marks[d]||{}).mode==='full') b.full=true; T.brands.forEach(br=>b.named[br]=(b.named[br]||0)+(s[d].named[br]||0));});
  return Object.keys(buckets).sort().slice(-12).map(k=>({k,full:buckets[k].full,n:buckets[k].n,v:Object.fromEntries(T.brands.map(br=>[br,buckets[k].n?Math.round(100*buckets[k].named[br]/buckets[k].n):0]))}));
 }
 function draw(g){
  const box=document.getElementById('charts'); box.innerHTML=''; let maxPts=0;
  Object.entries(T.engines).forEach(([eng,label])=>{
   const pts=points(eng,g); maxPts=Math.max(maxPts,pts.length);
   const W=380,H=220,L=34,R=132,Tp=12,B=28,iw=W-L-R,ih=H-Tp-B;
   const x=i=>L+(pts.length<2?iw/2:i*iw/(pts.length-1)), y=v=>Tp+ih-(v/100)*ih;
   let svg=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${label} share of voice">`;
   [0,25,50,75,100].forEach(v=>{svg+=`<line x1="${L}" x2="${L+iw}" y1="${y(v)}" y2="${y(v)}" stroke="${css('--rule')}"/><text x="${L-6}" y="${y(v)+4}" text-anchor="end" font-size="10" fill="${css('--soft')}">${v}</text>`});
   const step=Math.ceil(pts.length/5);
   pts.forEach((p,i)=>{if(i%step && i!==pts.length-1) return; if(i!==pts.length-1 && pts.length-1-i<step) return; svg+=`<text x="${x(i)}" y="${H-8}" text-anchor="middle" font-size="10" fill="${css('--soft')}">${g==='month'?p.k:p.k.slice(5)}</text>`});
   const labels=[];
   T.brands.forEach((br,bi)=>{
    const you=br===T.you, col=you?css('--accent'):T.greys[(bi+2)%3];
    if(pts.length>1) svg+=`<path d="${pts.map((p,i)=>(i?'L':'M')+x(i)+','+y(p.v[br])).join(' ')}" fill="none" stroke="${col}" stroke-width="${you?2.5:1.5}"/>`;
    pts.forEach((p,i)=>{svg+=`<circle cx="${x(i)}" cy="${y(p.v[br])}" r="${you?4:3}" fill="${p.full?css('--paper'):col}" stroke="${col}" stroke-width="1.5"><title>${br}: ${p.v[br]}% (${p.k}, ${p.n} runs${p.full?', full run':''})</title></circle>`});
    if(pts.length) labels.push({br,col,you,v:pts[pts.length-1].v[br]});
   });
   labels.sort((a,b)=>b.v-a.v); let lastY=-99;
   labels.forEach(l=>{const ly=Math.max(y(l.v)+4,lastY+12); lastY=ly; svg+=`<text x="${x(pts.length-1)+8}" y="${ly}" font-size="11" fill="${l.col}" font-weight="${l.you?600:400}">${l.br} ${l.v}%</text>`});
   box.insertAdjacentHTML('beforeend',`<div class="chart"><div class="k">${label}</div>${pts.length?svg+'</svg>':'<p class="muted">No data yet.</p>'}</div>`);
  });
  document.getElementById('trendnote').textContent=maxPts<2?'Only one '+(g==='month'?'month':'run')+' so far, so each brand is a single point. The lines appear from the next run.':'';
 }
 document.querySelectorAll('.toggle button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.toggle button').forEach(x=>x.classList.toggle('on',x===b));draw(b.dataset.g)});
 draw('week');
})();
"""

if __name__ == "__main__":
    main()
