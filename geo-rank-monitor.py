#!/usr/bin/env python3
"""
AMM GEO Rank Monitor v1.0
Simple CLI tool to check brand visibility across AI search engines.
Phase 0 MVP — uses programmatic queries where possible.
"""

import json
import subprocess
import sys
from datetime import datetime

TARGET_SITE = "amm-geo.com"
TARGET_KEYWORDS = [
    "GEO marketing agency",
    "Generative Engine Optimization",
    "AI search marketing",
    "GEO services",
    "AI-native marketing agency",
]

ENGINES = [
    {"name": "ChatGPT",     "url": "https://chatgpt.com",       "query_prefix": "What is "},
    {"name": "Gemini",      "url": "https://gemini.google.com", "query_prefix": ""},
    {"name": "Perplexity",  "url": "https://perplexity.ai",     "query_prefix": ""},
    {"name": "Claude",      "url": "https://claude.ai",         "query_prefix": ""},
    {"name": "Grok",        "url": "https://x.ai/grok",         "query_prefix": ""},
    {"name": "Bing Copilot","url": "https://bing.com/chat",     "query_prefix": ""},
]

def check_site_accessibility():
    """Verify our own site is accessible - basic health check."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", 
             "--max-time", "10", f"http://localhost:8080"],
            capture_output=True, text=True, timeout=15
        )
        code = result.stdout.strip()
        return {"reachable": code == "200", "status_code": code}
    except Exception as e:
        return {"reachable": False, "error": str(e)}

def run_engine_check(engine_name, keyword):
    """
    Placeholder for engine-specific rank checking.
    Phase 1: implement per-engine API/programmatic checks.
    Phase 0: manual baseline documented here.
    """
    return {
        "engine": engine_name,
        "keyword": keyword,
        "status": "manual_check_required",
        "note": f"Phase 0: Check {engine_name} for '{keyword}' — does {TARGET_SITE} appear?"
    }

def generate_report(results):
    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "target_site": TARGET_SITE,
        "site_health": check_site_accessibility(),
        "baseline_checks": results,
        "summary": {
            "total_keywords": len(TARGET_KEYWORDS),
            "total_engines": len(ENGINES),
            "baseline_date": datetime.utcnow().strftime("%Y-%m-%d"),
        }
    }
    return report

def main():
    print(f"=== AMM GEO Rank Monitor v1.0 ===")
    print(f"Target: {TARGET_SITE}")
    print(f"Date:   {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print()

    # Site health
    health = check_site_accessibility()
    print(f"Site Health: {'✓ Reachable' if health.get('reachable') else '✗ Unreachable'}")
    if health.get('status_code'):
        print(f"  HTTP {health['status_code']}")
    if health.get('error'):
        print(f"  Error: {health['error']}")
    print()

    # Baseline checks (placeholders for Phase 0)
    print("Baseline Checks (Phase 0 — manual):")
    print(f"{'Engine':<20} {'Keyword':<40} {'Status'}")
    print("-" * 80)

    results = []
    for engine in ENGINES:
        for kw in TARGET_KEYWORDS:
            r = run_engine_check(engine["name"], kw)
            results.append(r)
            print(f"{r['engine']:<20} {kw:<40} {r['status']}")

    # Save report
    report = generate_report(results)
    report_path = f"/home/ok2049/amm-company/website/geo-rank-baseline-{datetime.utcnow().strftime('%Y%m%d')}.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nReport saved to: {report_path}")
    print(f"Next step: Manually check each engine, update status, and re-run.")

if __name__ == "__main__":
    main()
