#!/usr/bin/env python3
"""
Redwood Real Estate Solutions — Multi-Page Site Generator
Generates all HTML pages from shared templates + unique page content.
Preserves existing visual design, restructures into SEO multi-page architecture.
"""

import os, json
from datetime import datetime

BASE = '/home/user/workspace/redwood-realestate'
DOMAIN = 'https://www.redwood-realestate.com'

# ── Navigation ─────────────────────────────────────────────
NAV = [
    ('Home', 'index.html', 'home'),
    ('How It Works', 'how-it-works.html', 'how-it-works'),
    ('Areas We Serve', 'areas-we-serve.html', 'areas'),
    ('Reviews', 'reviews.html', 'reviews'),
    ('FAQ', 'faq.html', 'faq'),
    ('Blog', 'blog.html', 'blog'),
]

CITIES = [
    {'name': 'Sacramento', 'slug': 'sacramento', 'population': '524,943', 'median': '$430,000', 'county': 'Sacramento County', 'zip_sample': '95814, 95816, 95818, 95820', 'desc': 'the state capital and the heart of Northern California\'s real estate market'},
    {'name': 'Elk Grove', 'slug': 'elk-grove', 'population': '176,124', 'median': '$575,000', 'county': 'Sacramento County', 'zip_sample': '95624, 95757, 95758', 'desc': 'one of the fastest-growing cities in Sacramento County'},
    {'name': 'Roseville', 'slug': 'roseville', 'population': '147,773', 'median': '$610,000', 'county': 'Placer County', 'zip_sample': '95661, 95678, 95747', 'desc': 'a thriving Placer County suburb with strong property values'},
    {'name': 'Folsom', 'slug': 'folsom', 'population': '82,203', 'median': '$680,000', 'county': 'Sacramento County', 'zip_sample': '95630', 'desc': 'a desirable city known for Folsom Lake and excellent schools'},
    {'name': 'Rancho Cordova', 'slug': 'rancho-cordova', 'population': '79,332', 'median': '$445,000', 'county': 'Sacramento County', 'zip_sample': '95670, 95742', 'desc': 'a growing Sacramento suburb with diverse housing stock'},
    {'name': 'Citrus Heights', 'slug': 'citrus-heights', 'population': '87,583', 'median': '$425,000', 'county': 'Sacramento County', 'zip_sample': '95610, 95621', 'desc': 'a well-established community in northeast Sacramento County'},
]

# ── Shared Template Components ─────────────────────────────

def asset_path(page_file, asset):
    """Get correct relative path for assets from any page depth."""
    if '/' in page_file:
        return '../' + asset
    return './' + asset

def page_path(from_page, to_page):
    """Get relative link between pages."""
    if '/' in from_page and '/' not in to_page:
        return '../' + to_page
    if '/' not in from_page and '/' in to_page:
        return to_page
    return to_page

def make_head(page_file, title, description, canonical_path='', schema_blocks=None, extra_head=''):
    canonical = DOMAIN + '/' + canonical_path if canonical_path else DOMAIN + '/'
    ap = lambda a: asset_path(page_file, a)
    schemas = ''
    if schema_blocks:
        for s in schema_blocks:
            schemas += f'  <script type="application/ld+json">\n  {json.dumps(s, indent=2)}\n  </script>\n'
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <link rel="canonical" href="{canonical}">
  <meta name="geo.region" content="US-CA">
  <meta name="geo.placename" content="Sacramento">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="Redwood Real Estate Solutions">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <link rel="preconnect" href="https://api.fontshare.com" crossorigin>
  <link href="https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@400,500,700,800&f[]=satoshi@400,500,600,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{ap('base.css')}">
  <link rel="stylesheet" href="{ap('style.css')}">
  <link rel="stylesheet" href="{ap('pages.css')}">
{schemas}{extra_head}</head>
<body>
  <a href="#main" class="sr-only" style="position:fixed;top:0;left:0;z-index:999;padding:1rem;background:var(--color-primary);color:white;">Skip to main content</a>
'''

def make_header(page_file, active_id=''):
    pp = lambda p: page_path(page_file, p)
    home = pp('index.html')
    offer = pp('index.html') + '#get-offer'
    
    nav_links = ''
    mobile_links = ''
    for label, href, nav_id in NAV:
        active = ' class="is-active"' if nav_id == active_id else ''
        link = pp(href)
        nav_links += f'          <li><a href="{link}"{active}>{label}</a></li>\n'
        mobile_links += f'      <li><a href="{link}" data-mobile-link>{label}</a></li>\n'
    
    return f'''  <header class="header" role="banner">
    <div class="header__inner">
      <a href="{home}" class="logo" aria-label="Redwood Real Estate Solutions — home">
        <svg class="logo__icon" viewBox="0 0 36 36" fill="none" aria-hidden="true">
          <rect width="36" height="36" rx="8" fill="var(--color-primary)" opacity="0.1"/>
          <path d="M18 4c-1.5 3-5 5-5 10a5 5 0 0010 0c0-5-3.5-7-5-10z" fill="var(--color-primary)" opacity="0.3"/>
          <path d="M18 8c-1 2-3.5 3.5-3.5 7a3.5 3.5 0 007 0c0-3.5-2.5-5-3.5-7z" fill="var(--color-primary)"/>
          <path d="M18 15v13" stroke="var(--color-primary)" stroke-width="2" stroke-linecap="round"/>
          <path d="M15 20h6" stroke="var(--color-primary)" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
          <path d="M10 30h16" stroke="var(--color-primary)" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <div class="logo__text">Redwood<span>Real Estate Solutions</span></div>
      </a>
      <nav class="nav" aria-label="Main navigation">
        <ul class="nav__links" role="list">
{nav_links}        </ul>
        <a href="{offer}" class="nav__cta">Get My Cash Offer</a>
        <button class="theme-toggle" data-theme-toggle aria-label="Switch to light mode">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
        </button>
        <button class="mobile-toggle" aria-label="Open menu" data-mobile-open>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12h18M3 6h18M3 18h18"/></svg>
        </button>
      </nav>
    </div>
  </header>
  <div class="mobile-menu" id="mobile-menu" role="dialog" aria-label="Navigation menu">
    <div class="mobile-menu__header">
      <div class="logo__text">Redwood<span style="color:var(--color-primary)">Real Estate Solutions</span></div>
      <button class="mobile-menu__close" aria-label="Close menu" data-mobile-close>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
      </button>
    </div>
    <ul class="mobile-menu__links" role="list">
{mobile_links}    </ul>
    <a href="{offer}" class="mobile-menu__cta" data-mobile-link>Get My Cash Offer</a>
  </div>
'''

def make_breadcrumb(page_file, crumbs):
    """crumbs: list of (label, href) tuples. Last one has no href."""
    pp = lambda p: page_path(page_file, p)
    items = f'<a href="{pp("index.html")}">Home</a>'
    for i, (label, href) in enumerate(crumbs):
        if href and i < len(crumbs) - 1:
            items += f' <span class="breadcrumb__sep" aria-hidden="true">/</span> <a href="{pp(href)}">{label}</a>'
        else:
            items += f' <span class="breadcrumb__sep" aria-hidden="true">/</span> <span aria-current="page">{label}</span>'
    return f'  <nav class="breadcrumb" aria-label="Breadcrumb">\n    <div class="container">{items}</div>\n  </nav>\n'

def make_page_hero(overline, title, subtitle=''):
    sub = f'\n          <p class="page-hero__subtitle">{subtitle}</p>' if subtitle else ''
    return f'''    <section class="page-hero">
      <div class="container">
        <div class="page-hero__content">
          <span class="page-hero__overline">{overline}</span>
          <h1 class="page-hero__title">{title}</h1>{sub}
        </div>
      </div>
    </section>
