#!/usr/bin/env python3
"""AI Fix List: the pages AI cites about your product, and the outreach ledger that works them.

Reads the run files the AI Shortlist Check writes (runs/YYYY-MM-DD.json) and its config.json,
keeps its own ledger in fix-list/ledger.json. Python 3 standard library only, no API keys.

Commands
  config    weekly limit of first emails and the most you'd pay for one placement
  report    the HTML report (fix-list/report-YYYY-MM-DD.html), same look as the Shortlist Check report
  facts     snapshot your own pricing and positioning pages, flag any change since the last run
  lookup    search your own site (sitemaps, help and docs) for a claim before calling it wrong
  collect   pages cited in the newest run (or --run FILE), with the lines that name your
            product, written to fix-list/candidates-YYYY-MM-DD.json for Claude to judge
  due       what needs you this week: drafts waiting, follow-ups due, quiet periods ending
  set       update one ledger entry (status, contact, dates, notes) without hand-editing JSON
  authority Tranco rank for one or more domains (free, no key), the authority half of a price
  show      the ledger as a short table

Run from the working folder of the AI Shortlist Check (the folder with config.json and runs/).
"""
import argparse
import datetime as dt
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import parse_qsl, urlencode, urlparse, urlsplit, urlunsplit

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
FOLLOW_UP_DAYS = (7, 14, 28)      # first email on day 0, then these, the last one closes the loop
QUIET_DAYS = 90                   # no reply after the last follow-up: leave them alone this long
STATUSES = ("found", "drafted", "sent", "replied", "negotiating", "payment-requested", "approved",
            "live", "quiet", "closed")
ALIASES = {"fixed": "live", "added": "live", "paid-offer": "payment-requested", "wrong": "found", "missing": "found",
           "declined": "closed", "skip": "closed"}
CLOSE_REASONS = ("declined", "no-reply", "not-worth-it", "page-gone", "filtered", "fixed-elsewhere", "too-expensive")
MAX_ROUNDS = 2          # a first email plus its follow-ups is one round; after two silent rounds the page closes itself
STALE_DRAFT_DAYS = 14   # a draft nobody sent for this long gets "send it or close it"
STALE_FOUND_DAYS = 30   # a page waiting behind the weekly limit this long gets "still worth it?"
KINDS = {"wrong": "fix", "missing": "earn", "refresh": "earn"}   # track 1 fixes what's wrong, track 2 earns mentions
DEFAULT_SETTINGS = {"weekly_first_emails": 10, "ceiling_usd": None}
TRACKING = ("utm_", "srsltid", "gclid", "fbclid", "ref_src", "mc_cid", "mc_eid")


def today():
    return dt.date.today().isoformat()


def load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def save(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def domain_of(url):
    host = urlparse(url).netloc.lower().split("@")[-1].split(":")[0]
    return host[4:] if host.startswith("www.") else host


def clean_url(u):
    try:
        p = urlsplit(u)
    except ValueError:
        return u
    if not p.scheme.startswith("http"):
        return u
    q = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True) if not k.lower().startswith(TRACKING)]
    path = p.path or "/"
    if len(path) > 1:
        path = path.rstrip("/")
    return urlunsplit(("https", p.netloc.lower(), path, urlencode(q), ""))


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def resolve(urls, cache):
    """Gemini cites vertexaisearch redirect links. Read the Location header, never follow it."""
    todo = [u for u in urls if "vertexaisearch.cloud.google.com" in u and not cache.get(u)]
    opener = urllib.request.build_opener(_NoRedirect)

    def one(u):
        try:
            opener.open(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=15)
        except urllib.error.HTTPError as e:
            return u, e.headers.get("Location")
        except Exception:
            return u, None
        return u, None
    with ThreadPoolExecutor(8) as ex:
        for u, loc in ex.map(one, todo):
            cache[u] = loc
    return [cache.get(u) or u for u in urls]


def as_list(v):
    if isinstance(v, list):
        return v
    if isinstance(v, str) and v.startswith("["):
        return re.findall(r"'(https?://[^']+)'", v) or re.findall(r'"(https?://[^"]+)"', v)
    return []


def brand_patterns(names):
    return [re.compile(r"(?<![\w-])" + re.escape(n) + r"(?![\w-])", re.I if "." in n else 0) for n in names if n]


def page_text(raw):
    raw = re.sub(r"(?is)<(script|style|noscript|svg|nav|footer)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</(p|li|h[1-6]|tr|div|td|th)>", "\n", raw)
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    return re.sub(r"[ \t\r\f\v]+", " ", text)


def title_of(raw):
    m = re.search(r"(?is)<title[^>]*>(.*?)</title>", raw)
    return html.unescape(re.sub(r"\s+", " ", m.group(1))).strip()[:160] if m else ""


