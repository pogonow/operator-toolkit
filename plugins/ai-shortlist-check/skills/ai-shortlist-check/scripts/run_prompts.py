#!/usr/bin/env python3
"""AI Shortlist Check: run buyer prompts through AI engines that search the web.

Standard library only. Run from anywhere:

    python3 run_prompts.py --workdir [working folder] [--mode auto|weekly|full] [--runs N] [--dry-run]
    python3 run_prompts.py --workdir [working folder] --mode full --runs 1 --limit 3 --tag test --no-history
    python3 run_prompts.py --workdir [working folder] --check-keys
    python3 run_prompts.py [--workdir [working folder]] --suggest-queries [--seeds "seed 1" "seed 2"]

Reads   [workdir]/config.json          (format: templates/config.example.json)
Reads   [workdir]/.env if it exists     (KEY=VALUE lines, only the key names below)
Writes  [workdir]/runs/YYYY-MM-DD.json  (raw answers and cited URLs, every run)
Appends [workdir]/data/history.json     (one row per prompt or query, engine and date)

Two lists live in config.json. "prompts" are conversational chat prompts for ChatGPT
and Gemini. A weekly run asks the non-branded ones runs_weekly times (default 2) with
the cheaper weekly ChatGPT model. A full run, every full_every_days (default 28), asks
every prompt: non-branded runs_full times (3), branded runs_branded_full times (2). "google_queries" are short Google searches for
the ai_overviews engine, run once per week through SerpApi whatever --runs says.

Keys (environment variables or the .env file, never printed, never in config.json):
    OPENROUTER_API_KEY  default route for the chat engines. Each engine maps to a model
                        slug in config "openrouter_models" (a list is tried in order
                        when a model is refused).
    SERPAPI_API_KEY     Google AI Overviews through SerpApi.
    OPENAI_API_KEY      fallback for chatgpt   (OpenAI Responses API, web_search tool)
    GEMINI_API_KEY      fallback for gemini    (generateContent, Google Search grounding)
    PERPLEXITY_API_KEY  fallback for perplexity, an engine added only on request (Sonar)
With OPENROUTER_API_KEY set, every chat engine goes through OpenRouter. Without it,
each chat engine uses its direct key. An engine with no usable key is skipped and named.

--suggest-queries pulls Google autocomplete (free, no key) for seeds taken from
--seeds or built from config (category, niches, competitors, "autocomplete_seeds")
and prints deduplicated candidates for the Google query list.

Request shapes checked against the vendors' docs on 2026-10-20:
  * OpenRouter: POST https://openrouter.ai/api/v1/chat/completions,
    Authorization: Bearer [key], body {model, messages, plugins: [{"id": "web"}]}.
    With no engine set, the web plugin uses the provider's native search for OpenAI,
    Google, Perplexity and Anthropic models (Exa for others). Citations arrive as
    message.annotations[] of type "url_citation" with url_citation.url. The parser
    also reads a top-level "citations" list. UNVERIFIED in a live call (no key here).
    Default slugs, checked on https://openrouter.ai/api/v1/models on 2026-10-20:
    chatgpt  openai/gpt-chat-latest (OpenAI's chat-latest alias, the Instant model
             used in ChatGPT), then openai/gpt-5.5 if refused
    gemini   google/gemini-3.8-flash
    on request only: perplexity perplexity/sonar, claude anthropic/claude-sonnet-5.5
  * SerpApi (https://serpapi.com/search-api, /ai-overview, /google-ai-overview-api):
    GET https://serpapi.com/search.json?engine=google&q=..&gl=..&hl=..&google_domain=..
    &api_key=.. returns "ai_overview" {text_blocks[], references[{title, link, snippet,
    source, index}]} when Google shows one. Sometimes ai_overview holds only
    "page_token" and "serpapi_link": the overview then needs a second request,
    GET ...?engine=google_ai_overview&page_token=..&api_key=.., made at once because
    the token expires within 1 minute. The script counts it as a second search (the
    docs don't say outright). "related_searches"[].query and "related_questions"[].
    question feed the suggested swap for a query with no AI Overview, so no extra
    searches. Account check: GET https://serpapi.com/account.json (free, no search).
    Pricing checked on https://serpapi.com/pricing: free plan 250 searches a month,
    50 an hour. Only successful searches count. UNVERIFIED in a live call.
  * Google autocomplete: GET https://suggestqueries.google.com/complete/search
    ?client=firefox&q=[seed] returns ["seed", ["suggestion", ...], ...]. No key.
  * OpenAI direct: POST https://api.openai.com/v1/responses, tools [{"type": "web_search"}],
    include ["web_search_call.action.sources"]. Citations are url_citation annotations
    on output_text. Default model OPENAI_MODEL or gpt-5.5. (Checked 2026-10-19.)
  * Perplexity direct: POST https://api.perplexity.ai/v1/sonar, model "sonar". Reads the
    old chat shape and the newer Agent shape. Falls back to /chat/completions on a 404.
    UNVERIFIED in a live call. (Checked 2026-10-19.)
  * Gemini direct: POST .../v1beta/models/{model}:generateContent with
    tools [{"google_search": {}}]. groundingChunks[].web.uri is a Google redirect, so the
    domain comes from web.title. Default model GEMINI_MODEL or gemini-3.8-flash.
If a vendor changed its shape, the run records the error for that engine and goes on.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import parse_qsl, urlencode, urlparse, urlsplit, urlunsplit

ENGINES = {
    "chatgpt": {"name": "ChatGPT", "key": "OPENAI_API_KEY", "label": "ChatGPT (OpenAI API, web search)"},
    "gemini": {"name": "Gemini", "key": "GEMINI_API_KEY", "label": "Gemini (API, Google Search grounding)"},
    "perplexity": {"name": "Perplexity", "key": "PERPLEXITY_API_KEY", "label": "Perplexity (Sonar API)"},
    "claude": {"name": "Claude", "key": None, "label": ""},  # OpenRouter only
}
AIO = "ai_overviews"  # Google AI Overviews through SerpApi, one check per query a week
SERPAPI_KEY = "SERPAPI_API_KEY"
SERPAPI_URL = "https://serpapi.com/search.json"
AUTOCOMPLETE_URL = "https://suggestqueries.google.com/complete/search"
DEFAULT_ENGINES = ["chatgpt", "gemini", AIO]
OPENROUTER_KEY = "OPENROUTER_API_KEY"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODELS = {
    "chatgpt": ["openai/gpt-chat-latest", "openai/gpt-5.5"],
    "gemini": ["google/gemini-3.8-flash"],
    "perplexity": ["perplexity/sonar"],
    "claude": ["anthropic/claude-sonnet-5.5"],
}
# Cost, measured on real calls on 2026-10-21 (3 prompts, OpenRouter usage.cost):
#   openai/gpt-chat-latest  ~$0.09-0.15 per answer. 13-21k input tokens of injected search
#                           results. web_search_options.search_context_size low and medium
#                           gave the same tokens and cost, so the script doesn't send it.
#   openai/gpt-6-luna       ~$0.03-0.04 per answer, mostly the search fee. Same core brands.
#   google/gemini-3.8-flash ~$0.03 per answer, mostly the grounding fee. With reasoning
#                           effort low every answer came back with its sources.
# So the weekly light run uses Luna for ChatGPT and the full run every 28 days uses the
# real ChatGPT model, which also re-checks that Luna still names the same brands.
OPENROUTER_WEB_DEFAULT = {}
OPENROUTER_CONTEXT_DEFAULT = None
OPENROUTER_MODELS_WEEKLY = {"chatgpt": ["openai/gpt-6-luna", "openai/gpt-chat-latest"]}
OPENROUTER_PARAMS_DEFAULT = {"gemini": {"reasoning": {"effort": "low"}}}
RUNS_WEEKLY_DEFAULT = 2   # weekly light run
RUNS_FULL_DEFAULT = 3     # full run, every FULL_EVERY_DAYS
RUNS_BRANDED_DEFAULT = 2  # branded prompts in the full run
FULL_EVERY_DAYS = 28
KEY_NAMES = (OPENROUTER_KEY, SERPAPI_KEY, "OPENAI_API_KEY", "GEMINI_API_KEY", "PERPLEXITY_API_KEY")
CHAT_DIRECT_KEYS = ("OPENAI_API_KEY", "GEMINI_API_KEY", "PERPLEXITY_API_KEY")

# First guess at a cited domain's type. Claude asks the founder about the most cited "other" ones.
REVIEW_SITES = ("g2.com", "capterra.com", "trustradius.com", "getapp.com",
                "softwareadvice.com", "trustpilot.com", "gartner.com", "sourceforge.net",
                "producthunt.com", "saasworthy.com")
FORUMS = ("reddit.com", "quora.com", "news.ycombinator.com", "stackexchange.com",
          "stackoverflow.com", "indiehackers.com")
VIDEO = ("youtube.com", "youtu.be", "vimeo.com")
LISTICLE_HINTS = ("best-", "/best", "top-", "/top", "alternatives", "-vs-", "/vs/", "compared")


# ---------------------------------------------------------------- helpers

def today():
    return dt.date.today().isoformat()


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def load_env_file(wd):
    """Read KEY=VALUE lines for the known key names from [workdir]/.env.
    A variable already set in the environment wins. Values are never printed."""
    path = os.path.join(wd, ".env")
    if not os.path.exists(path):
        return []
    found = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("export "):
                line = line[7:].strip()
            if "=" not in line or line.startswith("#"):
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k in KEY_NAMES and v and not os.environ.get(k):
                os.environ[k] = v
                found.append(k)
    return found


def domain_of(url):
    try:
        host = urlparse(url).netloc.lower()
    except ValueError:
        return ""
    host = host.split("@")[-1].split(":")[0]
    return host[4:] if host.startswith("www.") else host


def match_domain(host, domains):
    return any(host == d or host.endswith("." + d) for d in domains if d)


MARKETPLACES = ("apps.shopify.com", "marketplace.atlassian.com", "appexchange.salesforce.com",
                "ecosystem.hubspot.com", "workspace.google.com", "zapier.com/apps", "chromewebstore.google.com")


def classify(url, product, competitors, cfg=None):
    """Source type of a cited URL. Order: the founder's own labels in config "source_types"
    ({domain: type}), your site, tracked competitor, other vendor (a domain in config
    "other_brands"), review site or app store, Reddit or forum, YouTube, docs or help,
    listicle or comparison, other."""
    cfg = cfg or {}
    host = domain_of(url)
    try:
        path = urlparse(url).path.lower() if url.startswith("http") else ""
    except ValueError:
        path = ""
    own = cfg.get("source_types") or {}
    for d, t in own.items():
        if match_domain(host, [d]):
            return t
    if match_domain(host, [product.get("domain", "")]):
        return "your site"
    if match_domain(host, [c.get("domain", "") for c in competitors]):
        return "tracked competitor"
    if match_domain(host, [b.get("domain", "") for b in cfg.get("other_brands", [])]):
        return "other vendor"
    if match_domain(host, REVIEW_SITES) or any((host + path).startswith(m) for m in MARKETPLACES):
        return "review site or app store"
    if match_domain(host, FORUMS) or host.startswith(("community.", "forum.", "forums.")):
        return "Reddit or forum"
    if match_domain(host, VIDEO):
        return "YouTube"
    if host.startswith(("docs.", "help.", "support.")) or "/docs" in path or "/help" in path:
        return "docs or help"
    if any(h in path for h in LISTICLE_HINTS) or re.search(r"compare|comparison|review", path):
        return "listicle or comparison"
    return "other"


TRACKING_PARAMS = ("utm_", "srsltid", "gclid", "fbclid", "ref_src", "mc_cid", "mc_eid")


def clean_url(u):
    """Drop tracking parameters (utm_source=openai and friends), the fragment, a trailing
    slash and www-case noise, so the same page counts once and the link opens clean."""
    try:
        p = urlsplit(u)
    except ValueError:
        return u
    if not p.scheme.startswith("http"):
        return u
    q = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
         if not k.lower().startswith(TRACKING_PARAMS)]
    path = p.path or "/"
    if len(path) > 1:
        path = path.rstrip("/")
    return urlunsplit(("https", p.netloc.lower(), path, urlencode(q), ""))


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def resolve_redirects(urls, cache):
    """Gemini cites Google redirect links (vertexaisearch.cloud.google.com/grounding-api-
    redirect/...). Read the Location header of each one, without following it, so the report
    shows the real page. Results are cached in the run file. A failure keeps the redirect."""
    todo = [u for u in urls if "vertexaisearch.cloud.google.com" in u and u not in cache]
    if todo:
        opener = urllib.request.build_opener(_NoRedirect)

        def one(u):
            try:
                opener.open(urllib.request.Request(u, method="GET"), timeout=15)
            except urllib.error.HTTPError as e:
                return u, e.headers.get("Location")
            except Exception:
                return u, None
            return u, None
        with ThreadPoolExecutor(8) as ex:
            for u, loc in ex.map(one, todo):
                cache[u] = loc
    return [cache.get(u) or u for u in urls]


def brand_patterns(brand):
    names = [brand["name"]] + list(brand.get("aliases", []))
    # Names match case-sensitively (Aspire, Archive, Later are also plain words), anything
    # with a dot (a domain) case-insensitively.
    return [re.compile(r"(?<![\w-])" + re.escape(n) + r"(?![\w-])", re.I if "." in n else 0)
            for n in names if n]


def first_index(text, patterns):
    hits = [m.start() for p in patterns for m in [p.search(text)] if m]
    return min(hits) if hits else None


PRICE_RE = re.compile(r"([$€£]\s?\d[\d,.]*|\d[\d,.]*\s?(?:USD|EUR|GBP|dollars|euros))", re.I)


def price_snippets(text, patterns):
    out = []
    for sentence in re.split(r"(?<=[.!?\n])\s+", text):
        if PRICE_RE.search(sentence) and any(p.search(sentence) for p in patterns):
            out.append(sentence.strip()[:240])
    return out[:3]


def ordinal(n):
    return {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")


# ---------------------------------------------------------------- HTTP

def post_json(url, payload, headers, timeout=240, retries=4, retry_after_send=False):
    """POST JSON. Retries only what was never billed: HTTP 429 (rate limit, exponential
    backoff 10s, 20s, 40s, 80s) and 5xx (the provider failed, OpenRouter bills nothing). A timeout or
    a dropped connection is NOT retried unless retry_after_send=True, because the engine
    may have answered and billed the call already. The run records the error and moves on."""
    body = json.dumps(payload).encode("utf-8")
    last = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=body, method="POST",
                                     headers={"Content-Type": "application/json", **headers})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:500]
            last = RuntimeError(f"HTTP {e.code}: {detail}")
            last.code = e.code
            # OpenRouter bills only completed answers, so a provider 5xx is safe to ask again.
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                wait = 10 * (2 ** attempt)
                ra = e.headers.get("Retry-After") if e.headers else None
                if ra and ra.isdigit():
                    wait = max(wait, int(ra))
                time.sleep(min(wait, 120))
                continue
            raise last
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = RuntimeError(f"network: {e}")
            last.code = None
            if retry_after_send and attempt < retries:
                time.sleep(5 * (attempt + 1))
                continue
            raise last
    raise last


def get_json(url, params, timeout=90, retries=2, secret=None):
    """GET url?params and parse JSON. A secret in params never shows up in an error."""
    full = url + "?" + urlencode(params)
    last = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(full, headers={"User-Agent": "ai-shortlist-check/3"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read()
                charset = r.headers.get_content_charset() or "utf-8"
                return json.loads(raw.decode(charset, "replace"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:300]
            last = RuntimeError(f"HTTP {e.code}: {detail}")
            last.code = e.code
            if e.code in (500, 502, 503, 504) and attempt < retries:
                time.sleep(3 * (attempt + 1))
                continue
            break
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            last = RuntimeError(f"network: {e}")
            last.code = None
            if attempt < retries:
                time.sleep(3 * (attempt + 1))
                continue
            break
    if secret:
        code = getattr(last, "code", None)
        last = RuntimeError(str(last).replace(secret, "[key]"))
        last.code = code
    raise last


# ---------------------------------------------------------------- AI Overviews

AIO_SKIP_KEYS = {"link", "links", "thumbnail", "serpapi_link", "image", "images", "video",
                 "source", "snippet_links", "reference_indexes", "snippet_highlighted_words",
                 "snippet_latex", "type", "page_token", "references", "products",
                 "header_images", "error", "product_labels", "favicon"}


def aio_text(node):
    """All readable text inside an ai_overview block: text_blocks with their nested
    lists, tables, expandable and comparison blocks. Links and images are skipped."""
    out = []

    def walk(n):
        if isinstance(n, str):
            if n.strip() and not n.startswith("http"):
                out.append(n.strip())
        elif isinstance(n, list):
            for x in n:
                walk(x)
        elif isinstance(n, dict):
            for k, v in n.items():
                if k not in AIO_SKIP_KEYS:
                    walk(v)
    walk((node or {}).get("text_blocks") or [])
    return "\n".join(out)


def aio_refs(node):
    urls = []
    for r in (node or {}).get("references") or []:
        u = r.get("link") if isinstance(r, dict) else None
        if isinstance(u, str) and u.startswith("http"):
            urls.append(u)
    return list(dict.fromkeys(urls))


def related_candidates(data):
    """Close variants from the same SerpApi response, so a swap costs no extra search."""
    rs = [r.get("query") for r in data.get("related_searches") or [] if isinstance(r, dict)]
    rq = [r.get("question") for r in data.get("related_questions") or [] if isinstance(r, dict)]
    return ([("related_searches", q) for q in rs if isinstance(q, str) and q.strip()] +
            [("related_questions", q) for q in rq if isinstance(q, str) and q.strip()])


def parse_serp(data):
    """Read one google-engine SerpApi response.
    Returns (state, node, page_token): state is "shown", "none", "token" or "error"."""
    node = data.get("ai_overview")
    if not isinstance(node, dict):
        return "none", None, None
    if node.get("text_blocks"):
        return "shown", node, None
    if node.get("page_token"):
        return "token", node, node["page_token"]
    if node.get("error"):
        return "error", node, None
    return "none", None, None


def ask_ai_overview(query, serp_cfg, key, get=None):
    """One Google search through SerpApi, plus the google_ai_overview request when the
    overview comes as a page_token. Returns a dict with shown (True, False or None),
    text, urls, alternatives, searches and error."""
    get = get or get_json
    params = {"engine": "google", "q": query, "api_key": key}
    for k in ("gl", "hl", "google_domain", "location"):
        if serp_cfg.get(k):
            params[k] = serp_cfg[k]
    data = get(SERPAPI_URL, params, secret=key)
    searches = 1
    status = (data.get("search_metadata") or {}).get("status")
    if data.get("error") and status != "Success" and not data.get("organic_results"):
        if "hasn't returned any results" not in str(data["error"]):
            raise RuntimeError(f"SerpApi error: {str(data['error'])[:200]}")
    alts = related_candidates(data)
    state, node, token = parse_serp(data)
    error = None
    if state == "token":
        try:
            data2 = get(SERPAPI_URL, {"engine": "google_ai_overview", "page_token": token,
                                      "api_key": key}, secret=key)
            searches += 1
            state, node, _ = parse_serp(data2)
            if state == "token":
                state, error = "error", "second request returned another page_token"
            elif state == "none" and data2.get("error"):
                state, error = "error", str(data2["error"])[:200]
        except RuntimeError as e:
            state, error = "error", f"second request failed: {str(e)[:200]}"
    if state == "error" and not error:
        error = str((node or {}).get("error"))[:200]
    shown = {"shown": True, "none": False}.get(state)
    return {"shown": shown, "text": aio_text(node) if shown else "",
            "urls": aio_refs(node) if shown else [], "alternatives": alts,
            "searches": searches, "error": error}


def _tokens(q):
    return set(re.findall(r"[a-z0-9]+", q.lower()))


def pick_swap(query, candidates, taken):
    """Pick the candidate closest to the query that isn't on the list yet.
    candidates: list of (source, text). Related searches win over related questions."""
    base, seen = _tokens(query), {t.strip().lower() for t in taken}
    best, best_score = None, 0.0
    order = {"related_searches": 0.02, "autocomplete": 0.01, "related_questions": 0.0}
    for src, text in candidates:
        t = text.strip()
        if not t or t.lower() in seen or t.lower() == query.strip().lower():
            continue
        tok = _tokens(t)
        if not tok:
            continue
        score = len(base & tok) / len(base | tok) + order.get(src, 0) - 0.01 * max(0, len(tok) - 8)
        if score > best_score:
            best, best_score = {"query": t, "from": src}, score
    return best


def parse_autocomplete(raw, charset="utf-8"):
    """Google autocomplete (client=firefox) returns ["seed", ["s1", "s2", ...], ...]."""
    if isinstance(raw, bytes):
        raw = raw.decode(charset or "utf-8", "replace")
    data = json.loads(raw)
    if isinstance(data, list) and len(data) > 1 and isinstance(data[1], list):
        return [x for x in data[1] if isinstance(x, str)]
    return []


def autocomplete(seed, hl="en", gl="", timeout=15):
    params = {"client": "firefox", "q": seed, "hl": hl or "en"}
    if gl:
        params["gl"] = gl
    req = urllib.request.Request(AUTOCOMPLETE_URL + "?" + urlencode(params),
                                 headers={"User-Agent": "Mozilla/5.0 (ai-shortlist-check)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return parse_autocomplete(r.read(), r.headers.get_content_charset() or "utf-8")


def seeds_from_config(cfg):
    cat = (cfg.get("category") or "").strip()
    seeds = []
    if cat:
        seeds += [cat, f"best {cat}", f"{cat} pricing"]
        seeds += [f"{cat} for {n}" for n in cfg.get("niches", []) if n]
    for c in cfg.get("competitors", []):
        if c.get("name"):
            seeds += [f"{c['name']} alternatives", f"{c['name']} vs", f"{c['name']} pricing"]
    seeds += [x for x in cfg.get("autocomplete_seeds", []) if x]
    return list(dict.fromkeys(s for s in seeds if "[" not in s))


def suggest_queries(seeds, hl, gl, existing, fetch=None):
    """Print autocomplete suggestions per seed and one deduplicated candidate list.
    Never fails the process on a network error."""
    fetch = fetch or autocomplete
    if not seeds:
        print("No seeds. Pass --seeds or put category, niches and competitors in config.json.")
        return []
    have = {e.strip().lower() for e in existing}
    pool, failed = [], []
    for seed in seeds:
        try:
            sugg = fetch(seed, hl, gl)
        except Exception as e:  # network blocked, timeout, bad JSON
            failed.append((seed, str(e)[:120]))
            continue
        print(f"\n{seed}")
        for x in sugg:
            print(f"  {x}")
        pool += [seed] + sugg
        time.sleep(0.2)
    seen, out = set(), []
    for q in pool:
        k = re.sub(r"\s+", " ", q.strip().lower())
        if k and k not in seen and k not in have:
            seen.add(k)
            out.append(re.sub(r"\s+", " ", q.strip()))
    if failed:
        print(f"\nAutocomplete failed for {len(failed)} of {len(seeds)} seeds:")
        for seed, why in failed:
            print(f"  {seed}: {why}")
    if not out:
        print("\nGoogle autocomplete could not be reached from here. Build the list from the "
              "founder's words and the patterns in references/ai-overviews.md.")
        return []
    print(f"\n{len(out)} candidates (deduplicated, already listed queries left out):")
    for i, q in enumerate(out, 1):
        print(f"{i:>3}. {q}")
    return out


# ---------------------------------------------------------------- engines

def ask_chatgpt(prompt):
    key = os.environ["OPENAI_API_KEY"]
    payload = {
        "model": os.environ.get("OPENAI_MODEL", "gpt-5.5"),
        "tools": [{"type": "web_search"}],
        "input": prompt,
        "include": ["web_search_call.action.sources"],
    }
    headers = {"Authorization": f"Bearer {key}"}
    try:
        data = post_json("https://api.openai.com/v1/responses", payload, headers)
    except RuntimeError as e:
        if getattr(e, "code", None) == 400:  # older accounts may reject the include field
            payload.pop("include")
            data = post_json("https://api.openai.com/v1/responses", payload, headers)
        else:
            raise
    text, urls = [], []
    for item in data.get("output", []) or []:
        if item.get("type") == "message":
            for c in item.get("content", []) or []:
                if c.get("type") == "output_text":
                    text.append(c.get("text", ""))
                    for a in c.get("annotations", []) or []:
                        if a.get("type") == "url_citation" and a.get("url"):
                            urls.append(a["url"])
        elif item.get("type") == "web_search_call":
            for s in ((item.get("action") or {}).get("sources") or []):
                u = s.get("url") if isinstance(s, dict) else s
                if isinstance(u, str) and u.startswith("http"):
                    urls.append(u)
    if not text and isinstance(data.get("output_text"), str):
        text.append(data["output_text"])
    return "\n".join(text), urls


def ask_perplexity(prompt):
    key = os.environ["PERPLEXITY_API_KEY"]
    payload = {"model": os.environ.get("PERPLEXITY_MODEL", "sonar"),
               "messages": [{"role": "user", "content": prompt}]}
    headers = {"Authorization": f"Bearer {key}"}
    url = os.environ.get("PERPLEXITY_URL", "https://api.perplexity.ai/v1/sonar")
    try:
        data = post_json(url, payload, headers)
    except RuntimeError as e:
        if getattr(e, "code", None) == 404:
            data = post_json("https://api.perplexity.ai/chat/completions", payload, headers)
        else:
            raise
    text, urls = [], []
    for ch in data.get("choices", []) or []:  # chat-completions shape
        text.append(((ch.get("message") or {}).get("content")) or "")
    urls += [u for u in data.get("citations", []) or [] if isinstance(u, str)]
    urls += [r.get("url") for r in data.get("search_results", []) or [] if r.get("url")]
    for item in data.get("output", []) or []:  # Agent API shape
        if item.get("type") == "search_results":
            urls += [r.get("url") for r in item.get("results", []) or [] if r.get("url")]
        elif item.get("type") == "message":
            for c in item.get("content", []) or []:
                if c.get("type") in ("output_text", "text"):
                    text.append(c.get("text", ""))
    return "\n".join(t for t in text if t), urls


def ask_gemini(prompt):
    key = os.environ["GEMINI_API_KEY"]
    model = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "tools": [{"google_search": {}}]}
    data = post_json(url, payload, {"x-goog-api-key": key})
    text, urls = [], []
    for cand in data.get("candidates", []) or []:
        for part in ((cand.get("content") or {}).get("parts") or []):
            if part.get("text"):
                text.append(part["text"])
        for ch in ((cand.get("groundingMetadata") or {}).get("groundingChunks") or []):
            web = ch.get("web") or {}
            uri, title = web.get("uri", ""), (web.get("title") or "").strip()
            # uri is a Google redirect; title is usually the source domain
            if title and "." in title and " " not in title:
                urls.append("https://" + title.lower())
            elif uri:
                urls.append(uri)
        break
    return "\n".join(text), urls


ASK = {"chatgpt": ask_chatgpt, "perplexity": ask_perplexity, "gemini": ask_gemini}


def openrouter_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):  # content parts
        return "\n".join(p.get("text", "") for p in content if isinstance(p, dict))
    return ""


def usage_of(data):
    """Token counts and the billed cost OpenRouter returns with each answer."""
    u = data.get("usage") or {}
    det = u.get("completion_tokens_details") or {}
    pdet = u.get("prompt_tokens_details") or {}
    try:
        cost = float(u.get("cost")) if u.get("cost") is not None else None
    except (TypeError, ValueError):
        cost = None
    return {"prompt_tokens": u.get("prompt_tokens"), "completion_tokens": u.get("completion_tokens"),
            "reasoning_tokens": det.get("reasoning_tokens"), "cached_tokens": pdet.get("cached_tokens"),
            "cost": cost}


def ask_openrouter(prompt, models, web, context=None, extra=None):
    """POST to OpenRouter chat completions with the web plugin. Tries each model slug
    in order and moves on when OpenRouter refuses a slug (HTTP 400 or 404).
    Returns (answer, urls, model, usage)."""
    headers = {"Authorization": f"Bearer {os.environ[OPENROUTER_KEY]}",
               "X-OpenRouter-Title": "AI Shortlist Check"}
    last = None
    for model in models:
        payload = {"model": model, "messages": [{"role": "user", "content": prompt}],
                   "plugins": [dict({"id": "web"}, **(web or {}))],
                   "usage": {"include": True}}
        if context:
            payload["web_search_options"] = {"search_context_size": context}
        payload.update(extra or {})
        try:
            data = post_json(OPENROUTER_URL, payload, headers)
        except RuntimeError as e:
            last = e
            if getattr(e, "code", None) in (400, 404):
                continue
            raise
        if isinstance(data.get("error"), dict):
            last = RuntimeError(f"OpenRouter error: {str(data['error'])[:300]}")
            continue
        text, urls = [], []
        for ch in data.get("choices", []) or []:
            msg = ch.get("message") or {}
            text.append(openrouter_text(msg.get("content")))
            for a in msg.get("annotations", []) or []:
                if a.get("type") == "url_citation":
                    u = (a.get("url_citation") or {}).get("url") or a.get("url")
                    if isinstance(u, str) and u.startswith("http"):
                        urls.append(u)
        msg = data.get("message") or {}  # shape shown in the web search docs example
        for a in msg.get("annotations", []) or []:
            u = (a.get("url_citation") or {}).get("url")
            if isinstance(u, str) and u.startswith("http"):
                urls.append(u)
        urls += [u for u in data.get("citations", []) or [] if isinstance(u, str)]
        return "\n".join(t for t in text if t), urls, data.get("model") or model, usage_of(data)
    raise last or RuntimeError("no OpenRouter model configured for this engine")


# ---------------------------------------------------------------- dry run

def fake_answer(prompt, product, competitors, rng, p_product, category):
    brands = [c["name"] for c in competitors]
    for c in competitors:
        if rng.random() < 0.35:
            brands.remove(c["name"])
    if rng.random() < p_product:
        brands.insert(rng.randrange(len(brands) + 1), product["name"])
    filler = [f"Synthetic Tool {chr(65 + i)}" for i in range(rng.randint(1, 3))]
    names = brands + filler
    rng.shuffle(names)
    lines = [f"SYNTHETIC TEST ANSWER (dry run, not a real engine). For \"{prompt}\":"]
    lines += [f"{i}. {n}: a fit for teams that need {category}." for i, n in enumerate(names, 1)]
    if product["name"] in names and rng.random() < 0.25:
        lines.append(f"{product['name']} starts at ${rng.choice(range(19, 400, 10))} per user per month.")
    pool = [
        f"https://www.g2.com/categories/{category.replace(' ', '-')}",
        "https://www.reddit.com/r/SaaS/comments/synthetic",
        "https://www.youtube.com/watch?v=synthetic",
        f"https://bestlists.example/best-{category.replace(' ', '-')}-tools",
        "https://industry-news.example/report",
    ] + [f"https://{c['domain']}/vs/{product['name'].lower()}" for c in competitors if c.get("domain")]
    if product.get("domain"):
        pool.append(f"https://{product['domain']}/pricing")
    urls = rng.sample(pool, k=min(len(pool), rng.randint(2, 4)))
    return "\n".join(lines), urls


def fake_aio(query, idx, product, competitors, rng, p_product, category):
    """SYNTHETIC AI Overview for a dry run. Every third query never gets one, so the
    no-AI-Overview list, the swaps and the streak flag have something to show."""
    alts = [("related_searches", f"{query} for small teams"),
            ("related_searches", f"best {query}"),
            ("related_questions", f"What is the best {category} for {query.split()[0]}?")]
    searches = 2 if rng.random() < 0.4 else 1
    if idx % 3 == 2 or rng.random() < 0.15:
        return {"shown": False, "text": "", "urls": [], "alternatives": alts,
                "searches": 1, "error": None}
    text, urls = fake_answer(query, product, competitors, rng, p_product, category)
    return {"shown": True, "text": text.replace("SYNTHETIC TEST ANSWER", "SYNTHETIC AI OVERVIEW"),
            "urls": urls, "alternatives": alts, "searches": searches, "error": None}


def no_aio_streak(history_rows, query, date, shown):
    """Weeks in a row, this one included, with no AI Overview for this query text.
    Weeks where the overview could not be read (None) neither count nor break it."""
    if shown is not False:
        return 0
    past = sorted((r for r in history_rows if r.get("engine") == AIO and r["date"] < date
                   and r.get("prompt", "").strip().lower() == query.strip().lower()),
                  key=lambda r: r["date"], reverse=True)
    n = 1
    for r in past:
        if r.get("aio_shown") is None:
            continue
        if r.get("aio_shown") is False:
            n += 1
        else:
            break
    return n


# ---------------------------------------------------------------- main

def analyse(answer, urls, product, competitors, prompt=""):
    pp = brand_patterns(product)
    order = []
    p_idx = first_index(answer, pp)
    if p_idx is not None:
        order.append((p_idx, product["name"]))
    comps = {}
    for c in competitors:
        pats = brand_patterns(c)
        idx = first_index(answer, pats)
        # A brand named in the prompt itself ("[competitor] alternatives") is not counted
        # for that prompt, since the answer names it because the buyer did.
        comps[c["name"]] = None if first_index(prompt, pats) is not None else idx is not None
        if idx is not None:
            order.append((idx, c["name"]))
    order.sort()
    if p_idx is None:
        position = "not named"
    else:
        pos = [n for _, n in order].index(product["name"]) + 1
        position = f"named {ordinal(pos)} of {len(order)} tracked brands in this run"
    return p_idx is not None, position, comps, price_snippets(answer, pp)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--workdir", default=".")
    ap.add_argument("--runs", type=int, default=None, help="runs per prompt (default: config or 3)")
    ap.add_argument("--date", default=None, help="date to file the run under (default: today)")
    ap.add_argument("--dry-run", action="store_true", help="write a SYNTHETIC run, no API calls")
    ap.add_argument("--engines", default=None, help="comma list, overrides config")
    ap.add_argument("--limit", type=int, default=None, help="only the first N prompts (for a small test run)")
    ap.add_argument("--mode", choices=("auto", "weekly", "full"), default="auto",
                    help="weekly: non-branded prompts, 2 runs. full: every prompt, 3 runs. "
                         "auto (default): full when the last full run is 28+ days old, else weekly")
    ap.add_argument("--prompt-ids", default=None, help="comma list of prompt and query ids to run (test)")
    ap.add_argument("--model", action="append", default=[],
                    help="engine=slug to override the OpenRouter model, e.g. chatgpt=openai/gpt-6-luna")
    ap.add_argument("--search-context", choices=("low", "medium", "high", "off"), default=None,
                    help="OpenRouter web_search_options.search_context_size (default: not sent, no effect measured)")
    ap.add_argument("--max-results", type=int, default=None, help="web plugin max_results (default: not sent)")
    ap.add_argument("--runs-branded", type=int, default=None,
                    help="runs per branded prompt in the full run (default: config or 2)")
    ap.add_argument("--tag", default="", help="suffix for the run file name, keeps test runs apart")
    ap.add_argument("--no-history", action="store_true", help="write the run file only (test runs)")
    ap.add_argument("--check-keys", action="store_true", help="say which keys are set, never their values")
    ap.add_argument("--suggest-queries", action="store_true",
                    help="print Google autocomplete candidates for the AI Overview query list (no key)")
    ap.add_argument("--seeds", nargs="+", default=None, help="seeds for --suggest-queries")
    args = ap.parse_args()

    wd = os.path.abspath(args.workdir)
    from_env_file = load_env_file(wd)
    if args.suggest_queries:
        cfg = load_json(os.path.join(wd, "config.json"), {}) or {}
        serp = cfg.get("serpapi") or {}
        seeds = args.seeds or seeds_from_config(cfg)
        existing = [q.get("text", "") for q in cfg.get("google_queries", [])]
        suggest_queries(seeds, serp.get("hl", "en"), serp.get("gl", ""), existing)
        return
    if args.check_keys:
        for k in KEY_NAMES:
            where = " (from .env)" if k in from_env_file else ""
            print(f"{k}: {'set' + where if os.environ.get(k) else 'missing'}")
        if os.environ.get(OPENROUTER_KEY):
            print("Chat engines: OpenRouter for ChatGPT and Gemini.")
        elif any(os.environ.get(k) for k in CHAT_DIRECT_KEYS):
            print("Chat engines: direct keys, engines without a key get skipped.")
        else:
            print("Chat engines: no key yet. The no-key route still works.")
        if os.environ.get(SERPAPI_KEY):
            key = os.environ[SERPAPI_KEY]
            try:  # the account endpoint is free and uses no search
                acc = get_json("https://serpapi.com/account.json", {"api_key": key}, timeout=20,
                               retries=0, secret=key)
                print(f"AI Overviews: SerpApi key works. Plan {acc.get('plan_name', '?')}, "
                      f"{acc.get('plan_searches_left', acc.get('total_searches_left', '?'))} searches "
                      f"left this month.")
            except Exception as e:
                print(f"AI Overviews: SerpApi key set, account check failed ({str(e)[:120]}).")
        else:
            print("AI Overviews: no SerpApi key yet. Google queries get checked by hand.")
        return
    cfg = load_json(os.path.join(wd, "config.json"), None)
    if not cfg:
        sys.exit(f"No config.json in {wd}. Copy templates/config.example.json there and fill it in.")
    product, competitors = cfg["product"], cfg.get("competitors", [])
    prompts = cfg.get("prompts", [])
    gqueries = cfg.get("google_queries", [])
    for i, pr in enumerate(prompts, 1):
        pr.setdefault("id", f"P{i}")
    for i, gq in enumerate(gqueries, 1):
        gq.setdefault("id", f"G{i}")
    date = args.date or today()

    # Weekly light run or full run. Branded prompts are won or lost slowly and don't count
    # toward share of voice, so they run only in the full run.
    hist_path = os.path.join(wd, "data", "history.json")
    history = load_json(hist_path, {"schema": 1, "meta": {}, "rows": [], "weeks": []})
    mode = args.mode
    if mode == "auto":
        fulls = sorted(w.get("date") for w in history.get("weeks", []) if w.get("run_mode") == "full")
        if not fulls and history["rows"]:
            fulls = sorted({r["date"] for r in history["rows"] if r.get("branded") and r["engine"] != AIO})
        try:
            age = (dt.date.fromisoformat(date[:10]) - dt.date.fromisoformat(fulls[-1][:10])).days
        except (IndexError, ValueError):
            age = None
        mode = "full" if age is None or age >= int(cfg.get("full_every_days", FULL_EVERY_DAYS)) else "weekly"
    if mode == "weekly":
        prompts = [p for p in prompts if not (p.get("branded")
                   or first_index(p["text"], brand_patterns(product)) is not None)]
        runs_n = args.runs or cfg.get("runs_weekly", RUNS_WEEKLY_DEFAULT)
    else:
        runs_n = args.runs or cfg.get("runs_full", cfg.get("runs_per_prompt", RUNS_FULL_DEFAULT))
    # Branded prompts run only in the full run, at fewer runs: the founder wins or loses them
    # slowly and they don't count toward share of voice. --runs sets both for a test run.
    runs_branded = args.runs_branded or args.runs or cfg.get("runs_branded_full", RUNS_BRANDED_DEFAULT)
    if args.prompt_ids:
        ids = {x.strip() for x in args.prompt_ids.split(",")}
        prompts = [p for p in prompts if p["id"] in ids]
        gqueries = [q for q in gqueries if q["id"] in ids]
    if args.limit:
        prompts = prompts[: args.limit]
        gqueries = gqueries[: args.limit]
    wanted = (args.engines.split(",") if args.engines else cfg.get("engines", DEFAULT_ENGINES))
    wanted = [e.strip() for e in wanted]
    run_aio = AIO in wanted
    wanted = [e for e in wanted if e != AIO]
    if run_aio and not gqueries:
        print("Skipped ai_overviews: no google_queries in config.json")
        run_aio = False
    elif run_aio and not args.dry_run and not os.environ.get(SERPAPI_KEY):
        print(f"Skipped ai_overviews: no {SERPAPI_KEY} set")
        run_aio = False

    use_or = bool(os.environ.get(OPENROUTER_KEY))
    or_models = dict(OPENROUTER_MODELS)
    for e, m in (cfg.get("openrouter_models") or {}).items():
        or_models[e] = [m] if isinstance(m, str) else list(m)
    if mode == "weekly":
        weekly = dict(OPENROUTER_MODELS_WEEKLY)
        for e, m in (cfg.get("openrouter_models_weekly") or {}).items():
            weekly[e] = [m] if isinstance(m, str) else list(m)
        or_models.update(weekly)
    for spec in args.model:
        e, _, slug = spec.partition("=")
        if slug:
            or_models[e.strip()] = [slug.strip()]
    web = dict(OPENROUTER_WEB_DEFAULT, **(cfg.get("openrouter_web") or {}))
    if args.max_results:
        web["max_results"] = args.max_results
    context = args.search_context or cfg.get("openrouter_search_context") or OPENROUTER_CONTEXT_DEFAULT
    context = None if context == "off" else context
    or_params = dict(OPENROUTER_PARAMS_DEFAULT)
    for e, p in (cfg.get("openrouter_params") or {}).items():
        or_params[e] = p

    engines, skipped, via = [], {}, {}
    for e in wanted:
        if e not in ENGINES:
            skipped[e] = "no API in this script, paste answers by hand"
        elif args.dry_run:
            engines.append(e)
            has_direct = ENGINES[e]["key"] and os.environ.get(ENGINES[e]["key"])
            via[e] = "direct" if has_direct and not use_or else "openrouter"
        elif use_or and or_models.get(e):
            engines.append(e)
            via[e] = "openrouter"
        elif ENGINES[e]["key"] and os.environ.get(ENGINES[e]["key"]):
            engines.append(e)
            via[e] = "direct"
        else:
            need = OPENROUTER_KEY + (f" or {ENGINES[e]['key']}" if ENGINES[e]["key"] else "")
            skipped[e] = f"no {need} set"

    if args.dry_run:
        real = [r for r in history["rows"] if not r.get("synthetic")]
        if real:
            sys.exit("This history holds real runs. Run --dry-run in a scratch folder instead.")
    elif any(r.get("synthetic") for r in history["rows"]):
        sys.exit("This history holds SYNTHETIC dry-run rows. Use a fresh working folder for real runs.")

    synthetic_weeks = len({r["date"] for r in history["rows"] if r.get("synthetic")})
    seed = int(hashlib.sha256(f"{date}|{product['name']}".encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)

    # Resume: a run file for this date (and tag) that already holds answers is reused, so a
    # crash or a restart never pays twice for the same answer. Errors are asked again.
    run_file = os.path.join(wd, "runs", f"{date}{('-' + args.tag) if args.tag else ''}.json")
    done = {}
    prev = (load_json(run_file, {}) or {}) if not args.dry_run else {}
    resolved = dict(prev.get("resolved_urls") or {})
    if not args.dry_run:
        for r in prev.get("results", []):
            if r.get("engine") == AIO:
                continue
            for k, x in enumerate(r.get("runs", [])):
                if not x.get("error") and x.get("answer"):
                    done[(r["engine"], r["prompt_id"], k)] = x
        if done:
            print(f"Resuming: {len(done)} answers already in {os.path.basename(run_file)}, not asked again.")

    def checkpoint(results_so_far, complete=False):
        save_json(run_file, {"synthetic": bool(args.dry_run), "complete": complete,
                             "date": date, "run_mode": mode, "runs_per_prompt": runs_n,
                             "runs_branded": runs_branded, "search_context": context, "web": web,
                             "resolved_urls": resolved, "results": results_so_far})

    print(f"AI Shortlist Check run {date} ({mode}): {len(prompts)} prompts x {runs_n} runs"
          + (f", {len(gqueries)} Google queries x 1" if run_aio else ""))
    print("Engines: " + (", ".join([f"{e} (via {via[e]})" for e in engines]
                                   + (["ai_overviews (via serpapi)"] if run_aio else [])) or "none"))
    for e, why in skipped.items():
        print(f"Skipped {e}: {why}")
    if not engines and not run_aio:
        sys.exit("Nothing to run. Set OPENROUTER_API_KEY and SERPAPI_API_KEY, use --dry-run or paste answers by hand.")

    results, new_rows = [], []
    for e in engines:
        for i, pr in enumerate(prompts, 1):
            pid = pr.get("id") or f"P{i}"
            # A prompt that names the product is branded, whatever the config says.
            branded = bool(pr.get("branded")) or first_index(pr["text"], brand_patterns(product)) is not None
            run_list = []
            entry = {"engine": e, "via": via[e], "prompt_id": pid, "prompt": pr["text"], "runs": run_list}
            results.append(entry)
            n_runs = runs_branded if (branded and mode == "full") else runs_n
            for k in range(n_runs):
                if (e, pid, k) in done:
                    run_list.append(done[(e, pid, k)])
                    continue
                try:
                    model, usage = None, None
                    if args.dry_run:
                        p = min(0.85, 0.2 + 0.12 * synthetic_weeks + (0.5 if branded else 0))
                        ans, urls = fake_answer(pr["text"], product, competitors, rng, p,
                                                cfg.get("category", "software"))
                    elif via[e] == "openrouter":
                        ans, urls, model, usage = ask_openrouter(pr["text"], or_models[e], web,
                                                                 context, or_params.get(e))
                    else:
                        ans, urls = ASK[e](pr["text"])
                    if not args.dry_run:
                        urls = resolve_redirects(urls, resolved)
                    urls = [clean_url(u) for u in urls]
                    run_list.append({"answer": ans, "cited_urls": list(dict.fromkeys(urls)),
                                     "model": model, "usage": usage, "error": None})
                except Exception as ex:  # record and go on
                    run_list.append({"answer": "", "cited_urls": [], "error": str(ex)[:500]})
                    print(f"  {e} {pid} run {k + 1}: {str(ex)[:120]}")
                if not args.dry_run:
                    checkpoint(results)

            ok = [r for r in run_list if not r["error"]]
            mentioned, position, prices = [], [], []
            comp_counts = {c["name"]: (None if first_index(pr["text"], brand_patterns(c)) is not None else 0)
                           for c in competitors}
            counts = {}
            for r in ok:
                m, pos, comps, pz = analyse(r["answer"], r["cited_urls"], product, competitors, pr["text"])
                mentioned.append(m)
                position.append(pos)
                prices += pz
                for name, hit in comps.items():
                    if comp_counts[name] is not None:
                        comp_counts[name] += int(bool(hit))
                for u in r["cited_urls"]:
                    d = domain_of(u)
                    if d:
                        c = counts.setdefault(d, {"domain": d, "type": classify(u, product, competitors, cfg),
                                                  "count": 0, "example": u})
                        c["count"] += 1
            sources = sorted(counts.values(), key=lambda s: -s["count"])
            if via[e] == "openrouter":
                slug = ", ".join(sorted({r["model"] for r in ok if r.get("model")})) or or_models[e][0]
                label = f"{ENGINES[e]['name']} via OpenRouter ({slug}, web search)"
            else:
                label = ENGINES[e]["label"]
            new_rows.append({
                "date": date, "mode": "synthetic" if args.dry_run else "api",
                "engine": e, "engine_label": label, "via": via[e],
                "prompt_id": pid, "prompt": pr["text"], "branded": branded,
                "intent": pr.get("intent", ""),
                "niche": pr.get("niche", ""), "runs": len(ok), "mentioned": mentioned,
                "position": position, "competitors_mentioned": comp_counts,
                "cited_domains": [s["domain"] for s in sources], "cited_sources": sources,
                "price_mentions": list(dict.fromkeys(prices))[:3], "price_flag": None,
                "proxy": False, "synthetic": bool(args.dry_run),
            })

    serp = cfg.get("serpapi") or {}
    serp_cfg = {"gl": serp.get("gl", "us"), "hl": serp.get("hl", "en"),
                "google_domain": serp.get("google_domain", "google.com"),
                "location": serp.get("location", "")}
    replace_after = int(cfg.get("aio_replace_after_weeks", 3))
    searches_used, aio_results, aio_stop = 0, [], None
    listed = [q.get("text", "") for q in cfg.get("google_queries", [])]
    if run_aio:
        label = (f"Google AI Overviews via SerpApi ({serp_cfg['google_domain']}, "
                 f"gl={serp_cfg['gl']}, hl={serp_cfg['hl']})")
        for i, gq in enumerate(gqueries):
            gid = gq.get("id") or f"G{i + 1}"
            q = gq["text"]
            branded = bool(gq.get("branded")) or first_index(q, brand_patterns(product)) is not None
            if aio_stop:
                res = {"shown": None, "text": "", "urls": [], "alternatives": [], "searches": 0,
                       "error": aio_stop}
            elif args.dry_run:
                p = min(0.85, 0.2 + 0.12 * synthetic_weeks + (0.5 if branded else 0))
                res = fake_aio(q, i, product, competitors, rng, p, cfg.get("category", "software"))
            else:
                try:
                    res = ask_ai_overview(q, serp_cfg, os.environ[SERPAPI_KEY])
                except Exception as ex:
                    res = {"shown": None, "text": "", "urls": [], "alternatives": [], "searches": 0,
                           "error": str(ex)[:300]}
                    print(f"  ai_overviews {gid}: {str(ex)[:120]}")
                    if getattr(ex, "code", None) in (401, 403, 429):
                        aio_stop = f"stopped after HTTP {ex.code} on an earlier query"
            searches_used += res["searches"]
            shown = res["shown"]
            streak = no_aio_streak(history["rows"], q, date, shown)
            swap, alts = None, res["alternatives"]
            if shown is False:
                swap = pick_swap(q, alts, listed)
                if not swap and not args.dry_run:
                    try:  # free, no SerpApi search
                        alts = alts + [("autocomplete", x) for x in
                                       autocomplete(q, serp_cfg["hl"], serp_cfg["gl"])]
                        swap = pick_swap(q, alts, listed)
                    except Exception:
                        pass
            if shown:
                m, pos, comps, pz = analyse(res["text"], res["urls"], product, competitors, q)
                mentioned, position = [m], [pos]
                comp_counts = {n: (None if v is None else int(bool(v))) for n, v in comps.items()}
            else:
                mentioned, position, pz = [], [], []
                comp_counts = {c["name"]: (None if first_index(q, brand_patterns(c)) is not None else 0)
                               for c in competitors}
            counts = {}
            for u in res["urls"]:
                d = domain_of(u)
                if d:
                    c = counts.setdefault(d, {"domain": d, "type": classify(u, product, competitors, cfg),
                                              "count": 0, "example": u})
                    c["count"] += 1
            sources = sorted(counts.values(), key=lambda x: -x["count"])
            aio_results.append({"engine": AIO, "via": "serpapi", "prompt_id": gid, "prompt": q,
                                "aio_shown": shown, "answer": res["text"],
                                "cited_urls": list(dict.fromkeys(clean_url(u) for u in res["urls"])),
                                "alternatives": [{"from": a, "query": t} for a, t in alts],
                                "serpapi_searches": res["searches"], "error": res["error"]})
            new_rows.append({
                "date": date, "mode": "synthetic" if args.dry_run else "api",
                "engine": AIO, "engine_label": label, "via": "serpapi",
                "prompt_id": gid, "prompt": q, "branded": branded,
                "intent": gq.get("intent", ""), "niche": gq.get("niche", ""),
                "aio_shown": shown, "runs": 1 if shown else 0, "mentioned": mentioned,
                "position": position, "cited_founder": any(
                    match_domain(s_["domain"], [product.get("domain", "")]) for s_ in sources),
                "competitors_mentioned": comp_counts,
                "cited_domains": [x["domain"] for x in sources], "cited_sources": sources,
                "price_mentions": list(dict.fromkeys(pz))[:3], "price_flag": None,
                "no_aio_streak": streak, "replace": streak >= replace_after,
                "alternatives": [t for _, t in alts][:6], "suggested_swap": swap,
                "serpapi_searches": res["searches"], "aio_error": res["error"],
                "proxy": False, "synthetic": bool(args.dry_run),
            })
        results += aio_results

    cost_by_engine = {}
    for r in results:
        for x in r.get("runs", []):
            c = (x.get("usage") or {}).get("cost")
            if c is not None:
                cost_by_engine[r["engine"]] = cost_by_engine.get(r["engine"], 0.0) + c
    save_json(run_file, {
        "synthetic": bool(args.dry_run), "complete": True,
        "note": "SYNTHETIC dry run. Fake answers, not from any engine." if args.dry_run else "",
        "date": date, "run_mode": mode, "runs_per_prompt": runs_n, "runs_branded": runs_branded,
        "search_context": context, "web": web, "resolved_urls": resolved,
        "cost_usd": {k: round(v, 4) for k, v in cost_by_engine.items()},
        "engines_run": engines + ([AIO] if run_aio else []),
        "via": dict(via, **({AIO: "serpapi"} if run_aio else {})),
        "engines_skipped": skipped, "serpapi_searches": searches_used, "results": results,
    })

    if not args.no_history:
        keys = {(r["date"], r["engine"], r["prompt_id"], r["mode"]) for r in new_rows}
        history["rows"] = [r for r in history["rows"]
                           if (r["date"], r["engine"], r["prompt_id"], r["mode"]) not in keys] + new_rows
        history["meta"] = {
            "product": product["name"], "product_domain": product.get("domain", ""),
            "category": cfg.get("category", ""), "pricing": cfg.get("pricing", ""),
            "competitors": [c["name"] for c in competitors],
        }
        weeks = [w for w in history.get("weeks", []) if w.get("date") != date]
        weeks.append({"date": date, "run_mode": mode, "runs_per_prompt": runs_n,
                      "cost_usd": round(sum(cost_by_engine.values()), 4)})
        history["weeks"] = sorted(weeks, key=lambda w: w["date"])
        save_json(hist_path, history)

    lost = sum(1 for r in new_rows if r["runs"] and not any(r["mentioned"]) and not r["branded"])
    low = sum(1 for r in new_rows if r["runs"] < 2 and r["engine"] != AIO)
    print(f"Wrote {run_file}")
    if not args.no_history:
        print(f"Appended {len(new_rows)} rows to {hist_path} "
              f"({lost} non-branded prompt-engine pairs with no mention, {low} with fewer than 2 runs)")
    calls = {}
    for r in results:
        if r["engine"] != AIO:
            calls[r["engine"]] = calls.get(r["engine"], 0) + sum(1 for x in r["runs"] if not x.get("error"))
    if cost_by_engine:
        parts = [f"{e} ${v:.3f} ({calls.get(e, 0)} answers, ${v / max(calls.get(e, 1), 1):.4f} each)"
                 for e, v in cost_by_engine.items()]
        print(f"OpenRouter cost this run: ${sum(cost_by_engine.values()):.3f}. " + "; ".join(parts))
    if run_aio:
        aio_rows = [r for r in new_rows if r["engine"] == AIO]
        print(f"AI Overviews: {sum(1 for r in aio_rows if r['aio_shown'])} of {len(aio_rows)} queries "
              f"showed one, {sum(1 for r in aio_rows if r['aio_shown'] is False)} showed none, "
              f"{sum(1 for r in aio_rows if r['aio_shown'] is None)} could not be read. "
              f"{sum(1 for r in aio_rows if r.get('replace'))} flagged for replacement.")
        print(f"SerpApi searches used: {searches_used}" + (" (simulated)" if args.dry_run else ""))
    if args.dry_run:
        print("SYNTHETIC: these numbers are fake. Use them to test the setup only.")


if __name__ == "__main__":
    main()
