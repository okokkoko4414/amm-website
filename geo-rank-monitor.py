#!/usr/bin/env python3
"""
AMM GEO Rank Monitor v2.0
Real rank checking using web search + citation analysis.
Phase 1 — automated baseline tracking with search engine queries.
"""
import json
import subprocess
import sys
import re
from datetime import datetime, timezone

TARGET_SITE = "okokkoko4414.github.io/amm-website"
TARGET_DOMAIN = "okokkoko4414.github.io"
TARGET_URL = "https://okokkoko4414.github.io/amm-website/"

KEYWORDS = [
    "GEO marketing agency",
    "Generative Engine Optimization",
    "AI search marketing agency",
    "GEO services pricing",
]

ENGINES = [
    {"name": "Bing",         "search_url": "https://www.bing.com/search?q=",         "label": "Bing Search"},
    {"name": "DuckDuckGo",   "search_url": "https://duckduckgo.com/?q=",            "label": "DuckDuckGo"},
]


def check_site_accessibility():
    """Verify our own site is accessible."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "--max-time", "10", "--location", TARGET_URL],
            capture_output=True, text=True, timeout=15
        )
        code = result.stdout.strip()
        return {"reachable": code.startswith("2") or code.startswith("3"), "status_code": code}
    except Exception as e:
        return {"reachable": False, "error": str(e)}


def search_engine(engine, keyword):
    """
    Search for our site's presence in search engine results.
    Uses curl with proper user-agent to get HTML results.
    Returns:
      - rank: position in results (0 = not found, -1 = error)
      - snippet_found: whether our site/snippet appeared
      - result_count: estimated results count
    """
    query = f'site:{TARGET_DOMAIN} "{keyword}"'
    url = engine["search_url"] + query.replace(" ", "+")

    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "10", "--location",
             "-A", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
             url],
            capture_output=True, text=True, timeout=20
        )
        html = result.stdout.lower()

        # Count mentions of our domain
        domain_matches = len(re.findall(re.escape(TARGET_DOMAIN), html))
        site_matches = len(re.findall(re.escape(TARGET_SITE), html))
        total_matches = domain_matches + site_matches

        # Check for result stats
        result_count = 0
        result_count_match = re.search(r'about ([\d,]+) results', html)
        if result_count_match:
            result_count = int(result_count_match.group(1).replace(",", ""))
        result_count_match2 = re.search(r'([\d,]+) results', html)
        if result_count_match2 and result_count == 0:
            try:
                result_count = int(result_count_match2.group(1).replace(",", ""))
            except:
                pass

        return {
            "engine": engine["name"],
            "keyword": keyword,
            "domain_mentions": domain_matches,
            "site_mentions": site_matches,
            "total_mentions": total_matches,
            "result_count": result_count,
            "found": total_matches > 0,
            "html_size": len(html),
        }
    except Exception as e:
        return {
            "engine": engine["name"],
            "keyword": keyword,
            "error": str(e),
            "found": False,
        }


def check_schema_org():
    """Check if our site has valid Schema.org structured data."""
    checks = {}
    pages = [
        ("Home", "https://okokkoko4414.github.io/amm-website/"),
        ("FAQ", "https://okokkoko4414.github.io/amm-website/faq.html"),
        ("Services", "https://okokkoko4414.github.io/amm-website/services.html"),
        ("Pricing", "https://okokkoko4414.github.io/amm-website/pricing.html"),
    ]
    for name, url in pages:
        try:
            result = subprocess.run(
                ["curl", "-s", "--max-time", "10", url],
                capture_output=True, text=True, timeout=15
            )
            has_jsonld = "application/ld+json" in result.stdout
            has_schema = "schema.org" in result.stdout
            checks[name] = {
                "reachable": bool(result.stdout.strip()),
                "has_structured_data": has_jsonld and has_schema,
                "has_jsonld": has_jsonld,
                "has_schema_dot_org": has_schema,
                "html_size": len(result.stdout),
            }
        except Exception as e:
            checks[name] = {"reachable": False, "error": str(e)}
    return checks


def generate_report(search_results, schema_check, health):
    """Generate the complete GEO rank report."""
    found_count = sum(1 for r in search_results if r.get("found"))
    total_checks = len(search_results)
    visibility_pct = round(found_count / total_checks * 100, 1) if total_checks > 0 else 0

    keyword_found = {}
    for r in search_results:
        kw = r["keyword"]
        if kw not in keyword_found:
            keyword_found[kw] = {"found": 0, "total": 0, "engines": []}
        keyword_found[kw]["total"] += 1
        if r.get("found"):
            keyword_found[kw]["found"] += 1
            keyword_found[kw]["engines"].append(r["engine"])

    report = {
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
            "total_checks": total_checks,
            "found_count": found_count,
            "visibility_score_pct": visibility_pct,
            "keyword_visibility": keyword_found,
        },
        "recommendations": generate_recommendations(visibility_pct, schema_check, keyword_found),
    }
    return report


def generate_recommendations(visibility_pct, schema_check, keyword_found):
    recs = []
    if visibility_pct < 10:
        recs.append("CRITICAL: Site barely visible in search results. Need immediate GEO content strategy.")
    elif visibility_pct < 30:
        recs.append("LOW visibility. Focus on structured data + depth content around target keywords.")
    elif visibility_pct < 60:
        recs.append("MODERATE visibility. Strengthen content clusters and add more FAQ Schema pages.")

    schema_fail = [k for k, v in schema_check.items() if not v.get("has_structured_data")]
    if schema_fail:
        recs.append(f"Schema.org missing on: {', '.join(schema_fail)}. Add JSON-LD structured data.")

    weak_kw = [kw for kw, info in keyword_found.items() if info["found"] == 0]
    if weak_kw:
        recs.append(f"No visibility for: {', '.join(weak_kw)}. Create dedicated pillar content for these.")

    if not recs:
        recs.append("Good baseline. Continue content production and weekly tracking.")

    return recs


def print_report(report):
    """Pretty-print the report to stdout."""
    s = report["summary"]
    print("=" * 64)
    print("  AMM GEO Rank Monitor v2.0 — Daily Report")
    print(f"  Date: {s['baseline_date']}")
    print(f"  Target: {report['target_site']}")
    print("=" * 64)
    print()

    # Site health
    h = report["site_health"]
    print(f"  Site: {'✅ OK' if h.get('reachable') else '❌ FAIL'} (HTTP {h.get('status_code','?')})")
    print()

    # Visibility score
    print(f"  📊 Visibility Score: {s['visibility_score_pct']}% ({s['found_count']}/{s['total_checks']})")
    print()

    # Schema check
    print(f"  📋 Schema.org Check:")
    for page, check in report["schema_check"].items():
        icon = "✅" if check.get("has_structured_data") else "❌" if check.get("reachable") else "⚠️"
        print(f"    {icon} {page}: {'Schema OK' if check.get('has_structured_data') else 'Missing' if check.get('reachable') else 'Unreachable'}")
    print()

    # Per-keyword breakdown
    print(f"  🔍 Per-Keyword Visibility:")
    for kw, info in s["keyword_visibility"].items():
        bar = "█" * info["found"] + "░" * (info["total"] - info["found"])
        pct = round(info["found"] / info["total"] * 100) if info["total"] > 0 else 0
        engines = ", ".join(info["engines"]) if info["engines"] else "—"
        print(f"    {bar} {pct:>3}%  {kw:<40}  [{engines}]")
    print()

    # Recommendations
    print(f"  💡 Recommendations:")
    for r in report.get("recommendations", []):
        print(f"    → {r}")
    print()

    # Raw search results
    print(f"  🔎 Detailed Search Results:")
    print(f"    {'Engine':<15} {'Keyword':<35} {'Found':>6} {'Mentions':>9}")
    print(f"    {'-'*15} {'-'*35} {'-'*6} {'-'*9}")
    for r in report["search_results"]:
        found_icon = "✅" if r.get("found") else "❌"
        mentions = r.get("total_mentions", 0)
        print(f"    {r['engine']:<15} {r['keyword']:<35} {found_icon:>6} {mentions:>9}")
    print()

    print("=" * 64)


def main():
    print(f"AMM GEO Rank Monitor v2.0 — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print()

    # Check site health
    health = check_site_accessibility()
    print(f"Site: {'OK' if health.get('reachable') else 'FAIL'} (HTTP {health.get('status_code','?')})")
    print()

    # Run searches for all keywords across engines
    search_results = []
    total = len(KEYWORDS) * len(ENGINES)
    done = 0
    for engine in ENGINES:
        for kw in KEYWORDS:
            done += 1
            print(f"  [{done}/{total}] {engine['name']}: \"{kw}\"...", end=" ", flush=True)
            result = search_engine(engine, kw)
            search_results.append(result)
            if result.get("found"):
                print(f"✅ Found ({result['total_mentions']} mentions)")
            elif result.get("error"):
                print(f"⚠️ Error: {result['error'][:40]}")
            else:
                print("❌ Not found")

    # Check Schema.org on all pages
    print()
    print("Checking Schema.org...")
    schema_check = check_schema_org()

    # Generate and save report
    print()
    report = generate_report(search_results, schema_check, health)
    report_path = f"/home/ok2049/amm-company/website/geo-rank-baseline-{datetime.now(timezone.utc).strftime('%Y%m%d')}-v2.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, default=str)

    print_report(report)
    print(f"Full report saved to: {report_path}")


if __name__ == "__main__":
    main()