def fetch(url, cache_dir, hops=3):
    os.makedirs(cache_dir, exist_ok=True)
    path = os.path.join(cache_dir, hashlib.md5(url.encode()).hexdigest() + ".html")
    if os.path.exists(path) and os.path.getmtime(path) > time.time() - 6 * 86400:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read(), None
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en"})
        with urllib.request.urlopen(req, timeout=20) as r:
            raw = r.read(3_000_000).decode(r.headers.get_content_charset() or "utf-8", "replace")
    except urllib.error.HTTPError as e:
        loc = e.headers.get("Location")
        if e.code in (307, 308) and loc and hops:  # older Pythons don't follow 308
            raw, err = fetch(urllib.parse.urljoin(url, loc), cache_dir, hops - 1)
            if not err:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(raw)
            return raw, err
        return "", f"HTTP {e.code}"
    except Exception as e:
        return "", type(e).__name__
    with open(path, "w", encoding="utf-8") as f:
        f.write(raw)
    return raw, None


def lines_naming(text, patterns, limit=12):
    out = []
    for line in re.split(r"(?<=[.!?])\s+|\n+", text):
        line = line.strip()
        if 8 < len(line) < 400 and any(p.search(line) for p in patterns):
            if line not in out:
                out.append(line)
    return out[:limit]


def newest_run(wd):
    runs = sorted(f for f in os.listdir(os.path.join(wd, "runs")) if re.match(r"\d{4}-\d{2}-\d{2}\.json$", f))
    if not runs:
        sys.exit("No runs/YYYY-MM-DD.json here. Run the AI Shortlist Check first, or pass --run.")
    return os.path.join(wd, "runs", runs[-1])


def cmd_collect(a):
    wd = a.dir
    cfg = load(os.path.join(wd, "config.json"), {})
    prod = cfg.get("product", {})
    name = a.product or prod.get("name")
    own = a.domain or prod.get("domain", "")
    if not name:
        sys.exit("Product name missing: pass --product or run from the Shortlist Check folder.")
    names = [name] + list(prod.get("aliases", []))
    pats = brand_patterns(names)
    branded_by_id = {p.get("id"): bool(p.get("branded")) for p in cfg.get("prompts", [])}
    branded_by_id.update({q.get("id"): bool(q.get("branded")) for q in cfg.get("google_queries", []) if isinstance(q, dict)})
    comp_domains = {c.get("domain", ""): c.get("name", "") for c in cfg.get("competitors", [])}
    run_path = a.run or newest_run(wd)
    run = load(run_path, {})
    rcache_path = os.path.join(wd, "fix-list", "redirects.json")
    rcache = load(rcache_path, {})

    pages = {}
    for res in run.get("results", []):
        eng, pid, prompt = res.get("engine"), res.get("prompt_id"), res.get("prompt", "")
        branded = branded_by_id.get(pid, any(pt.search(prompt) for pt in pats))
        groups = [r.get("cited_urls") for r in res.get("runs", [])] or [res.get("cited_urls")]
        for g in groups:
            urls = resolve(as_list(g), rcache)
            for u in urls:
                if "vertexaisearch" in u:
                    continue
                u = clean_url(u)
                d = domain_of(u)
                if own and (d == own or d.endswith("." + own)):
                    continue
                p = pages.setdefault(u, {"url": u, "domain": d, "cites": 0, "engines": set(), "prompts": {}})
                p["cites"] += 1
                p["engines"].add(eng)
                p["prompts"][pid] = {"text": prompt[:140], "branded": branded}
    save(rcache_path, rcache)

    ledger = load(os.path.join(wd, "fix-list", "ledger.json"), {"schema": 1, "pages": {}})
    todo = sorted(pages.values(), key=lambda p: -p["cites"])[: a.max_pages]

    def work(p):
        raw, err = fetch(p["url"], os.path.join(wd, "fix-list", "pages"))
        text = page_text(raw) if raw else ""
        p["title"] = title_of(raw) if raw else ""
        p["fetch_error"] = err
        p["names_product"] = bool(text) and any(pt.search(text) for pt in pats)
        p["lines_naming_product"] = lines_naming(text, pats) if text else []
        p["competitor_page"] = comp_domains.get(p["domain"]) or None
        p["engines"] = sorted(x for x in p["engines"] if x)
        p["in_ledger"] = ledger["pages"].get(p["url"], {}).get("status")
        return p
    with ThreadPoolExecutor(6) as ex:
        done = list(ex.map(work, todo))

    out = {
        "date": run.get("date") or today(), "run_file": os.path.relpath(run_path, wd), "product": name,
        "own_domain": own, "pages_cited": len(pages), "pages_checked": len(done),
        "own_site_skipped": True, "pages": done,
    }
    path = os.path.join(wd, "fix-list", f"candidates-{out['date']}.json")
    save(path, out)
    new = [p for p in done if not p["in_ledger"]]
    unread = [p for p in done if p["fetch_error"]]
    print(f"{len(pages)} outside pages cited in {out['run_file']}, {len(done)} checked, "
          f"{len(new)} not in the ledger yet, {sum(p['names_product'] for p in done)} name {name}, "
          f"{len(unread)} could not be read (open those in a browser).")
    print(path)


def add_days(d, n):
    return (dt.date.fromisoformat(d) + dt.timedelta(days=n)).isoformat()