'''

def make_cta_section(page_file, form_id='offer-form-inner'):
    pp = lambda p: page_path(page_file, p)
    return f'''    <section class="cta-section" id="get-offer">
      <div class="cta-layout">
        <div class="cta-content">
          <p class="cta-content__overline">Get Started Today</p>
          <h2 class="cta-content__title">Ready to Sell Your House?</h2>
          <p class="cta-content__desc">Fill out the form and we'll reach out with a no-obligation cash offer within 24 hours. No pressure, no commitment — just an honest number.</p>
          <ul class="cta-content__promises" role="list">
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>Cash offer within 24 hours</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>Close in as few as 7 days</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>Zero fees, commissions, or closing costs</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>Sell as-is — no cleaning or repairs</li>
          </ul>
        </div>
        <div class="lead-form" id="lead-form-inner">
          <h3 class="lead-form__title">Get Your Free Cash Offer</h3>
          <p class="lead-form__subtitle">It takes less than 60 seconds.</p>
          <form id="{form_id}" novalidate>
            <div class="form-group">
              <label for="{form_id}-name">Full Name</label>
              <input type="text" id="{form_id}-name" name="full_name" placeholder="John Smith" required autocomplete="name">
            </div>
            <div class="form-group">
              <label for="{form_id}-address">Property Address</label>
              <input type="text" id="{form_id}-address" name="property_address" placeholder="123 Main St, Sacramento, CA" required autocomplete="street-address">
            </div>
            <div class="form-group">
              <label for="{form_id}-email">Email Address</label>
              <input type="email" id="{form_id}-email" name="email" placeholder="john@example.com" required autocomplete="email">
            </div>
            <div class="form-group">
              <label for="{form_id}-phone">Phone Number</label>
              <input type="tel" id="{form_id}-phone" name="phone" placeholder="(555) 123-4567" required autocomplete="tel">
            </div>
            <button type="submit" class="form-submit">Get My Cash Offer Now</button>
            <p class="form-disclaimer">Your information is 100% confidential and will never be shared.</p>
          </form>
          <div class="form-success" id="{form_id}-success">
            <svg class="form-success__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            <h3 class="form-success__title">Offer Request Received</h3>
            <p class="form-success__desc">Thank you. We'll be in touch within 24 hours with your no-obligation cash offer.</p>
          </div>
        </div>
      </div>
    </section>
'''

def make_footer(page_file):
    pp = lambda p: page_path(page_file, p)
    ap = lambda a: asset_path(page_file, a)
    
    links = ''
    for label, href, _ in NAV:
        links += f'          <li><a href="{pp(href)}">{label}</a></li>\n'
    
    city_links = ''
    for c in CITIES[:6]:
        city_links += f'          <li><a href="{pp(f"sell-my-house-fast-{c["slug"]}-ca.html")}">{c["name"]}</a></li>\n'
    
    return f'''  <footer class="footer" role="contentinfo">
    <div class="footer__inner">
      <div class="footer__brand">
        <a href="{pp('index.html')}" class="logo" aria-label="Redwood Real Estate Solutions">
          <svg class="logo__icon" viewBox="0 0 36 36" fill="none" aria-hidden="true">
            <rect width="36" height="36" rx="8" fill="var(--color-primary)" opacity="0.1"/>
            <path d="M18 4c-1.5 3-5 5-5 10a5 5 0 0010 0c0-5-3.5-7-5-10z" fill="var(--color-primary)" opacity="0.3"/>
            <path d="M18 8c-1 2-3.5 3.5-3.5 7a3.5 3.5 0 007 0c0-3.5-2.5-5-3.5-7z" fill="var(--color-primary)"/>
            <path d="M18 15v13" stroke="var(--color-primary)" stroke-width="2" stroke-linecap="round"/>
            <path d="M10 30h16" stroke="var(--color-primary)" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <div class="logo__text">Redwood<span>Real Estate Solutions</span></div>
        </a>
        <p>We help homeowners sell their houses quickly for a fair cash price. No repairs, no commissions, no stress — just a simple, honest way to move forward.</p>
      </div>
      <div class="footer__links">
        <h4>Quick Links</h4>
        <ul role="list">
{links}          <li><a href="{pp('index.html')}#get-offer">Get an Offer</a></li>
        </ul>
      </div>
      <div class="footer__links">
        <h4>Areas We Serve</h4>
        <ul role="list">
{city_links}        </ul>
      </div>
      <div class="footer__links">
        <h4>Contact</h4>
        <ul role="list">
          <li><a href="mailto:patrick@redwood-realestate.com">patrick@redwood-realestate.com</a></li>
          <li><a href="{pp('about.html')}">Meet Our Team</a></li>
          <li><a href="{pp('faq.html')}">View All FAQs</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <p>&copy; 2026 Redwood Real Estate Solutions. All rights reserved.</p>
      <p>We buy houses for cash in Sacramento, Elk Grove, Roseville, Folsom, Rancho Cordova, Citrus Heights, and throughout Northern California.</p>
    </div>
  </footer>
  <div class="sticky-phone">
    <a href="{pp('index.html')}#get-offer" class="sticky-phone__btn">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>
      Get My Free Cash Offer
    </a>
  </div>
  <script src="{ap('app.js')}" defer></script>
</body>
</html>
'''

def write_page(filename, content):
    filepath = os.path.join(BASE, filename)
    os.makedirs(os.path.dirname(filepath) if '/' in filename else BASE, exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f'  ✓ {filename}')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE BUILDERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_how_it_works():
    pf = 'how-it-works.html'
    schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": "How to Sell Your House Fast for Cash in Sacramento",
        "description": "Sell your Sacramento home for cash in four simple steps with Redwood Real Estate Solutions.",
        "totalTime": "P7D",
        "step": [
            {"@type": "HowToStep", "position": 1, "name": "Contact Us", "text": "Fill out our form or call us. Tell us about your property."},
            {"@type": "HowToStep", "position": 2, "name": "Get Your Cash Offer", "text": "We evaluate your property and present a fair, all-cash offer within 24 hours."},
            {"@type": "HowToStep", "position": 3, "name": "Pick Your Closing Date", "text": "Accept our offer and choose your closing date — as fast as 7 days."},
            {"@type": "HowToStep", "position": 4, "name": "Get Paid", "text": "Sign the paperwork and walk away with cash in hand."}
        ]
    }
    breadcrumb_schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN},
        {"@type": "ListItem", "position": 2, "name": "How It Works", "item": DOMAIN + "/how-it-works.html"}
    ]}
    
    content = make_head(pf, 'How It Works — Sell Your House Fast for Cash | Redwood Real Estate', 
        'Learn how our 4-step process works to sell your Sacramento home fast for cash. No repairs, no commissions, close in as little as 7 days.',
        'how-it-works.html', [schema, breadcrumb_schema])
    content += make_header(pf, 'how-it-works')
    content += '  <main id="main">\n'
    content += make_breadcrumb(pf, [('How It Works', '')])
    content += make_page_hero('How It Works', 'Sell Your House in 4 Simple Steps', 'No repairs. No commissions. No uncertainty. Our streamlined process gets you from first contact to cash in hand in days, not months.')
    
    content += '''    <section class="section">
      <div class="container">
        <div class="process-grid process-grid--detailed">
          <div class="process-step fade-in">
            <div class="process-step__number">1</div>
            <h2 class="process-step__title">Contact Us</h2>
            <p class="process-step__desc">Fill out our simple form or give us a call. Tell us about your property — the address, general condition, and your situation. There's absolutely zero obligation. We just need the basics to get started on your offer.</p>
            <ul class="process-step__details">
              <li>Takes less than 60 seconds</li>
              <li>No personal financial info needed</li>
              <li>We'll confirm receipt within 1 hour</li>
            </ul>
          </div>
          <div class="process-step fade-in">
            <div class="process-step__number">2</div>
            <h2 class="process-step__title">Get Your Cash Offer</h2>
            <p class="process-step__desc">We analyze recent comparable sales in your neighborhood, assess the property's condition, and factor in current Sacramento market trends. Within 24 hours, we present you with a fair, all-cash offer — no lowball tactics, just honest numbers.</p>
            <ul class="process-step__details">
              <li>Offer based on real market data</li>
              <li>We explain exactly how we calculated it</li>
              <li>No obligation to accept</li>
            </ul>
          </div>
          <div class="process-step fade-in">
            <div class="process-step__number">3</div>
            <h2 class="process-step__title">Pick Your Closing Date</h2>
            <p class="process-step__desc">Accept our offer and you choose the closing date. Need to close in 7 days to avoid foreclosure? Done. Need 60 days to find your next home? No problem. Your timeline, your terms.</p>
            <ul class="process-step__details">
              <li>Close in as few as 7 days</li>
              <li>Or take up to 60 days</li>
              <li>We handle title, escrow, and paperwork</li>
            </ul>
          </div>
          <div class="process-step fade-in">
            <div class="process-step__number">4</div>
            <h2 class="process-step__title">Get Paid</h2>
            <p class="process-step__desc">Show up to closing, sign the paperwork, and walk away with cash in hand. We cover all closing costs, title fees, and transfer taxes. The price we quoted is the price you get — guaranteed.</p>
            <ul class="process-step__details">
              <li>We pay all closing costs</li>
              <li>Cash wired or check issued same day</li>
              <li>No last-minute surprises</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container container--narrow">
        <div class="section__header section__header--center fade-in">
          <span class="section__overline">Full Transparency</span>
          <h2 class="section__title">How We Calculate Your Offer</h2>
          <p class="section__desc">We believe you deserve to understand exactly how we arrive at our offer price. Here's the formula we use:</p>
        </div>
        <div class="offer-formula fade-in">
          <div class="formula-card">
            <div class="formula-row">
              <span class="formula-label">After Repair Value (ARV)</span>
              <span class="formula-desc">What your home would sell for fully updated on the open market</span>
            </div>
            <div class="formula-row formula-row--minus">
              <span class="formula-label">Cost of Repairs (COR)</span>
              <span class="formula-desc">Estimated renovation and repair costs we'll handle</span>
            </div>
            <div class="formula-row formula-row--minus">
              <span class="formula-label">Our Selling Costs</span>
              <span class="formula-desc">Closing costs, holding costs, and transaction fees (~10% of ARV)</span>
            </div>
            <div class="formula-row formula-row--minus">
              <span class="formula-label">Our Margin</span>
              <span class="formula-desc">A reasonable profit that keeps our business running</span>
            </div>
            <div class="formula-row formula-row--result">
              <span class="formula-label">= Your Cash Offer</span>
              <span class="formula-desc">The amount you walk away with — no deductions, no surprises</span>
            </div>
          </div>
          <p class="formula-note">The less work your home needs, the higher our offer. That's why homes in decent condition often get offers close to market value. We'll walk you through every number so you can make an informed decision.</p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container container--narrow">
        <div class="section__header section__header--center fade-in">
          <span class="section__overline">Compare Your Options</span>
          <h2 class="section__title">Traditional Sale vs. Selling to Redwood</h2>
        </div>
        <div class="comparison-table fade-in" role="table" aria-label="Comparison between traditional sale and selling to Redwood">
          <div class="comparison-row comparison-row--header" role="row">
            <div role="columnheader"></div>
            <div role="columnheader">Traditional Sale</div>
            <div role="columnheader" class="comparison-highlight">Sell to Redwood</div>
          </div>
          <div class="comparison-row" role="row"><div class="comparison-label" role="rowheader">Timeline</div><div role="cell">3-6+ months</div><div role="cell" class="comparison-highlight">7-14 days</div></div>
          <div class="comparison-row" role="row"><div class="comparison-label" role="rowheader">Agent Commissions</div><div role="cell">5-6% of sale</div><div role="cell" class="comparison-highlight">$0</div></div>
          <div class="comparison-row" role="row"><div class="comparison-label" role="rowheader">Repairs Needed</div><div role="cell">$5,000-$30,000+</div><div role="cell" class="comparison-highlight">None</div></div>
          <div class="comparison-row" role="row"><div class="comparison-label" role="rowheader">Showings</div><div role="cell">Dozens</div><div role="cell" class="comparison-highlight">Zero</div></div>
          <div class="comparison-row" role="row"><div class="comparison-label" role="rowheader">Closing Costs</div><div role="cell">2-3% of sale</div><div role="cell" class="comparison-highlight">We pay them</div></div>
          <div class="comparison-row" role="row"><div class="comparison-label" role="rowheader">Risk of Deal Falling Through</div><div role="cell">Common</div><div role="cell" class="comparison-highlight">Never</div></div>
        </div>
      </div>
    </section>
