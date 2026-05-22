#!/usr/bin/env python3
"""
AMM GEO Rank Monitor v2.1 — Resilient baseline runner.
Saves partial results on timeout/failure. Runs 3 engine passes.
"""
import json, subprocess, sys, re, os, signal
from datetime import datetime, timezone

TARGET_SITE = "okokkoko4414.github.io/amm-website"
TARGET_DOMAIN = "okokkoko4414.github.io"
TARGET_URL = "https://okokkoko4414.github.io/amm-website/"

KEYWORDS = [
    "GEO marketing agency",
    "Generative Engine Optimization",
    "AI search marketing agency",
    "GEO services pricing",
    "AI-native marketing agency",
    "GEO optimization company",
    "AI search optimization service",
]

ENGINES = [
    {"name": "Google",     "search_url": "https://www.google.com/search?q="},
    {"name": "Bing",       "search_url": "https://www.bing.com/search?q="},
    {"name": "DuckDuckGo", "search_url": "https://duckduckgo.com/?q="},
]

PAGES = [
    ("Home",     "https://okokkoko4414.github.io/amm-website/"),
    ("FAQ",      "https://okokkoko4414.github.io/amm-website/faq.html"),
    ("Services", "https://okokkoko4414.github.io/amm-website/services.html"),
    ("Pricing",  "https://okokkoko4414.github.io/amm-website/pricing.html"),
    ("Contact",  "https://okokkoko4414.github.io/amm-website/contact.html"),
    ("Blog",     "https://okokkoko4414.github.io/amm-website/blog/"),
]

results = []
aborted = False

def search_engine(engine, keyword):
    query = f'site:{TARGET_DOMAIN} "{keyword}"'
    url = engine["search_url"] + query.replace(" ", "+")
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "12", "--location",
             "-A", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
             url],
            capture_output=True, text=True, timeout=15
        )
        html = result.stdout.lower()
        dm = len(re.findall(re.escape(TARGET_DOMAIN), html))
        sm = len(re.findall(re.escape(TARGET_SITE), html))
        return {
            "engine": engine["name"], "keyword": keyword,
            "domain_mentions": dm, "site_mentions": sm,
            "total_mentions": dm + sm,
            "found": (dm + sm) > 0, "html_size": len(html),
        }
    except subprocess.TimeoutExpired:
        return {"engine": engine["name"], "keyword": keyword, "error": "timeout", "found": False}
    except Exception as e:
        return {"engine": engine["name"], "keyword": keyword, "error": str(e)[:60], "found": False}

def save_progress(report, label="partial"):
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    path = f"/home/ok2049/amm-company/website/geo-rank-{label}-{ts}.json"
    with open(path, "w") as f:
        json.dump(report, f, indent=2, default=str)
    return path

def check_site():
    try:
        r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                            "--max-time", "10", "--location", TARGET_URL],
                           capture_output=True, text=True, timeout=15)
        code = r.stdout.strip()
        return {"reachable": code.startswith("2") or code.startswith("3"), "status_code": code}
    except Exception as e:
        return {"reachable": False, "error": str(e)}

def check_schema():
    checks = {}
    for name, url in PAGES:
        try:
            r = subprocess.run(["curl", "-s", "--max-time", "10", url],
                               capture_output=True, text=True, timeout=15)
            has_ld = "application/ld+json" in r.stdout
            has_sch = "schema.org" in r.stdout
            checks[name] = {
                "reachable": bool(r.stdout.strip()),
                "has_structured_data": has_ld and has_sch,
                "has_jsonld": has_ld,
                "html_size": len(r.stdout),
            }
        except Exception as e:
            checks[name] = {"reachable": False, "error": str(e)}
    return checks