def ledger_path(d):
    return os.path.join(d, "fix-list", "ledger.json")


def load_ledger(d):
    led = load(ledger_path(d), {"schema": 2, "pages": {}})
    led.setdefault("settings", dict(DEFAULT_SETTINGS))
    for e in led["pages"].values():
        if e.get("status") in ALIASES:
            e["status"] = ALIASES[e["status"]]
    return led


def cmd_config(a):
    led = load_ledger(a.dir)
    if a.weekly is not None:
        led["settings"]["weekly_first_emails"] = a.weekly
    if a.ceiling is not None:
        led["settings"]["ceiling_usd"] = a.ceiling
    save(ledger_path(a.dir), led)
    print(json.dumps(led["settings"]))


def cmd_set(a):
    led = load_ledger(a.dir)
    url = clean_url(a.url)
    e = led["pages"].setdefault(url, {"url": url, "domain": domain_of(url), "first_seen": a.date or today(),
                                      "status": "found", "history": []})
    if a.status in ("declined", "skip") and not a.close_reason:
        a.close_reason = "declined" if a.status == "declined" else "not-worth-it"
    status = ALIASES.get(a.status, a.status)
    if status == "closed" and not a.close_reason:
        sys.exit(f"Closing needs --close-reason, one of: {', '.join(CLOSE_REASONS)}")
    if status and status not in STATUSES:
        sys.exit(f"Unknown status {a.status}. Use one of: {', '.join(STATUSES)}")
    a.status = status
    changes = {}
    for k in ("status", "kind", "title", "wrong_line", "right_line", "proof_url", "proposed_mention", "placement",
              "why_readers", "contact_name", "contact_email", "contact_source", "gmail_thread", "price_asked",
              "recommendation", "notes", "cites", "close_reason"):
        v = getattr(a, k, None)
        if v is not None:
            if k == "cites" and not str(v).isdigit():
                sys.exit("--cites takes a whole number")
            e[k] = int(v) if k == "cites" else v
            changes[k] = e[k]
    when = a.date or today()
    if changes.get("status"):
        e["status_since"] = when
    if a.status == "sent":
        e["sent_on"] = when
        e["follow_ups"] = [{"n": i + 1, "due": add_days(when, d), "done": False} for i, d in enumerate(FOLLOW_UP_DAYS)]
    if a.status == "quiet":
        e["quiet_until"] = a.quiet_until or add_days(when, QUIET_DAYS)
    if a.followup_sent:
        prev = FOLLOW_UP_DAYS[a.followup_sent - 1] if a.followup_sent <= len(FOLLOW_UP_DAYS) else 0
        for f in e.get("follow_ups", []):
            if f["n"] == a.followup_sent:
                f["done"] = when
            elif f["n"] > a.followup_sent and not f["done"]:
                f["due"] = add_days(when, FOLLOW_UP_DAYS[f["n"] - 1] - prev)
        if a.followup_sent == len(FOLLOW_UP_DAYS):
            e["rounds"] = e.get("rounds", 0) + 1
            if e["rounds"] >= MAX_ROUNDS:
                e["status"], e["status_since"], e["close_reason"] = "closed", when, "no-reply"
            else:
                e["status"], e["status_since"] = "quiet", when
                e["quiet_until"] = add_days(when, QUIET_DAYS)
    if a.status in ("replied", "negotiating", "payment-requested", "approved", "live", "closed"):
        for f in e.get("follow_ups", []):
            if not f["done"]:
                f["done"] = "cancelled"
    e["history"].append({"date": when, **changes, **({"followup_sent": a.followup_sent} if a.followup_sent else {})})
    save(ledger_path(a.dir), led)
    print(json.dumps(e, indent=2, ensure_ascii=False))


def next_step(e, t, ceiling=None):
    """(who, what, due date or None). Due dates in the past are overdue."""
    s, since = e.get("status", "found"), e.get("status_since") or e.get("first_seen") or t
    price = e.get("price_asked")
    if s == "found" and since <= add_days(t, -STALE_FOUND_DAYS):
        return ("You", f"Waiting {STALE_FOUND_DAYS}+ days behind the weekly limit: still worth an email, or close it?", t)
    if s == "found":
        return ("Claude", "Write the first email in the next run, inside the weekly limit" if e.get("contact_email") or e.get("contact_source")
                else "Find the owner and write the first email in the next run, inside the weekly limit", None)
    if s == "drafted":
        if since <= add_days(t, -STALE_DRAFT_DAYS):
            return ("You", f"Draft unsent for {STALE_DRAFT_DAYS}+ days: send it or close it", add_days(since, 2))
        return ("You", "Read the draft in Gmail and click send", add_days(since, 2))
    if s == "sent":
        nxt = next((f for f in e.get("follow_ups", []) if not f["done"]), None)
        if nxt:
            return ("You", f"Send follow-up {nxt['n']} of {len(FOLLOW_UP_DAYS)} (Claude drafts it that week)", nxt["due"])
        return ("Claude", "Mark it quiet", t)
    if s == "replied":
        return ("You", "Answer their reply (Claude drafts it)", add_days(since, 2))
    if s == "negotiating":
        return ("You", "Agree terms" + (f", they asked {price}" if price else ""), add_days(since, 3))
    if s == "payment-requested":
        rec = e.get("recommendation") or "Claude prices it against your ceiling"
        return ("You", f"Decide: pay {price or '?'}? {rec}", add_days(since, 3))
    if s == "approved":
        return ("You", "Pay, send the copy, then Claude checks the page is live", add_days(since, 7))
    if s == "live":
        return ("Claude", "Recheck the page on the next full run", None)
    if s == "quiet":
        return ("Claude", "Second and last round: open the page again, new email or close", e.get("quiet_until"))
    return ("", "Nothing", None)