'''
    content += make_cta_section(pf, 'offer-form-hiw')
    content += '  </main>\n'
    content += make_footer(pf)
    write_page(pf, content)


def build_about():
    pf = 'about.html'
    schema = {"@context": "https://schema.org", "@type": "AboutPage", "name": "About Redwood Real Estate Solutions", "url": DOMAIN + "/about.html",
        "mainEntity": {"@type": "RealEstateAgent", "name": "Redwood Real Estate Solutions", "founder": {"@type": "Person", "name": "Patrick Mahoney", "jobTitle": "Founder & Owner"},
            "address": {"@type": "PostalAddress", "addressLocality": "Sacramento", "addressRegion": "CA", "addressCountry": "US"},
            "areaServed": "Sacramento Metropolitan Area"}}
    breadcrumb_schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN},
        {"@type": "ListItem", "position": 2, "name": "About Us", "item": DOMAIN + "/about.html"}
    ]}
    
    content = make_head(pf, 'About Us — Meet Patrick Mahoney | Redwood Real Estate Solutions',
        'Meet Patrick Mahoney, founder of Redwood Real Estate Solutions. Sacramento-based cash home buyers committed to integrity, transparency, and helping homeowners move forward.',
        'about.html', [schema, breadcrumb_schema])
    content += make_header(pf, 'about')
    content += '  <main id="main">\n'
    content += make_breadcrumb(pf, [('About Us', '')])
    content += make_page_hero('About Us', 'Meet Redwood Real Estate Solutions', 'A Sacramento-based team built on integrity, transparency, and a genuine desire to help homeowners move forward.')
    
    content += '''    <section class="section">
      <div class="container">
        <div class="about-layout">
          <div class="about-company fade-in">
            <h2 class="about__heading">Our Mission</h2>
            <p>Redwood Real Estate Solutions was founded with a simple belief: selling your home shouldn't be one of the most stressful experiences of your life. Too many homeowners get stuck — facing foreclosure, dealing with costly repairs, navigating a difficult life transition — and the traditional real estate process only adds to the burden.</p>
            <p>We built Redwood to be different. We buy houses directly for cash, cutting out the agents, the commissions, the months of uncertainty, and the expensive repairs. Our process is built around you — your timeline, your situation, your terms.</p>
            <p>Whether your property is in perfect shape or needs major work, we'll make you a fair offer and close on your schedule. Based in Sacramento and serving homeowners throughout Northern California — including Elk Grove, Roseville, Folsom, Rancho Cordova, and Citrus Heights — we're a local team that understands this market and genuinely cares about helping our neighbors.</p>
            <div class="about-values">
              <div class="about-value">
                <svg class="about-value__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                <div><strong>Integrity First</strong><span>Honest offers, no hidden fees, no pressure tactics.</span></div>
              </div>
              <div class="about-value">
                <svg class="about-value__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                <div><strong>Speed & Simplicity</strong><span>Close in as little as 7 days. We handle the hard parts.</span></div>
              </div>
              <div class="about-value">
                <svg class="about-value__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
                <div><strong>People Over Profit</strong><span>Your wellbeing matters more than the transaction.</span></div>
              </div>
            </div>
          </div>
          <div class="about-founder fade-in">
            <div class="about-founder__photo">
              <img src="./assets/patrick-mahoney.png" alt="Patrick Mahoney, owner and founder of Redwood Real Estate Solutions in Sacramento, California" width="500" height="500" loading="lazy">
            </div>
            <h2 class="about-founder__name">Patrick Mahoney</h2>
            <p class="about-founder__role">Founder & Owner</p>
            <p class="about-founder__bio">Patrick Mahoney is the founder and owner of Redwood Real Estate Solutions, a Sacramento-based company specializing in helping homeowners sell their properties quickly and hassle-free for cash.</p>
            <p class="about-founder__bio">With deep roots in Northern California, Patrick started Redwood after seeing firsthand how stressful the traditional home-selling process can be — especially for homeowners facing tough situations like foreclosure, divorce, probate, or properties in disrepair.</p>
            <p class="about-founder__bio">He takes a hands-on approach with every homeowner, ensuring they understand their options, feel respected, and never face high-pressure tactics. When he's not helping Sacramento homeowners, you can find him exploring Northern California's trails and investing in the local community.</p>
            <a href="mailto:patrick@redwood-realestate.com" class="about-founder__email">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
              patrick@redwood-realestate.com
            </a>
          </div>
        </div>
        <div class="trust-badges fade-in">
          <a href="https://www.google.com/maps/place/Redwood+Real+Estate+Solutions" target="_blank" rel="noopener" class="trust-badge trust-badge--google" aria-label="View our Google Reviews">
            <div class="trust-badge__icon"><svg viewBox="0 0 24 24" width="32" height="32"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg></div>
            <div class="trust-badge__content"><div class="trust-badge__stars"><svg viewBox="0 0 120 20" width="96" height="16"><polygon points="12,0 15.09,7.36 23.27,8.18 17.14,13.64 18.82,21.82 12,17.77 5.18,21.82 6.86,13.64 0.73,8.18 8.91,7.36" fill="#FBBC05"/><polygon points="36,0 39.09,7.36 47.27,8.18 41.14,13.64 42.82,21.82 36,17.77 29.18,21.82 30.86,13.64 24.73,8.18 32.91,7.36" fill="#FBBC05"/><polygon points="60,0 63.09,7.36 71.27,8.18 65.14,13.64 66.82,21.82 60,17.77 53.18,21.82 54.86,13.64 48.73,8.18 56.91,7.36" fill="#FBBC05"/><polygon points="84,0 87.09,7.36 95.27,8.18 89.14,13.64 90.82,21.82 84,17.77 77.18,21.82 78.86,13.64 72.73,8.18 80.91,7.36" fill="#FBBC05"/><polygon points="108,0 111.09,7.36 119.27,8.18 113.14,13.64 114.82,21.82 108,17.77 101.18,21.82 102.86,13.64 96.73,8.18 104.91,7.36" fill="#FBBC05"/></svg></div><span class="trust-badge__label">5.0 Stars on Google</span><span class="trust-badge__sub">Read Our Reviews</span></div>
          </a>
          <a href="https://www.bbb.org/" target="_blank" rel="noopener" class="trust-badge trust-badge--bbb" aria-label="BBB Accreditation">
            <div class="trust-badge__icon trust-badge__icon--bbb"><svg viewBox="0 0 80 40" width="64" height="32" fill="none"><rect x="1" y="1" width="78" height="38" rx="4" stroke="#006BA6" stroke-width="2"/><text x="40" y="18" text-anchor="middle" fill="#006BA6" font-family="Arial, sans-serif" font-weight="700" font-size="14">BBB</text><rect x="20" y="24" width="40" height="10" rx="2" fill="#006BA6"/><text x="40" y="32" text-anchor="middle" fill="#fff" font-family="Arial, sans-serif" font-weight="600" font-size="8">ACCREDITED</text></svg></div>
            <div class="trust-badge__content"><span class="trust-badge__rating">A+</span><span class="trust-badge__label">BBB Rating</span><span class="trust-badge__sub">Accredited Business</span></div>
          </a>
        </div>
      </div>
    </section>