def generate_report(search_results, schema_check, health):
    found = sum(1 for r in search_results if r.get("found"))
    total = len(search_results)
    visibility = round(found / total * 100, 1) if total > 0 else 0

    kw_vis = {}
    for r in search_results:
        kw = r["keyword"]
        if kw not in kw_vis:
            kw_vis[kw] = {"found": 0, "total": 0, "engines": []}
        kw_vis[kw]["total"] += 1
        if r.get("found"):
            kw_vis[kw]["found"] += 1
            kw_vis[kw]["engines"].append(r["engine"])

    recs = []
    if visibility < 10:
        recs.append("CRITICAL: Barely visible in search. Need immediate content + GEO strategy.")
    elif visibility < 30:
        recs.append("LOW visibility. Add structured data + depth content around target keywords.")
    elif visibility < 60:
        recs.append("MODERATE visibility. Strengthen content clusters, add more FAQ pages.")

    schema_fail = [k for k, v in schema_check.items() if v.get("reachable") and not v.get("has_structured_data")]
    if schema_fail:
        recs.append(f"Schema.org missing on: {', '.join(schema_fail)}. Add JSON-LD.")
    weak = [kw for kw, info in kw_vis.items() if info["found"] == 0]
    if weak:
        recs.append(f"No visibility for: {', '.join(weak)}. Create dedicated pillar content.")
    if not recs:
        recs.append("Good baseline. Continue content + weekly tracking.")

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "target_site": TARGET_SITE,
        "target_url": TARGET_URL,
        "site_health": health,
        "keywords_tracked": KEYWORDS,
        "engines": [e["name"] for e in ENGINES],
        "search_results": search_results,
        "schema_check": schema_check,
        "summary": {
            "baseline_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "total_checks": total,
            "found_count": found,
            "visibility_score_pct": visibility,
            "keyword_visibility": kw_vis,
        },
        "recommendations": recs,
    }

def print_report(report):
    s = report["summary"]
    print("=" * 64)
    print(f"  GEO Rank Monitor — Baseline Report")
    print(f"  Date: {s['baseline_date']}")
    print(f"  Target: {report['target_site']}")
    print("=" * 64)
    h = report["site_health"]
    print(f"\n  Site: {'✅ OK' if h.get('reachable') else '❌ FAIL'} (HTTP {h.get('status_code','?')})")
    print(f"\n  📊 Visibility Score: {s['visibility_score_pct']}% ({s['found_count']}/{s['total_checks']})")
    print(f"\n  📋 Schema.org Check:")
    for page, c in report["schema_check"].items():
        ico = "✅" if c.get("has_structured_data") else "❌" if c.get("reachable") else "⚠️"
        print(f"    {ico} {page}: {'Schema OK' if c.get('has_structured_data') else 'Missing' if c.get('reachable') else 'Unreachable'}")
    print(f"\n  🔍 Per-Keyword Visibility:")
    for kw, info in s["keyword_visibility"].items():
        pct = round(info["found"] / info["total"] * 100) if info["total"] > 0 else 0
        eng = ", ".join(info["engines"]) if info["engines"] else "—"
        print(f"    {pct:>3}%  {kw:<40}  [{eng}]")
    print(f"\n  💡 Recommendations:")
    for r in report.get("recommendations", []):
        print(f"    → {r}")
    print(f"\n  🔎 Detail ({s['total_checks']} checks):")
    for r in report["search_results"]:
        ico = "✅" if r.get("found") else "❌"
        err = f" [{r.get('error','')}]" if r.get('error') else ""
        print(f"    {ico} {r['engine']:<12} {r['keyword'][:35]:<35} mentions={r.get('total_mentions',0)}{err}")
    print("=" * 64)

# --- Main ---
print(f"AMM GEO Rank Monitor v2.1 — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n")

health = check_site()
print(f"Site health: {'OK' if health.get('reachable') else 'FAIL'} (HTTP {health.get('status_code','?')})\n")

# Search phase — save partial results at each engine boundary
all_results = []
for engine in ENGINES:
    for kw in KEYWORDS:
        print(f"  {engine['name']}: \"{kw}\"...", end=" ", flush=True)
        result = search_engine(engine, kw)
        all_results.append(result)
        if result.get("found"):
            print(f"✅ {result['total_mentions']} mentions")
        elif result.get("error"):
            print(f"⚠️ {result['error']}")
        else:
            print("❌")
    # Save after each engine
    partial = generate_report(all_results, {}, health)
    save_progress(partial, f"after-{engine['name'].lower()}")
    print(f"  → Partial saved after {engine['name']}\n")

print("Checking Schema.org...")
schema_check = check_schema()
for p, c in schema_check.items():
    print(f"  {'✅' if c.get('has_structured_data') else '❌'} {p}")

report = generate_report(all_results, schema_check, health)
path = save_progress(report, "baseline-v2")
print(f"\nReport saved to: {path}\n")
print_report(report)