def cmd_facts(a):
    """Snapshot the founder's own source pages (pricing, plans, positioning) and say what changed since last time."""
    wd = a.dir
    path = os.path.join(wd, "fix-list", "facts-sources.json")
    src = load(path, {"pages": {}})
    for u in a.add or []:
        src["pages"].setdefault(clean_url(u), {})
    for u in a.remove or []:
        src["pages"].pop(clean_url(u), None)
    if not src["pages"]:
        sys.exit("No source pages yet. Add them: facts --add [pricing page URL] [other page URL]")
    changed = []
    snap_dir = os.path.join(wd, "fix-list", "facts-snapshots")
    os.makedirs(snap_dir, exist_ok=True)
    for u, meta in src["pages"].items():
        cache = os.path.join(wd, "fix-list", "pages-fresh")
        f = os.path.join(cache, hashlib.md5(u.encode()).hexdigest() + ".html")
        if os.path.exists(f):
            os.remove(f)  # always fetch fresh, the 6-day page cache is for other people's pages
        raw, err = fetch(u, cache)
        if err:
            print(f"{u}: could not read ({err}), facts unchanged")
            continue
        text = re.sub(r"\s+", " ", page_text(raw)).strip()
        h = hashlib.sha256(text.encode()).hexdigest()[:16]
        old = meta.get("hash")
        snap = os.path.join(snap_dir, f"{hashlib.md5(u.encode()).hexdigest()[:10]}-{today()}-{time.strftime('%H%M%S')}.txt")
        if h != old:
            with open(snap, "w", encoding="utf-8") as fh:
                fh.write(text)
            prev = meta.get("snapshot")
            meta.update(hash=h, snapshot=os.path.relpath(snap, wd), changed=today(), previous=prev)
            if old:
                changed.append(u)
                print(f"CHANGED {u}: compare {prev} with {meta['snapshot']}")
            else:
                print(f"first snapshot {u}")
        else:
            print(f"same {u} (unchanged since {meta.get('changed')})")
        meta["checked"] = today()
    save(path, src)
    if changed:
        print("Facts may be out of date. Read both snapshots, update facts.md with the founder, then recheck the ledger.")


def sitemap_urls(domain, limit=400):
    """Every URL in the product's own sitemaps (sitemap index followed one level), main site plus
    the usual help and docs subdomains."""
    seen, out = set(), []
    hosts = [domain, "www." + domain, "help." + domain, "support." + domain, "docs." + domain]
    todo = [f"https://{h}/sitemap.xml" for h in hosts]
    while todo and len(out) < limit:
        sm = todo.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        try:
            req = urllib.request.Request(sm, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=15) as r:
                xml = r.read(5_000_000).decode("utf-8", "replace")
        except Exception:
            continue
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
        if "<sitemapindex" in xml:
            todo.extend(locs)
        else:
            out.extend(u for u in locs if domain in urlparse(u).netloc)
    return list(dict.fromkeys(out))[:limit]


def cmd_lookup(a):
    """Search the product's own site for a claim before calling it wrong or asking the founder."""
    wd = a.dir
    cfg = load(os.path.join(wd, "config.json"), {})
    domain = a.domain or (cfg.get("product") or {}).get("domain")
    if not domain:
        sys.exit("No product domain: pass --domain or run from the Shortlist Check folder.")
    terms = [t.lower() for t in a.terms]
    src = load(os.path.join(wd, "fix-list", "facts-sources.json"), {"pages": {}})
    urls = list(src["pages"]) + sitemap_urls(domain, a.max_pages)
    urls = list(dict.fromkeys(urls))[: a.max_pages]
    cache = os.path.join(wd, "fix-list", "own-pages")

    def one(u):
        raw, err = fetch(u, cache)
        if err or not raw:
            return u, []
        text = page_text(raw)
        hits = []
        for line in re.split(r"(?<=[.!?])\s+|\n+", text):
            l = line.strip()
            if 8 < len(l) < 400 and all(t in l.lower() for t in terms):
                hits.append(l)
        return u, hits[:3]
    with ThreadPoolExecutor(8) as ex:
        results = [r for r in ex.map(one, urls) if r[1]]
    print(f"Searched {len(urls)} pages on {domain} for: {' + '.join(a.terms)}")
    if not results:
        print("Not found on your own site. Ask the founder before you call the claim wrong or right.")
    results.sort(key=lambda r: ("/blog" in r[0], -len(r[1])))  # product, pricing, help and docs pages before the blog
    for u, hits in results[:12]:
        print(f"\n{u}")
        for h in hits:
            print(f"  - {h[:300]}")