'''
    content += make_cta_section(pf, 'offer-form-about')
    content += '  </main>\n'
    content += make_footer(pf)
    write_page(pf, content)


def build_faq():
    pf = 'faq.html'
    questions = [
        ("How fast can you close on my house?", "We can close in as little as 7 days, or on whatever timeline works best for you. Whether you need to move next week or in 60 days, we work around your schedule. Every homeowner's situation is different, and we adapt our timeline to fit yours."),
        ("Do I need to make repairs before selling?", "Absolutely not. We buy houses in any condition — water damage, foundation issues, fire damage, outdated interiors, code violations, mold, roof problems, you name it. Sell your house exactly as it is. Don't spend a single dollar on repairs. We handle everything after we close."),
        ("Are there any fees or commissions?", "None. There are zero fees, zero commissions, and zero closing costs on your end. The offer we make is the amount you receive — period. No hidden surprises, no last-minute deductions, no fine print."),
        ("How do you determine the offer price?", "We analyze recent comparable sales in your neighborhood, the current condition of the property, local market trends, and estimated repair costs. We then present a fair, competitive cash offer and walk you through exactly how we calculated it — full transparency."),
        ("What types of properties do you buy?", "We buy single-family homes, condos, townhomes, duplexes, multi-family properties, mobile homes, and vacant land across the Sacramento metro area. Occupied or vacant, livable or not — we'll make you an offer."),
        ("Is there any obligation if I request an offer?", "Absolutely none. Requesting an offer is completely free and carries zero obligation. If our offer doesn't work for you, no hard feelings. We'll never pressure you or use high-pressure sales tactics. The decision is always 100% yours."),
        ("What areas of Sacramento do you serve?", "We buy houses throughout the Sacramento metropolitan area, including Sacramento, Elk Grove, Roseville, Folsom, Rancho Cordova, Citrus Heights, Davis, Woodland, and surrounding communities. If your property is in Northern California, chances are we can help."),
        ("Can you buy my house if I'm behind on payments?", "Yes. If you're behind on mortgage payments or facing foreclosure, selling your home for cash can help you avoid the foreclosure process, protect your credit, and walk away with money in your pocket. The sooner you reach out, the more options you have."),
        ("What if I inherited a property I don't want?", "We work with many homeowners who've inherited properties. Whether the home needs work, is out of state, or is tied up in probate, we can often still make you an offer. We'll help you navigate the process and get cash for the property quickly."),
        ("Do you buy houses with tenants?", "Yes. We purchase occupied rental properties regularly. You don't need to evict tenants first — we handle tenant situations after closing. This is a common solution for tired landlords ready to move on."),
        ("How is selling to you different from listing with an agent?", "When you list with an agent, you typically wait 3-6+ months for a buyer, pay 5-6% in commissions, make costly repairs, host dozens of showings, and risk deals falling through. When you sell to Redwood, you get a cash offer in 24 hours, close on your schedule, pay zero fees, make zero repairs, and the deal is guaranteed."),
        ("What happens after I submit the form?", "After you submit your information, a member of our team will review your property details and reach out within 24 hours — usually much sooner. We'll ask a few follow-up questions, schedule a quick property visit if needed, and present you with a no-obligation cash offer."),
    ]
    
    faq_schema_items = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in questions]
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema_items}
    breadcrumb_schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN},
        {"@type": "ListItem", "position": 2, "name": "FAQ", "item": DOMAIN + "/faq.html"}
    ]}
    
    content = make_head(pf, 'Frequently Asked Questions — Sell Your House for Cash | Redwood Real Estate',
        'Get answers to common questions about selling your house for cash in Sacramento. Learn about our process, fees (none), timeline, and what to expect.',
        'faq.html', [schema, breadcrumb_schema])
    content += make_header(pf, 'faq')
    content += '  <main id="main">\n'
    content += make_breadcrumb(pf, [('FAQ', '')])
    content += make_page_hero('Common Questions', 'Frequently Asked Questions', 'We believe in full transparency. Here are honest answers to the questions Sacramento homeowners ask us most.')
    
    content += '    <section class="section">\n      <div class="container container--narrow">\n        <div class="faq-list">\n'
    for q, a in questions:
        content += f'''          <div class="faq-item">
            <button class="faq-item__trigger" aria-expanded="false">
              <span>{q}</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
            </button>
            <div class="faq-item__content"><p class="faq-item__answer">{a}</p></div>
          </div>
'''
    content += '        </div>\n      </div>\n    </section>\n'
    content += make_cta_section(pf, 'offer-form-faq')
    content += '  </main>\n'
    content += make_footer(pf)
    write_page(pf, content)


def build_reviews():
    pf = 'reviews.html'
    reviews = [
        ("Maria S.", "Sacramento, CA", "Sold in 10 days, avoided foreclosure", "I was facing foreclosure and had no idea what to do. Redwood made me an offer within a day and we closed in 10 days. They saved my credit and gave me peace of mind. I can't recommend them enough."),
        ("James & Linda T.", "Elk Grove, CA", "Inherited property, sold as-is", "After my father passed, we inherited a house across the country that needed major work. Redwood bought it as-is and the whole thing took 2 weeks. Couldn't have been easier. They handled everything."),
        ("David R.", "Roseville, CA", "Sold 2 rental properties", "I was tired of being a landlord. Problem tenants, constant repairs — I was done. Redwood bought both my rental properties and I finally got my life back. Fair price, zero hassle."),
        ("Sarah M.", "Rancho Cordova, CA", "Closed in 8 days during divorce", "Going through a divorce was hard enough without worrying about the house. Patrick and his team made the whole process painless. Got a fair offer and closed in just over a week. One less thing to stress about."),
        ("Robert & Ann K.", "Citrus Heights, CA", "Sold house with major foundation issues", "No one would touch our house because of foundation problems. Redwood made us a fair offer and didn't try to lowball us because of the damage. Honest people doing honest business."),
        ("Jennifer L.", "Folsom, CA", "Relocated for work, needed fast sale", "I got a job offer in another state and needed to sell fast. Redwood closed in 12 days and I was able to start my new job without worrying about an unsold house back home. Lifesaver."),
    ]
    
    review_schema = {"@context": "https://schema.org", "@type": "LocalBusiness", "name": "Redwood Real Estate Solutions",
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "bestRating": "5", "worstRating": "1", "ratingCount": str(len(reviews))},
        "review": [{"@type": "Review", "author": {"@type": "Person", "name": r[0]}, "reviewRating": {"@type": "Rating", "ratingValue": "5"}, "reviewBody": r[3]} for r in reviews]}
    breadcrumb_schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN},
        {"@type": "ListItem", "position": 2, "name": "Reviews", "item": DOMAIN + "/reviews.html"}
    ]}
    
    content = make_head(pf, 'Reviews & Testimonials — Homeowners Who Trusted Redwood | Redwood Real Estate',
        'Read real reviews from Sacramento homeowners who sold their houses for cash to Redwood Real Estate Solutions. 5-star rated, BBB accredited.',
        'reviews.html', [review_schema, breadcrumb_schema])
    content += make_header(pf, 'reviews')
    content += '  <main id="main">\n'
    content += make_breadcrumb(pf, [('Reviews', '')])
    content += make_page_hero('Success Stories', 'What Homeowners Say About Us', 'Real stories from real people we\'ve helped move on to the next chapter of their lives.')
    
    content += '    <section class="section">\n      <div class="container">\n        <div class="testimonials-grid testimonials-grid--full">\n'
    for name, location, detail, quote in reviews:
        stars = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>' * 5
        content += f'''          <div class="testimonial-card fade-in">
            <div class="testimonial-card__stars">{stars}</div>
            <p class="testimonial-card__quote">"{quote}"</p>
            <p class="testimonial-card__author">{name}</p>
            <p class="testimonial-card__location">{location}</p>
            <p class="testimonial-card__detail">{detail}</p>
          </div>
