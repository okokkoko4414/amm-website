#!/usr/bin/env python3
"""Fix Schema gaps identified in GEO-15 status review.
Adds: Twitter Card tags, Article schema (blog), BreadcrumbList, WebSite schema.
"""
import re, json, os

BASE = "/home/ok2049/amm-company/website"
SITE_URL = "https://okokkoko4414.github.io/amm-website"

PAGES = {
    "index.html": {"title": "AMM — AI-Native GEO Marketing Agency", "desc": "AI-native GEO marketing agency helping B2B companies dominate AI search visibility.", "path": "/"},
    "about.html": {"title": "About AMM — Our Story & AI-Native Approach", "desc": "Learn about AMM, the first fully AI-agent operated GEO marketing company.", "path": "/about.html"},
    "services.html": {"title": "GEO Marketing Services — AMM", "desc": "Comprehensive GEO marketing services: AI search optimization, content engineering, and brand visibility.", "path": "/services.html"},
    "service-groups.html": {"title": "GEO Service Groups — AMM", "desc": "Explore our GEO service categories: visibility, content, monitoring, and strategy.", "path": "/service-groups.html"},
    "pricing.html": {"title": "GEO Marketing Pricing — AMM", "desc": "Transparent GEO marketing pricing starting at $300/month. No hidden fees.", "path": "/pricing.html"},
    "contact.html": {"title": "Contact AMM — GEO Marketing Agency", "desc": "Get in touch with AMM for your GEO marketing needs. Free consultation available.", "path": "/contact.html"},
    "faq.html": {"title": "GEO Marketing FAQ — AMM", "desc": "Frequently asked questions about Generative Engine Optimization (GEO).", "path": "/faq.html"},
}

BLOG_PAGES = {
    "blog/what-is-geo-complete-guide.html": {
        "title": "What is GEO? Complete Guide to Generative Engine Optimization",
        "desc": "Comprehensive guide to Generative Engine Optimization — how it works, why it matters, and how to get started.",
        "path": "/blog/what-is-geo-complete-guide.html",
        "date": "2026-05-23",
        "author": "AMM Research Team"
    },
    "blog/geo-vs-seo-differences.html": {
        "title": "GEO vs SEO: Key Differences Explained",
        "desc": "Understanding the differences between Generative Engine Optimization and traditional SEO.",
        "path": "/blog/geo-vs-seo-differences.html",
        "date": "2026-05-22",
        "author": "AMM Research Team"
    },
    "blog/why-deepseek-matters-for-geo.html": {
        "title": "Why DeepSeek Matters for GEO Marketing",
        "desc": "How DeepSeek's AI capabilities impact Generative Engine Optimization strategies.",
        "path": "/blog/why-deepseek-matters-for-geo.html",
        "date": "2026-05-24",
        "author": "AMM Research Team"
    },
}

def add_twitter_cards(html, title, desc, image=None):
    """Add Twitter Card meta tags after existing OG tags."""
    twitter_tags = (
        f'  <meta name="twitter:card" content="summary_large_image">\n'
        f'  <meta name="twitter:title" content="{title}">\n'
        f'  <meta name="twitter:description" content="{desc}">\n'
    )
    if image:
        twitter_tags += f'  <meta name="twitter:image" content="{image}">\n'
    # Insert after the last og:type tag (handle both > and /> endings)
    html = re.sub(
        r'(<meta property="og:type" content="[^"]*"\s*/?>)\s*\n',
        rf'\1\n{twitter_tags}',
        html,
        count=1
    )
    return html

def add_breadcrumb_schema(html, items):
    """Add BreadcrumbList JSON-LD schema before </head>."""
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
        ] + [
            {"@type": "ListItem", "position": i+2, "name": name, "item": SITE_URL + url}
            for i, (name, url) in enumerate(items)
        ]
    }
    block = f'\n  <script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n  </script>'
    html = html.replace('</head>', f'{block}\n</head>')
    return html

def add_article_schema(html, page_info):
    """Add Article JSON-LD schema before </head>."""
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": page_info["title"],
        "description": page_info["desc"],
        "author": {"@type": "Organization", "name": "AMM", "url": SITE_URL},
        "publisher": {"@type": "Organization", "name": "AMM", "url": SITE_URL},
        "datePublished": page_info["date"],
        "dateModified": page_info["date"],
        "mainEntityOfPage": {"@type": "WebPage", "@id": SITE_URL + page_info["path"]},
        "url": SITE_URL + page_info["path"]
    }
    block = f'\n  <script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n  </script>'
    html = html.replace('</head>', f'{block}\n</head>')
    return html

def add_website_schema(html):
    """Add WebSite schema with SearchAction to homepage."""
    schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "AMM — AI-Native GEO Marketing Agency",
        "url": SITE_URL + "/",
        "potentialAction": {
            "@type": "SearchAction",
            "target": SITE_URL + "/blog/?q={search_term_string}",
            "query-input": "required name=search_term_string"
        }
    }
    block = f'\n  <script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n  </script>'
    html = html.replace('</head>', f'{block}\n</head>')
    return html

# Process main pages
for filename, info in PAGES.items():
    filepath = os.path.join(BASE, filename)
    if not os.path.exists(filepath):
        print(f"SKIP (not found): {filename}")
        continue
    with open(filepath) as f:
        html = f.read()
    
    # 1. Add Twitter Cards
    html = add_twitter_cards(html, info["title"], info["desc"])
    
    # 2. Add BreadcrumbList
    breadcrumb_items = []
    if info["path"] != "/":
        parts = info["path"].lstrip("/").split("/")
        if len(parts) == 1:
            breadcrumb_items.append((info["title"][:40], info["path"]))
    html = add_breadcrumb_schema(html, breadcrumb_items)
    
    # 3. Add WebSite schema to homepage only
    if filename == "index.html":
        html = add_website_schema(html)
    
    with open(filepath, "w") as f:
        f.write(html)
    print(f"OK: {filename} — Twitter Cards + Breadcrumb{' + WebSite' if filename == 'index.html' else ''}")

# Process blog pages
for filename, info in BLOG_PAGES.items():
    filepath = os.path.join(BASE, filename)
    if not os.path.exists(filepath):
        print(f"SKIP (not found): {filename}")
        continue
    with open(filepath) as f:
        html = f.read()
    
    # 1. Add Twitter Cards
    html = add_twitter_cards(html, info["title"], info["desc"])
    
    # 2. Add Article schema
    html = add_article_schema(html, info)
    
    # 3. Add BreadcrumbList for blog
    html = add_breadcrumb_schema(html, [
        ("Blog", "/blog/"),
        (info["title"][:35], info["path"])
    ])
    
    with open(filepath, "w") as f:
        f.write(html)
    print(f"OK: {filename} — Twitter Cards + Article + Breadcrumb")

print("\nDone. All Schema gaps fixed.")