def cmd_due(a):
    led = load_ledger(a.dir)
    t = a.date or today()
    rows = []
    for e in led["pages"].values():
        who, what, due = next_step(e, t, led["settings"].get("ceiling_usd"))
        if e.get("status") in ("closed", "live") or not what or what == "Nothing":
            continue
        if e.get("status") == "quiet" and (due or "9999") > t:
            continue
        if e.get("status") == "sent" and due and due > t:
            continue
        rows.append((due or t, who, what, e))
    rows.sort(key=lambda r: r[0])
    print(f"Fix List, {t}. Weekly limit: {led['settings'].get('weekly_first_emails')} first emails.")
    for due, who, what, e in rows:
        late = " OVERDUE" if due < t else ""
        print(f"  [{who}] {due}{late}  {e['domain']} ({KINDS.get(e.get('kind'), '?')}, {e.get('status')}): {what}")
    waiting = [e for e in led["pages"].values() if e.get("status") == "sent" and (next_step(e, t)[2] or "0") > t]
    print(f"Sent and waiting, nothing due yet: {len(waiting)}")
    if a.json:
        print(json.dumps([{"due": d, "who": w, "what": x, "url": e["url"]} for d, w, x, e in rows], ensure_ascii=False))


def cmd_show(a):
    led = load_ledger(a.dir)
    rows = sorted(led["pages"].values(), key=lambda e: (KINDS.get(e.get("kind"), "z"), e.get("status", ""), -int(e.get("cites", 0))))
    print(f"{'track':<5} {'status':<18} {'cites':>5}  page")
    for e in rows:
        print(f"{KINDS.get(e.get('kind'), '?'):<5} {e.get('status', ''):<18} {e.get('cites', ''):>5}  {e['url']}")


def cmd_authority(a):
    out = {}
    for i, d in enumerate(a.domains):
        if i:
            time.sleep(1.2)  # Tranco's free API allows about one request a second
        d = domain_of("https://" + d) if "://" not in d else domain_of(d)
        try:
            req = urllib.request.Request(f"https://tranco-list.eu/api/ranks/domain/{d}", headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=15) as r:
                ranks = json.load(r).get("ranks", [])
            out[d] = ranks[0]["rank"] if ranks else "not in the top million"
        except Exception as e:
            out[d] = f"lookup failed ({type(e).__name__})"
        print(f"{d}: {out[d]}")
    if a.json:
        print(json.dumps(out))


def esc(x):
    return html.escape(str(x if x is not None else ""))


STATUS_LABEL = {"found": "Found", "drafted": "Draft ready", "sent": "Sent", "replied": "Replied",
                "negotiating": "Negotiating", "payment-requested": "Payment asked", "approved": "Approved",
                "live": "Live", "quiet": "Quiet", "closed": "Closed"}
STATUS_ORDER = {k: n for n, k in enumerate(("payment-requested", "negotiating", "replied", "drafted", "approved", "found",
                                            "sent", "quiet", "live", "closed"))}
REPORT_CSS = """
.pill{display:inline-block;font:600 11px 'DM Sans';letter-spacing:.04em;text-transform:uppercase;padding:2px 8px;border-radius:10px;border:1px solid;white-space:nowrap}
.s-found{color:var(--soft);border-color:var(--rule)}
.s-drafted{color:#9A6512;border-color:#D9A54A;background:#F6E7C8}
.s-sent{color:#35536E;border-color:#8FA9C0;background:#E3EAF1}
.s-replied{color:#24695C;border-color:#7DB3A6;background:#DCEDE8}
.s-negotiating,.s-payment-requested{color:var(--accent);border-color:var(--accent);background:#F3DCD8}
.s-approved{color:#3F6B31;border-color:#8DB37E;background:#E3EEDC}
.s-live{color:#fff;border-color:#4A7C3A;background:#4A7C3A}
.s-quiet{color:var(--soft);border-color:var(--rule);border-style:dashed}
.s-closed{color:var(--soft);border-color:var(--rule);text-decoration:line-through}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .s-drafted{color:#E8B65C;background:#3A2E18;border-color:#7A5A22}
:root:not([data-theme="light"]) .s-sent{color:#A9C2D8;background:#1F2A35;border-color:#46607A}
:root:not([data-theme="light"]) .s-replied{color:#8FCBBC;background:#1B2D29;border-color:#3F6F64}
:root:not([data-theme="light"]) .s-negotiating,:root:not([data-theme="light"]) .s-payment-requested{background:#3A201D}
:root:not([data-theme="light"]) .s-approved{color:#A9CF98;background:#22301D;border-color:#4F7341}}
.late{color:var(--accent);font-weight:600}.who{font:600 11px 'DM Sans';letter-spacing:.06em;text-transform:uppercase;color:var(--soft)}
.line{font-size:14px}.line s{color:var(--soft)}td.pg a{word-break:normal}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:14px 0}
.bar button{font:600 13px 'DM Sans';background:none;border:1px solid var(--rule);color:var(--soft);padding:5px 12px;border-radius:14px;cursor:pointer}
.bar button.on{border-color:var(--ink);color:var(--ink);background:var(--sand)}.bar button b{font-weight:600;margin-left:4px}
.bar input{font:14px 'DM Sans';padding:6px 10px;border:1px solid var(--rule);border-radius:14px;background:var(--paper);color:var(--ink);min-width:220px;margin-left:auto}
th[data-k]{cursor:pointer;user-select:none}th[data-k]::after{content:" ↕";color:var(--rule)}th.asc::after{content:" ↑";color:var(--ink)}th.desc::after{content:" ↓";color:var(--ink)}
.trk{font:600 11px 'DM Sans';text-transform:uppercase;letter-spacing:.06em}.trk.fix{color:var(--accent)}.trk.earn{color:var(--ink)}
.count{color:var(--soft);font-size:13px;margin-top:8px}
@media(max-width:760px){.hide-m{display:none}.bar input{margin-left:0;width:100%}}
"""