'''
    content += '        </div>\n'
    
    # Trust badges
    content += '''        <div class="trust-badges fade-in" style="margin-top:var(--space-16);">
          <a href="https://www.google.com/maps/place/Redwood+Real+Estate+Solutions" target="_blank" rel="noopener" class="trust-badge trust-badge--google" aria-label="View our Google Reviews">
            <div class="trust-badge__icon"><svg viewBox="0 0 24 24" width="32" height="32"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg></div>
            <div class="trust-badge__content"><div class="trust-badge__stars"><svg viewBox="0 0 120 20" width="96" height="16"><polygon points="12,0 15.09,7.36 23.27,8.18 17.14,13.64 18.82,21.82 12,17.77 5.18,21.82 6.86,13.64 0.73,8.18 8.91,7.36" fill="#FBBC05"/><polygon points="36,0 39.09,7.36 47.27,8.18 41.14,13.64 42.82,21.82 36,17.77 29.18,21.82 30.86,13.64 24.73,8.18 32.91,7.36" fill="#FBBC05"/><polygon points="60,0 63.09,7.36 71.27,8.18 65.14,13.64 66.82,21.82 60,17.77 53.18,21.82 54.86,13.64 48.73,8.18 56.91,7.36" fill="#FBBC05"/><polygon points="84,0 87.09,7.36 95.27,8.18 89.14,13.64 90.82,21.82 84,17.77 77.18,21.82 78.86,13.64 72.73,8.18 80.91,7.36" fill="#FBBC05"/><polygon points="108,0 111.09,7.36 119.27,8.18 113.14,13.64 114.82,21.82 108,17.77 101.18,21.82 102.86,13.64 96.73,8.18 104.91,7.36" fill="#FBBC05"/></svg></div><span class="trust-badge__label">5.0 Stars on Google</span></div>
          </a>
          <a href="https://www.bbb.org/" target="_blank" rel="noopener" class="trust-badge trust-badge--bbb" aria-label="BBB Accreditation">
            <div class="trust-badge__icon trust-badge__icon--bbb"><svg viewBox="0 0 80 40" width="64" height="32" fill="none"><rect x="1" y="1" width="78" height="38" rx="4" stroke="#006BA6" stroke-width="2"/><text x="40" y="18" text-anchor="middle" fill="#006BA6" font-family="Arial,sans-serif" font-weight="700" font-size="14">BBB</text><rect x="20" y="24" width="40" height="10" rx="2" fill="#006BA6"/><text x="40" y="32" text-anchor="middle" fill="#fff" font-family="Arial,sans-serif" font-weight="600" font-size="8">ACCREDITED</text></svg></div>
            <div class="trust-badge__content"><span class="trust-badge__rating">A+</span><span class="trust-badge__label">BBB Rating</span></div>
          </a>
        </div>
'''
    content += '      </div>\n    </section>\n'
    content += make_cta_section(pf, 'offer-form-reviews')
    content += '  </main>\n'
    content += make_footer(pf)
    write_page(pf, content)


def build_areas():
    pf = 'areas-we-serve.html'
    breadcrumb_schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN},
        {"@type": "ListItem", "position": 2, "name": "Areas We Serve", "item": DOMAIN + "/areas-we-serve.html"}
    ]}
    
    content = make_head(pf, 'Areas We Serve — Cash Home Buyers in Sacramento & Northern California | Redwood',
        'Redwood Real Estate Solutions buys houses for cash in Sacramento, Elk Grove, Roseville, Folsom, Rancho Cordova, Citrus Heights, and throughout Northern California.',
        'areas-we-serve.html', [breadcrumb_schema])
    content += make_header(pf, 'areas')
    content += '  <main id="main">\n'
    content += make_breadcrumb(pf, [('Areas We Serve', '')])
    content += make_page_hero('Areas We Serve', 'Cash Home Buyers Across Sacramento & Northern California', 'We buy houses in any condition throughout the Sacramento metropolitan area. Select your city below to learn more.')
    
    content += '    <section class="section">\n      <div class="container">\n        <div class="areas-grid">\n'
    for c in CITIES:
        content += f'''          <a href="sell-my-house-fast-{c['slug']}-ca.html" class="area-card fade-in">
            <h2 class="area-card__city">{c['name']}</h2>
            <p class="area-card__county">{c['county']}</p>
            <p class="area-card__stats">Population: {c['population']} &middot; Median Home: {c['median']}</p>
            <span class="area-card__link">Sell My House in {c['name']} →</span>
          </a>
'''
    content += '        </div>\n'
    
    # Additional areas
    content += '''        <div class="section__header section__header--center fade-in" style="margin-top:var(--space-16);">
          <h2 class="section__title">We Also Serve These Communities</h2>
          <p class="section__desc">Don't see your city? We buy houses throughout Northern California. Contact us to get your free cash offer.</p>
        </div>
        <div class="additional-areas fade-in">
          <span>Davis</span><span>Woodland</span><span>West Sacramento</span><span>Carmichael</span>
          <span>Fair Oaks</span><span>Orangevale</span><span>North Highlands</span><span>Antelope</span>
          <span>Rio Linda</span><span>Rocklin</span><span>Lincoln</span><span>Loomis</span>
          <span>Granite Bay</span><span>Auburn</span><span>Placerville</span><span>Galt</span>
        </div>