REPORT_JS = r"""
const rows=[...document.querySelectorAll('#pages tbody tr')];let view='open',track='all',q='',sk='due',sd=1,lim=20;
const T=document.body.dataset.today;
function show(r){const st=r.dataset.status,d=r.dataset;
 if(track!=='all'&&d.track!==track)return false;
 if(q&&!d.text.includes(q))return false;
 if(view==='open')return st!=='closed'&&st!=='live';
 if(view==='you')return d.who==='You'&&st!=='closed'&&st!=='live';
 if(view==='late')return d.late==='1';
 if(view==='paid')return ['negotiating','payment-requested','approved'].includes(st);
 if(view==='live')return st==='live';
 if(view==='closed')return st==='closed';
 return true}
function draw(){const tb=document.querySelector('#pages tbody');
 rows.sort((a,b)=>{let x=a.dataset[sk],y=b.dataset[sk];if(sk==='cites'){x=+x;y=+y}return (x>y?1:x<y?-1:0)*sd});
 let n=0;rows.forEach(r=>{tb.appendChild(r);const v=show(r);if(v)n++;r.style.display=(v&&n<=lim)?'':'none'});
 const m=document.getElementById('more');m.style.display=n>lim?'':'none';m.textContent='Show all '+n;
 document.getElementById('count').textContent=Math.min(n,lim)+' of '+n+' shown, '+rows.length+' pages in the ledger';
 document.querySelectorAll('th[data-k]').forEach(th=>th.className=th.dataset.k===sk?(sd>0?'asc':'desc'):'')}
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>{view=b.dataset.view;document.querySelectorAll('[data-view]').forEach(x=>x.classList.toggle('on',x===b));draw()});
document.querySelectorAll('[data-track]').forEach(b=>b.onclick=()=>{track=b.dataset.track;document.querySelectorAll('[data-track]').forEach(x=>x.classList.toggle('on',x===b));draw()});
document.querySelectorAll('th[data-k]').forEach(th=>th.onclick=()=>{if(sk===th.dataset.k)sd=-sd;else{sk=th.dataset.k;sd=th.dataset.k==='cites'?-1:1}draw()});
document.getElementById('q').oninput=e=>{q=e.target.value.toLowerCase();draw()};
document.getElementById('more').onclick=()=>{lim=1e9;draw()};
document.querySelectorAll('[data-view],[data-track]').forEach(b=>b.addEventListener('click',()=>{lim=20;draw()}));
document.querySelectorAll('[data-go]').forEach(a=>a.onclick=e=>{e.preventDefault();document.querySelector('[data-view="'+a.dataset.go+'"]').click();document.getElementById('all').scrollIntoView()});
draw();
"""