'''
    content += '      </div>\n    </section>\n'
    content += make_cta_section(pf, 'offer-form-areas')
    content += '  </main>\n'
    content += make_footer(pf)
    write_page(pf, content)


def build_city_page(city):
    slug = city['slug']
    name = city['name']
    pf = f'sell-my-house-fast-{slug}-ca.html'
    
    local_business = {"@context": "https://schema.org", "@type": "RealEstateAgent",
        "name": f"Redwood Real Estate Solutions — {name}",
        "url": f"{DOMAIN}/sell-my-house-fast-{slug}-ca.html",
        "address": {"@type": "PostalAddress", "addressLocality": name, "addressRegion": "CA", "addressCountry": "US"},
        "areaServed": {"@type": "City", "name": name},
        "description": f"We buy houses for cash in {name}, CA. No repairs, no commissions, close in as little as 7 days."}
    faq_items = [
        (f"How fast can you buy my house in {name}?", f"We can close on your {name} home in as little as 7 days. After you submit your information, we'll present a cash offer within 24 hours and you choose the closing date."),
        (f"Do you buy houses in any condition in {name}?", f"Yes. We buy houses in any condition throughout {name} — whether your home needs major repairs, has code violations, or is perfectly maintained. No repairs needed on your end."),
        (f"Are there really no fees when selling my {name} home to you?", f"Correct — zero fees, zero commissions, zero closing costs. The cash offer we present is the amount you receive at closing. We cover all transaction costs."),
    ]
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_items]}
    breadcrumb_schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN},
        {"@type": "ListItem", "position": 2, "name": "Areas We Serve", "item": DOMAIN + "/areas-we-serve.html"},
        {"@type": "ListItem", "position": 3, "name": name, "item": f"{DOMAIN}/sell-my-house-fast-{slug}-ca.html"}
    ]}
    
    content = make_head(pf, f'Sell My House Fast in {name}, CA — Cash Offer in 24 Hours | Redwood Real Estate',
        f'Need to sell your house fast in {name}, California? Redwood Real Estate Solutions buys homes for cash in any condition. No repairs, no commissions, close in 7 days. Get your free offer.',
        f'sell-my-house-fast-{slug}-ca.html', [local_business, faq_schema, breadcrumb_schema])
    content += make_header(pf, 'areas')
    content += '  <main id="main">\n'
    content += make_breadcrumb(pf, [('Areas We Serve', 'areas-we-serve.html'), (name, '')])
    content += make_page_hero(f'We Buy Houses in {name}', f'Sell My House Fast in {name}, CA', f'Get a fair, no-obligation cash offer on your {name} home within 24 hours. No repairs, no commissions, no hassle.')
    
    content += f'''    <section class="section">
      <div class="container">
        <div class="city-content">
          <div class="city-content__main fade-in">
            <h2>Cash Home Buyers in {name}, California</h2>
            <p>If you need to sell your house fast in {name}, Redwood Real Estate Solutions is here to help. We're local cash home buyers serving {city['desc']}. Whether you're facing foreclosure, going through a divorce, dealing with an inherited property, or simply need to sell quickly — we buy houses in any condition and close on your timeline.</p>
            <p>Unlike listing with a real estate agent (which typically takes 3-6 months, costs 5-6% in commissions, and requires expensive repairs), selling to Redwood means you get a cash offer within 24 hours, pay zero fees, make zero repairs, and close in as few as 7 days.</p>
            
            <h3>Why {name} Homeowners Choose Redwood</h3>
            <ul class="city-benefits">
              <li><strong>Fast Cash Offers:</strong> We present a fair, all-cash offer within 24 hours of learning about your property.</li>
              <li><strong>Close on Your Schedule:</strong> Whether you need 7 days or 60 days, you pick the closing date.</li>
              <li><strong>No Repairs Required:</strong> Foundation issues, roof damage, mold, code violations — we buy homes as-is.</li>
              <li><strong>Zero Fees:</strong> No agent commissions, no closing costs, no hidden charges.</li>
              <li><strong>Local Expertise:</strong> We know the {name} market inside and out — from {city['zip_sample']} and beyond.</li>
            </ul>

            <h3>About the {name} Housing Market</h3>
            <p>With a population of {city['population']} and a median home price of {city['median']}, {name} is {city['desc']}. Whether your property is a single-family home, condo, duplex, or mobile home, we're interested in making you a fair offer.</p>
            <p>Many {name} homeowners come to us after discovering that the traditional selling process doesn't work for their situation. Between agent commissions (typically 5-6% of the sale price), repair costs ($5,000-$30,000+), and months of waiting, the traditional route can cost far more than most people realize.</p>

            <h3>Situations We Help {name} Homeowners With</h3>
            <div class="situations-list situations-list--compact">
              <div class="situation-item"><svg class="situation-item__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg><span>Facing Foreclosure</span></div>
              <div class="situation-item"><svg class="situation-item__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg><span>Inherited Property</span></div>
              <div class="situation-item"><svg class="situation-item__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg><span>Divorce</span></div>
              <div class="situation-item"><svg class="situation-item__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg><span>Behind on Payments</span></div>
              <div class="situation-item"><svg class="situation-item__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg><span>Job Relocation</span></div>
              <div class="situation-item"><svg class="situation-item__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg><span>Tired Landlord</span></div>
              <div class="situation-item"><svg class="situation-item__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg><span>Major Repairs Needed</span></div>
              <div class="situation-item"><svg class="situation-item__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg><span>Code Violations</span></div>
            </div>
          </div>
          <div class="city-content__sidebar fade-in">
            <div class="city-stats-card">
              <h3 class="city-stats-card__title">{name} at a Glance</h3>
              <div class="city-stat"><span class="city-stat__label">Population</span><span class="city-stat__value">{city['population']}</span></div>
              <div class="city-stat"><span class="city-stat__label">Median Home Price</span><span class="city-stat__value">{city['median']}</span></div>
              <div class="city-stat"><span class="city-stat__label">County</span><span class="city-stat__value">{city['county']}</span></div>
              <div class="city-stat"><span class="city-stat__label">ZIP Codes</span><span class="city-stat__value">{city['zip_sample']}</span></div>
            </div>
            <div class="city-process-card">
              <h3>How It Works</h3>
              <div class="mini-step"><span class="mini-step__num">1</span><span>Tell us about your {name} property</span></div>
              <div class="mini-step"><span class="mini-step__num">2</span><span>Get a fair cash offer in 24 hours</span></div>
              <div class="mini-step"><span class="mini-step__num">3</span><span>Pick your closing date</span></div>
              <div class="mini-step"><span class="mini-step__num">4</span><span>Get paid — we cover all costs</span></div>
              <a href="#get-offer" class="city-sidebar-cta">Get My Cash Offer →</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container container--narrow">
        <div class="section__header section__header--center fade-in">
          <h2 class="section__title">Common Questions About Selling in {name}</h2>
        </div>
        <div class="faq-list">
'''
    for q, a in faq_items:
        content += f'''          <div class="faq-item">
            <button class="faq-item__trigger" aria-expanded="false"><span>{q}</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button>
            <div class="faq-item__content"><p class="faq-item__answer">{a}</p></div>
          </div>
'''
    content += '        </div>\n      </div>\n    </section>\n'
    content += make_cta_section(pf, f'offer-form-{slug}')
    content += '  </main>\n'
    content += make_footer(pf)
    write_page(pf, content)


def build_blog_index():
    pf = 'blog.html'
    breadcrumb_schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": DOMAIN + "/blog.html"}
    ]}
    
    posts = [
        ("How to Sell Your House Fast in Sacramento: The Complete 2026 Guide", "blog-sell-house-fast-sacramento.html", "Selling Guide", "Apr 1, 2026", "2026-04-01", "8 min read",
         "Learn the fastest ways to sell your Sacramento home for cash — from preparing your property to understanding your options beyond a traditional listing."),
        ("How to Avoid Foreclosure in Sacramento: 5 Options You Need to Know", "blog-avoid-foreclosure-sacramento.html", "Foreclosure", "Mar 25, 2026", "2026-03-25", "6 min read",
         "Facing foreclosure in Sacramento County? Discover five proven strategies to stop foreclosure and protect your credit."),
        ("Inherited a House in California? Here's How to Sell It Quickly", "blog-inherited-house-california.html", "Inherited Property", "Mar 18, 2026", "2026-03-18", "7 min read",
         "Navigating probate, taxes, and maintenance on an inherited home can be overwhelming. Learn how to sell an inherited property quickly and stress-free."),
        ("Sacramento Housing Market Update: What Sellers Need to Know in 2026", "blog-sacramento-market-2026.html", "Market Update", "Mar 10, 2026", "2026-03-10", "5 min read",
         "Is now a good time to sell in Sacramento? Current pricing trends, inventory levels, and what the 2026 market means for homeowners."),
        ("Cash Home Buyers vs. Real Estate Agents: Which Is Right for You?", "blog-cash-buyers-vs-agents.html", "Comparison", "Mar 3, 2026", "2026-03-03", "6 min read",
         "Compare the pros and cons of working with a cash buyer versus listing with a traditional real estate agent."),
        ("How to Sell a House with Code Violations in California", "blog-sell-house-code-violations.html", "Selling Tips", "Feb 24, 2026", "2026-02-24", "5 min read",
         "Code violations don't have to stop you from selling. Learn your options for selling a property with building code issues in California."),
    ]
    
    content = make_head(pf, 'Blog — Sacramento Real Estate Guides & Tips | Redwood Real Estate Solutions',
        'Expert advice on selling your home fast for cash, navigating foreclosure, inherited properties, and understanding the Sacramento real estate market.',
        'blog.html', [breadcrumb_schema])
    content += make_header(pf, 'blog')
    content += '  <main id="main">\n'
    content += make_breadcrumb(pf, [('Blog', '')])
    content += make_page_hero('Resources & Insights', 'Homeowner Guides & Tips', 'Expert advice on selling your home, navigating tricky situations, and understanding the Sacramento real estate market.')
    
    content += '    <section class="section">\n      <div class="container">\n        <div class="blog-grid">\n'
    for title, href, cat, date_str, date_iso, read_time, excerpt in posts:
        content += f'''          <article class="blog-card fade-in" itemscope itemtype="https://schema.org/Article">
            <div class="blog-card__meta">
              <span class="blog-card__category">{cat}</span>
              <time class="blog-card__date" datetime="{date_iso}" itemprop="datePublished">{date_str}</time>
            </div>
            <h2 class="blog-card__title" itemprop="headline"><a href="{href}" itemprop="url">{title}</a></h2>
            <p class="blog-card__excerpt" itemprop="description">{excerpt}</p>
            <div class="blog-card__footer">
              <span class="blog-card__read-time">{read_time}</span>
              <span class="blog-card__arrow" aria-hidden="true">→</span>
            </div>
            <meta itemprop="author" content="Patrick Mahoney">
          </article>
'''
    content += '        </div>\n      </div>\n    </section>\n'
    content += make_cta_section(pf, 'offer-form-blog')
    content += '  </main>\n'
    content += make_footer(pf)
    write_page(pf, content)


def build_blog_post(slug, title, category, date_str, date_iso, read_time, description, body_html):
    pf = f'blog-{slug}.html'
    schema = {"@context": "https://schema.org", "@type": "Article",
        "headline": title, "datePublished": date_iso, "dateModified": date_iso,
        "author": {"@type": "Person", "name": "Patrick Mahoney"},
        "publisher": {"@type": "Organization", "name": "Redwood Real Estate Solutions", "url": DOMAIN},
        "description": description, "mainEntityOfPage": f"{DOMAIN}/blog-{slug}.html"}
    breadcrumb_schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": DOMAIN + "/blog.html"},
        {"@type": "ListItem", "position": 3, "name": title, "item": f"{DOMAIN}/blog-{slug}.html"}
    ]}
    
    content = make_head(pf, f'{title} | Redwood Real Estate Solutions', description, f'blog-{slug}.html', [schema, breadcrumb_schema])
    content += make_header(pf, 'blog')
    content += '  <main id="main">\n'
    content += make_breadcrumb(pf, [('Blog', 'blog.html'), (title[:50] + '...' if len(title) > 50 else title, '')])
    
    content += f'''    <article class="blog-post">
      <header class="blog-post__header">
        <div class="container container--narrow">
          <span class="blog-post__category">{category}</span>
          <h1 class="blog-post__title">{title}</h1>
          <div class="blog-post__meta">
            <span class="blog-post__author">By Patrick Mahoney</span>
            <time datetime="{date_iso}">{date_str}</time>
            <span>{read_time}</span>
          </div>
        </div>
      </header>
      <div class="blog-post__body">
        <div class="container container--narrow">
{body_html}
        </div>
      </div>
    </article>