def cmd_report(a):
    wd, t = a.dir, a.date or today()
    led = load_ledger(wd)
    cfg = load(os.path.join(wd, "config.json"), {})
    name = (cfg.get("product") or {}).get("name") or "Your product"
    pages = list(led["pages"].values())
    notes = load(os.path.join(wd, "fix-list", f"notes-{t}.json"), {})
    css = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates", "report.css"), encoding="utf-8").read() + REPORT_CSS
    shortlist = sorted(f for f in os.listdir(wd) if re.match(r"report-\d{4}-\d{2}-\d{2}\.html$", f))
    sl_link = (f'<a href="../{shortlist[-1]}">AI Shortlist Check report, {shortlist[-1][7:17]}</a>' if shortlist
               else "the AI Shortlist Check report")
    ceiling = led["settings"].get("ceiling_usd")
    limit = led["settings"].get("weekly_first_emails")

    def pill(st):
        return f'<span class="pill s-{esc(st)}">{esc(STATUS_LABEL.get(st, st))}</span>'

    trs, counts = [], {"open": 0, "you": 0, "late": 0, "paid": 0, "live": 0, "closed": 0}
    for e in pages:
        st = e.get("status", "found")
        who, what, due = next_step(e, t, ceiling)
        trk = KINDS.get(e.get("kind"), "earn")
        is_open = st not in ("closed", "live")
        late = bool(is_open and due and due < t and who)
        counts["open"] += is_open
        counts["you"] += is_open and who == "You"
        counts["late"] += late
        counts["paid"] += st in ("negotiating", "payment-requested", "approved")
        counts["live"] += st == "live"
        counts["closed"] += st == "closed"
        if trk == "fix":
            detail = f'<div class="line"><s>{esc(e.get("wrong_line"))}</s><br>{esc(e.get("right_line"))}</div>'
        else:
            detail = (f'<div class="line">{esc(e.get("proposed_mention") or "Mention to propose")}'
                      + (f'<br><span class="muted">Where: {esc(e.get("placement"))}</span>' if e.get("placement") else "") + "</div>")
        if st == "payment-requested" or st == "negotiating":
            detail += f'<div class="line"><b>Asked {esc(e.get("price_asked") or "?")}</b>. {esc(e.get("recommendation") or "")}</div>'
        if st == "closed":
            step = f'<span class="muted">Closed {esc(e.get("status_since"))}: {esc((e.get("close_reason") or "").replace("-", " "))}</span>'
        elif st == "live":
            step = f'<span class="muted">Live since {esc(e.get("status_since"))}. Rechecked on the next full run.</span>'
        elif what and what != "Nothing":
            when = (f'<span class="{"late" if late else "muted"}">{"overdue since " if late else "by "}{esc(due)}</span>' if due else "")
            step = f'<span class="who">{esc(who)}</span> {esc(what)}<br>{when}'
        else:
            step = '<span class="muted">-</span>'
        title = e.get("title") or e["domain"]
        text = " ".join(str(e.get(k, "")) for k in ("title", "domain", "wrong_line", "proposed_mention", "contact_name")).lower()
        trs.append(
            f'<tr data-status="{esc(st)}" data-track="{trk}" data-who="{esc(who)}" data-late="{int(late)}" '
            f'data-due="{esc(due or "9999")}" data-cites="{esc(e.get("cites", 0))}" data-st="{STATUS_ORDER.get(st, 9)}" '
            f'data-page="{esc(title.lower())}" data-text="{esc(text)}">'
            f'<td class="pg"><a href="{esc(e["url"])}">{esc(title)}</a><div class="meta">{esc(e["domain"])} · cited {esc(e.get("cites", "?"))}x</div></td>'
            f'<td class="num0">{esc(e.get("cites", 0))}x</td><td><span class="trk {trk}">{trk}</span></td><td class="hide-m">{detail}</td><td>{pill(st)}</td><td>{step}</td></tr>')

    you = sorted(((d or "9999", w, x, e) for e in pages if e.get("status") not in ("closed", "live")
                  for (x, w, d) in [next_step(e, t, ceiling)] if x == "You"), key=lambda r: r[0])
    top = "".join(f'<li><div class="n">{i}</div><div><div class="at">{esc(w)}</div><div class="muted">{esc(e.get("title") or e["domain"])} · '
                  f'{("<span class=late>overdue since " + esc(d) + "</span>") if d < t else "by " + esc(d)}</div></div></li>'
                  for i, (d, w, x, e) in enumerate(you[:8], 1)) \
        or '<li><div class="n">-</div><div class="muted">Nothing waits on you this week.</div></li>'
    more = (f'<p class="muted"><a href="#all" data-go="you">All {len(you)} in the table below</a></p>' if len(you) > 8 else "")
    fix_open = sum(1 for e in pages if KINDS.get(e.get("kind")) == "fix" and e.get("status") not in ("closed", "live"))
    earn_open = sum(1 for e in pages if KINDS.get(e.get("kind")) == "earn" and e.get("status") not in ("closed", "live"))
    sent_week = sum(1 for e in pages if e.get("sent_on") and e["sent_on"] > add_days(t, -7) and not e.get("rounds"))

    def lst(key, empty):
        items = notes.get(key) or []
        return '<ul class="ch">' + ("".join(f"<li>{esc(x)}</li>" for x in items) or f'<li class="muted">{esc(empty)}</li>') + "</ul>"

    cards = "".join(f'<div class="card"><div class="k">{k}</div><div class="big">{v}</div><div class="muted">{m}</div></div>' for k, v, m in [
        ("Fix: wrong lines open", fix_open, "track 1"),
        ("Earn: mentions to get", earn_open, "track 2"),
        ("First emails this week", f"{sent_week}<span>/{limit}</span>", "your weekly limit"),
        ("Live", counts["live"], "fixed or added, checked on the page")])
    btn = lambda v, label, on="": f'<button data-view="{v}" class="{on}">{label}<b>{counts.get(v, len(pages))}</b></button>'
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(name)} on other people's pages, {t}</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600&family=Newsreader:ital,wght@0,500;1,400&display=swap" rel="stylesheet">
<style>{css}</style></head><body data-today="{t}"><main>
<div class="kicker">AI Fix List</div><h1>{esc(name)} on other people's pages</h1>
<div class="sub">Week of {t}</div>
<div class="facts">Pages from <b>{sl_link}</b> · Pages in the ledger <b>{len(pages)}</b> · Weekly limit <b>{limit} first emails</b> · Most you'd pay for a placement <b>{esc(("$" + str(ceiling)) if ceiling is not None else "not set")}</b></div>
<div class="note">Two tracks run side by side. Fix: pages that get a fact about you wrong. Earn: lists and comparisons AI cites for your buyers' questions where you're missing or out of date. Claude drafts every email, you send them. A page closes itself after two rounds with no reply, or when you close it.</div>
<section><h2>This week</h2><div class="cards">{cards}</div></section>
<section><h2>Waiting on you</h2><p class="muted">The next {min(8, len(you))} of {len(you)}, oldest due date first. Overdue in red.</p><ol class="acts">{top}</ol>{more}</section>
<section id="all"><h2>Every page</h2><p class="muted">Click a column to sort. Closed and live pages sit behind their own buttons, so the open list stays short.</p>
<div class="bar">{btn("open", "Open", "on")}{btn("you", "On you")}{btn("late", "Overdue")}{btn("paid", "Paid offers")}{btn("live", "Live")}{btn("closed", "Closed")}{btn("all", "All")}</div>
<div class="bar"><button data-track="all" class="on">Both tracks</button><button data-track="fix">Fix</button><button data-track="earn">Earn</button><input id="q" placeholder="Search page, domain, line, contact"></div>
<table id="pages"><thead><tr><th data-k="page">Page</th><th data-k="cites">Cited</th><th>Track</th><th class="hide-m">Wrong / right or proposed mention</th><th data-k="st">Status</th><th data-k="due">Next step</th></tr></thead><tbody>{"".join(trs)}</tbody></table>
<p class="count" id="count"></p><div class="bar"><button id="more">Show all</button></div></section>
<section><h2>Fix on your own site first</h2>{lst("own_site", "Your own pages agree with each other.")}</section>
<section><h2>Earned, not email</h2><p class="muted">Reddit, forums and videos AI cites. Worth your time, not an email.</p>{lst("earned", "None this week.")}</section>
<section><h2>Skipped by the filters</h2>{lst("filtered", "Nothing filtered this week.")}</section>
<section><h2>Pages Claude couldn't open</h2>{lst("unread", "Every page opened.")}</section>
<footer>AI Fix List, from The Anti-Grind SaaS Manual by Paul Ogonowski. Built from fix-list/ledger.json.</footer>
</main><script>{REPORT_JS}</script></body></html>"""
    out = os.path.join(wd, "fix-list", f"report-{t}.html")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(page)
    print(f"Wrote {out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=".", help="the AI Shortlist Check working folder")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collect")
    c.add_argument("--run")
    c.add_argument("--product")
    c.add_argument("--domain")
    c.add_argument("--max-pages", type=int, default=200)
    s = sub.add_parser("set")
    s.add_argument("url")
    s.add_argument("--status")
    s.add_argument("--kind", choices=sorted(KINDS))
    s.add_argument("--cites")
    for k in ("title", "wrong-line", "right-line", "proof-url", "proposed-mention", "placement", "why-readers",
              "contact-name", "contact-email", "contact-source", "gmail-thread", "price-asked", "recommendation",
              "notes", "date"):
        s.add_argument("--" + k)
    s.add_argument("--followup-sent", type=int)
    s.add_argument("--close-reason", choices=CLOSE_REASONS)
    s.add_argument("--quiet-until", help="YYYY-MM-DD, default 90 days after --date")
    cf = sub.add_parser("config")
    cf.add_argument("--weekly", type=int, help="first emails a week, setup offers 5, 10, 20 or 30, any number works")
    cf.add_argument("--ceiling", type=int, help="USD for one placement for a year, 0 = never pay")
    d = sub.add_parser("due")
    d.add_argument("--date")
    d.add_argument("--json", action="store_true")
    sub.add_parser("show")
    lk = sub.add_parser("lookup")
    lk.add_argument("terms", nargs="+", help="words that must all appear in one sentence, e.g. agency plan")
    lk.add_argument("--domain")
    lk.add_argument("--max-pages", type=int, default=150)
    fa = sub.add_parser("facts")
    fa.add_argument("--add", nargs="+")
    fa.add_argument("--remove", nargs="+")
    r = sub.add_parser("report")
    r.add_argument("--date")
    au = sub.add_parser("authority")
    au.add_argument("domains", nargs="+")
    au.add_argument("--json", action="store_true")
    a = ap.parse_args()
    {"collect": cmd_collect, "set": cmd_set, "due": cmd_due, "show": cmd_show, "authority": cmd_authority,
     "config": cmd_config, "report": cmd_report, "facts": cmd_facts, "lookup": cmd_lookup}[a.cmd](a)


if __name__ == "__main__":
    main()