'''
    content += make_cta_section(pf, f'offer-form-{slug}')
    content += '  </main>\n'
    content += make_footer(pf)
    write_page(pf, content)


def build_sitemap():
    pages = [
        ('', '1.0', 'weekly'),
        ('how-it-works.html', '0.9', 'monthly'),
        ('about.html', '0.8', 'monthly'),
        ('reviews.html', '0.8', 'monthly'),
        ('faq.html', '0.8', 'monthly'),
        ('areas-we-serve.html', '0.9', 'weekly'),
        ('blog.html', '0.8', 'weekly'),
    ]
    for c in CITIES:
        pages.append((f'sell-my-house-fast-{c["slug"]}-ca.html', '0.8', 'monthly'))
    
    blog_slugs = ['sell-house-fast-sacramento', 'avoid-foreclosure-sacramento', 'inherited-house-california',
                  'sacramento-market-2026', 'cash-buyers-vs-agents', 'sell-house-code-violations']
    for s in blog_slugs:
        pages.append((f'blog-{s}.html', '0.7', 'monthly'))
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    today = datetime.now().strftime('%Y-%m-%d')
    for path, priority, freq in pages:
        url = DOMAIN + '/' + path if path else DOMAIN + '/'
        xml += f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{priority}</priority>\n  </url>\n'
    xml += '</urlset>\n'
    write_page('sitemap.xml', xml)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BLOG POST CONTENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BLOG_SELL_FAST = """
          <p>Selling a house quickly in Sacramento doesn't have to mean accepting a lowball offer or dealing with months of stress. Whether you're facing a life change, financial pressure, or simply want to move on, there are proven strategies to sell your Sacramento home fast while still getting a fair price.</p>

          <h2>Understanding Your Options</h2>
          <p>Sacramento homeowners looking to sell quickly generally have three paths: listing with a real estate agent, selling For Sale By Owner (FSBO), or selling directly to a cash home buyer. Each has distinct advantages depending on your situation, timeline, and how much effort you want to invest.</p>

          <h3>Option 1: List with a Real Estate Agent</h3>
          <p>The traditional route involves hiring a listing agent, preparing your home for showings, and waiting for a qualified buyer. In the current Sacramento market, well-priced homes in good condition can sell in 30-60 days. However, when you factor in agent commissions (typically 5-6%), repair costs, staging, and closing costs, you may net significantly less than the sale price suggests.</p>
          <p><strong>Best for:</strong> Homeowners who have time (3-6 months), a home in good condition, and want to maximize sale price regardless of costs and timeline.</p>

          <h3>Option 2: Sell FSBO (For Sale By Owner)</h3>
          <p>Selling without an agent saves on commissions but requires you to handle marketing, showings, negotiations, and paperwork yourself. In Sacramento, FSBO homes typically sell for less than agent-listed homes and take longer to close.</p>
          <p><strong>Best for:</strong> Experienced sellers with time, marketing skills, and a home that's move-in ready.</p>

          <h3>Option 3: Sell to a Cash Home Buyer</h3>
          <p>Cash home buyers like <a href="./index.html">Redwood Real Estate Solutions</a> purchase homes directly — no agents, no commissions, no repairs needed. You receive a cash offer (usually within 24 hours) and can close in as little as 7 days. The trade-off is typically a lower sale price than a perfect open-market sale, but when you account for the commissions, repairs, and months of carrying costs you avoid, the net difference is often much smaller than expected.</p>
          <p><strong>Best for:</strong> Homeowners who need speed, have properties that need work, or want to avoid the hassle of the traditional process.</p>

          <h2>How to Prepare for a Fast Sale</h2>
          <p>Regardless of which selling method you choose, these steps will help you move faster:</p>
          <ol>
            <li><strong>Gather your documents early.</strong> Locate your deed, mortgage statement, tax records, and any HOA documents. Having these ready prevents delays.</li>
            <li><strong>Know your home's value.</strong> Research recent comparable sales in your Sacramento neighborhood. Sites like Zillow, Redfin, and Realtor.com provide free estimates, though in-person evaluations are more accurate.</li>
            <li><strong>Be realistic about condition.</strong> If your home needs major work, factor repair costs into your expectations. A cash buyer who takes the property as-is saves you those costs and the time to manage contractors.</li>
            <li><strong>Understand your timeline.</strong> Know your hard deadline. If you need to close by a certain date, work backward from there.</li>
          </ol>

          <h2>Sacramento-Specific Tips</h2>
          <p>The Sacramento real estate market has its own dynamics that affect how fast you can sell:</p>
          <ul>
            <li><strong>Seasonality matters less for cash sales.</strong> While the spring/summer market is traditionally stronger for listed homes, cash buyers operate year-round with consistent timelines.</li>
            <li><strong>Neighborhoods vary widely.</strong> A home in Land Park or East Sacramento may attract different buyer pools than one in North Sacramento or Del Paso Heights. Cash buyers serve all areas equally.</li>
            <li><strong>California disclosure requirements apply.</strong> Even in a fast sale, California law requires sellers to disclose known defects. A reputable cash buyer will help you understand your obligations.</li>
          </ul>

          <h2>Red Flags to Watch For</h2>
          <p>If you're considering a cash buyer, protect yourself by watching for these warning signs:</p>
          <ul>
            <li>Offers that seem too good to be true</li>
            <li>Pressure to sign immediately without time to review</li>
            <li>Lack of a physical address or verifiable business history</li>
            <li>Requests for upfront fees (legitimate buyers never charge sellers)</li>
            <li>Unwillingness to explain how they calculated the offer</li>
          </ul>
          <p>A trustworthy cash home buyer will be transparent about their process, provide references, and give you time to make your decision. At <a href="./index.html">Redwood Real Estate Solutions</a>, we walk you through our offer formula and never pressure you to accept.</p>

          <h2>Ready to Get Your Free Cash Offer?</h2>
          <p>If you're a Sacramento homeowner looking to sell fast, <a href="./index.html#get-offer">request your free, no-obligation cash offer</a> today. We'll evaluate your property and present you with a fair offer within 24 hours — no strings attached.</p>
"""

BLOG_FORECLOSURE = """
          <p>Facing foreclosure in Sacramento is stressful, but you have more options than you might think. The key is acting quickly — the sooner you explore your alternatives, the more leverage you have to protect your credit, your equity, and your family's future.</p>

          <h2>Understanding Foreclosure in California</h2>
          <p>California is a non-judicial foreclosure state, meaning lenders can foreclose without going through the court system. The process typically takes about 120 days from the first missed payment to the Notice of Default, then another 90+ days to the auction. That gives you roughly 4-7 months to find a solution — but earlier action gives you significantly better options.</p>

          <h2>Option 1: Contact Your Lender Immediately</h2>
          <p>This should be your first call. Most lenders would rather work with you than go through the expensive foreclosure process. Options they may offer include:</p>
          <ul>
            <li><strong>Loan modification:</strong> Changing the terms of your loan to lower monthly payments</li>
            <li><strong>Forbearance agreement:</strong> Temporarily reducing or pausing payments</li>
            <li><strong>Repayment plan:</strong> Spreading missed payments over future months</li>
          </ul>
          <p>Be honest about your situation. Lenders have dedicated loss mitigation departments specifically for this purpose.</p>

          <h2>Option 2: Explore Government Assistance Programs</h2>
          <p>Several programs exist to help Sacramento homeowners avoid foreclosure:</p>
          <ul>
            <li><strong>California Mortgage Relief Program:</strong> Provides up to $80,000 in assistance for past-due mortgage payments, property taxes, and other housing costs for eligible homeowners.</li>
            <li><strong>HUD-Approved Housing Counseling:</strong> Free counseling services that help you understand your options and negotiate with your lender. Find a local counselor at hud.gov.</li>
            <li><strong>Sacramento County resources:</strong> Local nonprofits offer foreclosure prevention counseling and financial literacy programs.</li>
          </ul>

          <h2>Option 3: Sell Your Home Before Foreclosure</h2>
          <p>If keeping your home isn't feasible, selling before the foreclosure completes protects your credit score (a foreclosure stays on your record for 7 years) and lets you walk away with remaining equity.</p>
          <p><strong>Traditional sale:</strong> If you have 3-6 months and your home is in good condition, listing with an agent may net the highest price. However, if time is short, this may not be realistic.</p>
          <p><strong>Cash sale:</strong> Selling to a cash buyer like <a href="./index.html">Redwood Real Estate Solutions</a> is often the fastest option. We can close in as few as 7 days, helping you avoid the foreclosure entirely. Many of our clients came to us facing foreclosure and were able to sell their home, pay off their mortgage, and walk away with cash in their pocket.</p>

          <h2>Option 4: Short Sale</h2>
          <p>If you owe more than your home is worth, your lender may agree to a short sale — accepting less than the full mortgage balance. This requires lender approval and can take 2-4 months, but it's less damaging to your credit than a foreclosure.</p>

          <h2>Option 5: Bankruptcy (Last Resort)</h2>
          <p>Filing for Chapter 13 bankruptcy can temporarily halt foreclosure proceedings through an automatic stay, giving you time to reorganize your debts. This is a serious step with long-term consequences and should only be considered after consulting with a bankruptcy attorney.</p>

          <h2>What NOT to Do</h2>
          <ul>
            <li><strong>Don't ignore the notices.</strong> Every day you wait reduces your options.</li>
            <li><strong>Don't abandon the property.</strong> An empty home deteriorates faster and may attract vandalism.</li>
            <li><strong>Don't fall for rescue scams.</strong> Be wary of anyone who asks you to sign over your deed or pay upfront fees to "save" your home.</li>
          </ul>

          <h2>Take Action Today</h2>
          <p>If you're a Sacramento homeowner facing foreclosure, time is your most valuable asset. <a href="./index.html#get-offer">Contact Redwood Real Estate Solutions</a> for a free, no-obligation cash offer. We can often close before your foreclosure date, helping you protect your credit and move forward with dignity.</p>
"""

BLOG_INHERITED = """
          <p>Inheriting a house in California can be both emotionally and logistically overwhelming. Between navigating probate, understanding tax implications, managing a property you may not live near, and making decisions during a difficult time — it's a lot. This guide walks you through your options for selling an inherited property quickly and stress-free.</p>

          <h2>Step 1: Understand the Probate Process</h2>
          <p>In California, most inherited properties must go through probate — the legal process of transferring ownership from the deceased to the heir(s). Probate in California typically takes 7-12 months, though simplified procedures exist for smaller estates.</p>
          <p><strong>Key point:</strong> You can often begin the selling process during probate. California law allows the personal representative (executor) to sell real property with court approval, and many cash buyers are experienced with probate transactions.</p>
          <ul>
            <li><strong>Full probate:</strong> Required for estates over $184,500 (2024 threshold). Takes 7-12+ months.</li>
            <li><strong>Small estate affidavit:</strong> For estates under the threshold. Faster and simpler.</li>
            <li><strong>Living trust:</strong> If the property was in a trust, probate may be avoided entirely.</li>
          </ul>

          <h2>Step 2: Know Your Tax Obligations</h2>
          <p>California's tax rules for inherited property include some significant benefits:</p>
          <ul>
            <li><strong>Stepped-up basis:</strong> When you inherit a property, your tax basis is "stepped up" to the fair market value at the time of the owner's death. This means if you sell soon after inheriting, you may owe little or no capital gains tax.</li>
            <li><strong>Property tax reassessment:</strong> Under Proposition 19, inherited properties used as primary residences by the heir receive a limited exclusion from reassessment. Investment or second properties will be reassessed at current market value.</li>
            <li><strong>No inheritance tax:</strong> California does not have a state inheritance or estate tax.</li>
          </ul>
          <p>Consult with a tax professional for advice specific to your situation.</p>

          <h2>Step 3: Evaluate the Property's Condition</h2>
          <p>Inherited homes often need work — sometimes significant work. Common issues include:</p>
          <ul>
            <li>Deferred maintenance (roofing, plumbing, electrical)</li>
            <li>Outdated systems and finishes</li>
            <li>Items left behind that need clearing</li>
            <li>Potential code violations or unpermitted additions</li>
          </ul>
          <p>Before deciding whether to renovate and list or sell as-is, get a realistic estimate of repair costs. If the property needs $30,000+ in work and you'd rather not manage a renovation from afar, selling as-is to a cash buyer may be the most practical path.</p>

          <h2>Step 4: Decide How to Sell</h2>
          <h3>Option A: List with an Agent</h3>
          <p>If the property is in good condition and you have time, listing with a Sacramento real estate agent can maximize the sale price. Expect 3-6 months for the full process, plus 5-6% in commissions and potential repair costs.</p>

          <h3>Option B: Sell to a Cash Home Buyer</h3>
          <p>A cash buyer like <a href="./index.html">Redwood Real Estate Solutions</a> will purchase the property as-is — no repairs, no cleaning out, no staging, no waiting. This is especially useful when:</p>
          <ul>
            <li>The property needs significant repairs</li>
            <li>You live far away and can't manage showings</li>
            <li>Multiple heirs want to split the proceeds quickly</li>
            <li>You want to avoid the carrying costs (property taxes, insurance, utilities, maintenance)</li>
            <li>You need to settle the estate promptly</li>
          </ul>

          <h2>Step 5: Handle the Practical Details</h2>
          <p>While waiting for the sale to process:</p>
          <ol>
            <li><strong>Secure the property:</strong> Make sure it's locked, insured, and maintained.</li>
            <li><strong>Continue paying property taxes and insurance:</strong> These remain your responsibility until the sale closes.</li>
            <li><strong>Notify the utility companies:</strong> Transfer or maintain accounts to prevent damage (e.g., frozen pipes in winter).</li>
            <li><strong>Check for liens or outstanding debts:</strong> These will need to be resolved at closing.</li>
          </ol>

          <h2>Sell Your Inherited Property Quickly</h2>
          <p>If you've inherited a property in Sacramento or anywhere in Northern California and want to sell it quickly without the burden of repairs and a lengthy listing process, <a href="./index.html#get-offer">contact Redwood Real Estate Solutions</a>. We specialize in inherited property purchases and can close on your timeline — even during probate.</p>
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN BUILD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    print('Building Redwood Real Estate Solutions — Multi-Page Site')
    print('=' * 60)
    
    # Core pages
    build_how_it_works()
    build_about()
    build_faq()
    build_reviews()
    build_areas()
    
    # City pages
    for city in CITIES:
        build_city_page(city)
    
    # Blog
    build_blog_index()
    
    build_blog_post('sell-house-fast-sacramento',
        'How to Sell Your House Fast in Sacramento: The Complete 2026 Guide',
        'Selling Guide', 'April 1, 2026', '2026-04-01', '8 min read',
        'Learn the fastest ways to sell your Sacramento home for cash — from preparing your property to understanding your options beyond a traditional listing.',
        BLOG_SELL_FAST)
    
    build_blog_post('avoid-foreclosure-sacramento',
        'How to Avoid Foreclosure in Sacramento: 5 Options You Need to Know',
        'Foreclosure', 'March 25, 2026', '2026-03-25', '6 min read',
        'Facing foreclosure in Sacramento County? Discover five proven strategies to stop foreclosure and protect your credit — including selling your house fast for cash.',
        BLOG_FORECLOSURE)
    
    build_blog_post('inherited-house-california',
        "Inherited a House in California? Here's How to Sell It Quickly",
        'Inherited Property', 'March 18, 2026', '2026-03-18', '7 min read',
        'Navigating probate, taxes, and maintenance on an inherited home can be overwhelming. Learn how to sell an inherited property in California quickly.',
        BLOG_INHERITED)
    
    # Sitemap
    build_sitemap()
    
    print('=' * 60)
    print('Build complete!')

if __name__ == '__main__':
    main()
