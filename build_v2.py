#!/usr/bin/env python3
"""
Redwood Real Estate Solutions — Multi-Location SEO Architecture Generator
Generates all state hub, county, and city pages for CA and MT hierarchies.
Reuses shared template functions from existing build.py patterns.
"""

import os, json
from datetime import datetime

BASE   = '/home/user/workspace/redwood-realestate'
DOMAIN = 'https://www.redwood-realestate.com'

# ── Navigation ──────────────────────────────────────────────
NAV = [
    ('Home',          'index.html',        'home'),
    ('How It Works',  'how-it-works.html', 'how-it-works'),
    ('Areas We Serve','areas-we-serve.html','areas'),
    ('Reviews',       'reviews.html',      'reviews'),
    ('FAQ',           'faq.html',          'faq'),
    ('Blog',          'blog.html',         'blog'),
]

# ── City data used by footer ─────────────────────────────────
FOOTER_CITIES = [
    {'name': 'Sacramento', 'slug': 'sacramento', 'state': 'california'},
    {'name': 'Elk Grove',  'slug': 'elk-grove',  'state': 'california'},
    {'name': 'Roseville',  'slug': 'roseville',  'state': 'california'},
    {'name': 'Folsom',     'slug': 'folsom',      'state': 'california'},
    {'name': 'Kalispell',  'slug': 'kalispell',   'state': 'montana'},
    {'name': 'Missoula',   'slug': 'missoula',    'state': 'montana'},
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOCATION DATA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CA_COUNTIES = [
    {
        'name': 'Sacramento County',
        'slug': 'sacramento-county',
        'population': '1,618,000',
        'median': '$525,000',
        'seat': 'Sacramento',
        'lat': 38.58, 'lng': -121.49,
        'zips': '95823, 95630, 95624, 95758, 95828, 95608, 95670',
        'market_desc': 'Sacramento County is the state capital region of Northern California, home to a diverse economy anchored by government, healthcare, and a growing tech sector. Significant Bay Area migration over the past decade has driven sustained demand, making it one of the most active real estate markets in the state while still offering prices far below coastal California.',
        'sell_reasons': 'job relocations, inherited properties, divorce settlements, pre-foreclosure situations, and military Permanent Change of Station (PCS) orders',
        'cities': [
            {'name': 'Sacramento',     'slug': 'sacramento',     'population': '541,000',  'median': '$430,000', 'zips': '95814, 95816, 95818, 95820', 'desc': 'the state capital and the economic heart of Northern California, home to government offices, major healthcare systems, and a fast-growing tech sector'},
            {'name': 'Elk Grove',      'slug': 'elk-grove',      'population': '186,000',  'median': '$575,000', 'zips': '95624, 95757, 95758',         'desc': 'one of the fastest-growing cities in California, known for its master-planned neighborhoods, top-rated schools, and family-friendly community'},
            {'name': 'Folsom',         'slug': 'folsom',         'population': '92,000',   'median': '$680,000', 'zips': '95630',                        'desc': 'a highly desirable city in eastern Sacramento County, celebrated for Folsom Lake, Intel\'s major campus, and outstanding school districts'},
            {'name': 'Citrus Heights', 'slug': 'citrus-heights', 'population': '87,000',   'median': '$425,000', 'zips': '95610, 95621',                 'desc': 'a well-established suburban community in northeast Sacramento County with a diverse mix of homeowners and strong neighborhood associations'},
            {'name': 'Rancho Cordova', 'slug': 'rancho-cordova', 'population': '79,000',   'median': '$445,000', 'zips': '95670, 95742',                 'desc': 'a growing Sacramento suburb with a diverse housing stock, light rail access, and an expanding employment base in aerospace and defense'},
        ],
        'faq': [
            ("How quickly can you buy my house in Sacramento County?",
             "We can close on Sacramento County homes in as few as 7 days. After you contact us with property details, we present a cash offer within 24 hours and let you choose the closing date — whether that's one week or two months from now."),
            ("Do you buy houses in all Sacramento County cities?",
             "Yes. We serve all communities in Sacramento County, including Sacramento, Elk Grove, Folsom, Citrus Heights, Rancho Cordova, Carmichael, Fair Oaks, Orangevale, North Highlands, and every unincorporated area in between."),
            ("My Sacramento County home needs major repairs. Will you still buy it?",
             "Absolutely. We purchase Sacramento County homes in any condition — water damage, fire damage, foundation issues, code violations, outdated systems, and everything in between. You never have to make a single repair."),
            ("Are there any commissions or fees when selling to Redwood in Sacramento County?",
             "None whatsoever. No agent commissions, no closing costs, no transaction fees. The cash figure in your offer is the full amount you receive at closing."),
            ("What is the current real estate market like in Sacramento County?",
             "Sacramento County has a median home price around $525,000, driven by Bay Area migration and strong local employment in government and healthcare. While the market has moderated from its 2022 peak, well-located properties still attract multiple buyers. Cash sales remain a fast, certain alternative for homeowners who can't or don't want to navigate the traditional process."),
        ],
    },
    {
        'name': 'Napa County',
        'slug': 'napa-county',
        'population': '133,000',
        'median': '$950,000',
        'seat': 'Napa',
        'lat': 38.30, 'lng': -122.29,
        'zips': '94558, 94559, 94503, 94574, 94515',
        'market_desc': 'Napa County is synonymous with world-class wine country and luxury living, with a median home price near $950,000. Its proximity to the Bay Area fuels demand from high-earning professionals, while the county\'s limited housing supply keeps prices elevated. Tourism, viticulture, and hospitality anchor the local economy, creating a unique real estate landscape dominated by estates, vineyard properties, and upscale residences.',
        'sell_reasons': 'high property taxes, estate maintenance costs, downsizing, relocation, and concerns about wildfire and earthquake risk',
        'cities': [
            {'name': 'Napa',            'slug': 'napa',            'population': '76,000', 'median': '$800,000',   'zips': '94558, 94559', 'desc': 'the county seat and largest city in Napa Valley, blending world-renowned wine culture with a revitalized downtown, fine dining, and premium real estate'},
            {'name': 'American Canyon', 'slug': 'american-canyon', 'population': '22,000', 'median': '$700,000',   'zips': '94503',        'desc': 'the most affordable gateway to Napa County, popular with Bay Area commuters seeking wine country living at relatively lower price points'},
            {'name': 'St. Helena',      'slug': 'st-helena',       'population': '5,200',  'median': '$1,200,000', 'zips': '94574',        'desc': 'an exclusive Napa Valley enclave at the heart of the most prestigious wine corridor in America, featuring luxury estates and boutique vineyard properties'},
        ],
        'faq': [
            ("Can you buy luxury or vineyard properties in Napa County?",
             "Yes. We evaluate all property types in Napa County, including luxury homes, vineyard estates, and commercial-residential mixed properties. Larger or more complex properties may require a slightly longer evaluation period, but we still aim to present an offer within 48 hours."),
            ("Do you buy Napa County homes with fire or earthquake damage?",
             "We purchase Napa County properties regardless of condition, including those with fire damage, earthquake-related foundation issues, smoke damage, or deferred maintenance from years of estate ownership. No repairs are required."),
            ("High property taxes in Napa County are driving me to sell — can you help?",
             "Absolutely. Many Napa County homeowners are burdened by property taxes on estates they've outgrown or inherited. A fast cash sale allows you to liquidate the asset quickly without listing costs, carrying costs, or months of uncertainty."),
            ("What is the typical timeline for selling my Napa County home to Redwood?",
             "We can close in as few as 7 days, though Napa County transactions for larger or more complex properties sometimes take 14-21 days to fully process title and escrow. We'll give you a realistic timeline upfront with no surprises."),
        ],
    },
    {
        'name': 'Sonoma County',
        'slug': 'sonoma-county',
        'population': '485,000',
        'median': '$773,000',
        'seat': 'Santa Rosa',
        'lat': 38.51, 'lng': -122.93,
        'zips': '95403, 95407, 95404, 94954, 95401, 95476, 94928',
        'market_desc': 'Sonoma County blends coastal redwoods, wine country prestige, and Bay Area accessibility into one of Northern California\'s most desirable regions. With over 350 wineries, a thriving tourism industry, and strong demand from Bay Area relocators, the county commands a median home price near $773,000. The ongoing wildfire risk has shaped insurance markets and seller motivations across the region.',
        'sell_reasons': 'wildfire damage, uninsurable properties, rising insurance premiums, downsizing seniors, estate sales, and Bay Area relocations',
        'cities': [
            {'name': 'Santa Rosa',   'slug': 'santa-rosa',   'population': '177,000', 'median': '$700,000', 'zips': '95403, 95407, 95404, 95401', 'desc': 'the county seat and commercial hub of Sonoma County, a city rebuilding with renewed energy after the devastating 2017 Tubbs Fire — with a strong local economy and proximity to both wine country and the coast'},
            {'name': 'Petaluma',     'slug': 'petaluma',     'population': '59,000',  'median': '$800,000', 'zips': '94952, 94954',               'desc': 'a charming Southern Sonoma city beloved for its Victorian architecture, thriving restaurant scene, and SMART train access to the Bay Area'},
            {'name': 'Rohnert Park', 'slug': 'rohnert-park', 'population': '45,000',  'median': '$620,000', 'zips': '94928',                      'desc': 'a planned suburban community in central Sonoma County with one of the county\'s more affordable price points, home to Sonoma State University'},
        ],
        'faq': [
            ("Do you buy wildfire-damaged homes in Sonoma County?",
             "Yes. We purchase fire-damaged, smoke-damaged, and fully destroyed properties in Sonoma County. We can often close quickly, allowing homeowners to avoid carrying costs on a property they cannot live in or easily insure."),
            ("My Sonoma County home is uninsurable — will you still make an offer?",
             "Yes. We work with many Sonoma County homeowners whose properties have become difficult or impossible to insure due to wildfire risk. This is not a barrier for a cash purchase, as we assume the property risk ourselves."),
            ("How does Redwood determine offer prices for Sonoma County homes?",
             "We analyze recent comparable sales throughout the specific neighborhood or community, factor in the property's condition, and account for any special circumstances (fire risk, deferred maintenance, etc.). We then present a transparent offer with a clear explanation of how we arrived at the number."),
            ("Can you buy my Sonoma County home during a divorce?",
             "Yes, and we work with these situations regularly. We can work with both parties or with the appointed representative, close on a timeline that fits the legal proceedings, and ensure proceeds are handled according to the agreed split."),
        ],
    },
    {
        'name': 'Contra Costa County',
        'slug': 'contra-costa-county',
        'population': '1,173,000',
        'median': '$750,000',
        'seat': 'Martinez',
        'lat': 38.02, 'lng': -122.13,
        'zips': '94565, 94509, 94513, 94806, 94553, 94582',
        'market_desc': 'Contra Costa County anchors the East Bay with a population exceeding 1.1 million and a housing market driven by BART access to San Francisco and Oakland. The county encompasses everything from the affordable Delta communities to the affluent Lamorinda corridor, attracting a diverse mix of tech workers, healthcare professionals, and logistics industry employees who need Bay Area access without Bay Area prices.',
        'sell_reasons': 'job relocations, divorce, inherited properties, costly deferred repairs, and tired landlords dealing with tenant issues',
        'cities': [
            {'name': 'Concord',      'slug': 'concord',      'population': '123,000', 'median': '$680,000', 'zips': '94519, 94520, 94521, 94522', 'desc': 'the largest city in Contra Costa County and a major BART hub, offering suburban convenience with access to East Bay employment centers and San Francisco'},
            {'name': 'Antioch',      'slug': 'antioch',      'population': '120,000', 'median': '$550,000', 'zips': '94509, 94531',               'desc': 'a fast-growing Delta city in east Contra Costa County with some of the most affordable price points in the Bay Area and expanding e-commerce employment'},
            {'name': 'Richmond',     'slug': 'richmond',     'population': '115,000', 'median': '$550,000', 'zips': '94801, 94804, 94806',        'desc': 'a diverse West Contra Costa city with Bay views, a revitalized waterfront district, and BART access making it increasingly attractive to Bay Area buyers priced out elsewhere'},
            {'name': 'Walnut Creek', 'slug': 'walnut-creek', 'population': '70,000',  'median': '$900,000', 'zips': '94595, 94596, 94597, 94598', 'desc': 'an affluent East Bay city with upscale shopping, outstanding schools, and BART access — one of the most desirable addresses in Contra Costa County'},
        ],
        'faq': [
            ("Do you buy houses in all parts of Contra Costa County?",
             "Yes. We purchase homes throughout Contra Costa County — from the Delta communities of Antioch, Brentwood, and Pittsburg, to the central county cities of Concord and Martinez, to the affluent Lamorinda area (Lafayette, Moraga, Orinda) and West County cities like Richmond and El Cerrito."),
            ("My Contra Costa County home has significant deferred maintenance. Is that a problem?",
             "Not at all. We buy properties in any condition throughout the county — whether that means outdated systems, foundation issues, roof problems, unpermitted additions, or a full renovation backlog. You sell as-is and we handle everything after closing."),
            ("How fast can I sell my Contra Costa County house for cash?",
             "We can close in as few as 7 days after you accept your offer. The timeline from initial contact to cash in hand is typically 7-14 days, though you can choose any closing date that works for your schedule."),
            ("What types of Contra Costa County properties do you buy?",
             "We purchase single-family homes, condos, townhomes, duplexes, multi-unit residential properties, and even mobile homes on owned land throughout Contra Costa County. Occupied or vacant, any condition."),
        ],
    },
    {
        'name': 'Marin County',
        'slug': 'marin-county',
        'population': '255,000',
        'median': '$1,400,000',
        'seat': 'San Rafael',
        'lat': 37.99, 'lng': -122.53,
        'zips': '94901, 94903, 94941, 94947, 94949, 94960',
        'market_desc': 'Marin County sits just north of San Francisco across the Golden Gate Bridge, offering a rarefied combination of scenic beauty, top-ranked schools, biotech employment, and exceptional quality of life. With a median home price near $1.4 million, it is among the most expensive counties in the nation. The population skews affluent and aging, generating a consistent pipeline of estate sales, downsizing transactions, and discreet off-market sales.',
        'sell_reasons': 'estate sales from an aging population, divorce, off-market seller preference, retirement downsizing, and relocation to lower-cost states',
        'cities': [
            {'name': 'San Rafael', 'slug': 'san-rafael', 'population': '59,000', 'median': '$1,100,000', 'zips': '94901, 94903', 'desc': 'the county seat of Marin and its most populated city, with a vibrant downtown, diverse community, and proximity to Highway 101 and SMART train service'},
            {'name': 'Novato',     'slug': 'novato',     'population': '52,000', 'median': '$1,000,000', 'zips': '94945, 94947, 94949', 'desc': 'the northernmost and most affordable city in Marin County, popular with Bay Area families seeking more space while maintaining Marin\'s lifestyle and school quality'},
            {'name': 'Mill Valley', 'slug': 'mill-valley', 'population': '14,000', 'median': '$1,700,000', 'zips': '94941', 'desc': 'an iconic Marin enclave nestled at the base of Mount Tamalpais, celebrated for its redwood canyons, artistic community, and some of the highest home prices in the county'},
        ],
        'faq': [
            ("Do you purchase high-value Marin County estates?",
             "Yes. We evaluate and purchase Marin County properties at all price points, including luxury estates over $2 million. High-value properties may involve a slightly longer due diligence period, but we maintain our commitment to a fair, transparent cash offer and a closing timeline that suits the seller."),
            ("Can I sell my Marin County home off-market and discreetly?",
             "Absolutely. Many Marin County homeowners prefer to sell without public listings, open houses, or strangers walking through their homes. A direct cash sale to Redwood is entirely private — no MLS listing, no public record until the deed records at close."),
            ("My Marin County property has title complications from an estate. Can you help?",
             "We work with estate attorneys, probate courts, and title companies to navigate complex title situations routinely. Whether the property is in probate, has multiple heirs, or carries old liens, we have the experience and patience to work through it."),
            ("Is a cash sale in Marin County right for me even at these price points?",
             "It depends on your priorities. If speed, certainty, and privacy matter more than squeezing every dollar from an open-market sale, a cash offer makes sense even at Marin's premium price points. Our offer accounts for current comparable sales and provides clear documentation so you can make an informed decision."),
        ],
    },
    {
        'name': 'Solano County',
        'slug': 'solano-county',
        'population': '455,000',
        'median': '$570,000',
        'seat': 'Fairfield',
        'lat': 38.26, 'lng': -122.05,
        'zips': '94533, 95687, 94591, 94534, 94590, 94585, 95688',
        'market_desc': 'Solano County offers Bay Area accessibility at a significant discount, positioned between Sacramento and the Bay with Interstate 80 as its spine. Travis Air Force Base is the county\'s largest employer, creating a steady market of military relocations and PCS sales. The county attracts first-time buyers and Bay Area migrants priced out of closer-in East Bay communities, keeping demand relatively stable.',
        'sell_reasons': 'military Permanent Change of Station orders from Travis AFB, foreclosures, job changes, and Bay Area relocation',
        'cities': [
            {'name': 'Fairfield', 'slug': 'fairfield', 'population': '124,000', 'median': '$560,000', 'zips': '94533, 94534', 'desc': 'the Solano County seat and home to Travis Air Force Base, with a growing commercial corridor and strong demand from military families and Bay Area commuters'},
            {'name': 'Vallejo',   'slug': 'vallejo',   'population': '122,000', 'median': '$480,000', 'zips': '94589, 94590, 94591', 'desc': 'a diverse waterfront city on San Pablo Bay with some of the most affordable home prices in the greater Bay Area and a ferry connection to San Francisco'},
            {'name': 'Vacaville', 'slug': 'vacaville', 'population': '105,000', 'median': '$565,000', 'zips': '95687, 95688', 'desc': 'a clean, family-oriented city midway between Sacramento and the Bay Area, popular with commuters from both directions and known for its outlet shopping and community events'},
        ],
        'faq': [
            ("Do you buy homes from military families on PCS orders from Travis AFB?",
             "Yes — this is one of our most common situations in Solano County. Military families receiving Permanent Change of Station orders need fast, certain closings with no complications. We can close in 7 days and work around any military-specific timing constraints."),
            ("Can you help if I'm facing foreclosure in Solano County?",
             "Yes. A quick cash sale is often the best way to avoid foreclosure in Solano County, protecting your credit score and letting you walk away with any remaining equity. Contact us as soon as possible — the more time we have, the more options are available."),
            ("What is the Solano County real estate market like right now?",
             "Solano County has a median home price around $570,000, making it one of the more affordable Bay Area-adjacent markets in Northern California. Demand from Bay Area migrants remains steady, though rising interest rates have slowed some buyer activity. Cash buyers remain very active."),
            ("Do you buy homes in Benicia, Dixon, or Rio Vista in Solano County?",
             "Yes. We purchase homes throughout all of Solano County, including smaller communities like Benicia, Dixon, Rio Vista, Suisun City, and the unincorporated areas between them."),
        ],
    },
    {
        'name': 'Placer County',
        'slug': 'placer-county',
        'population': '434,000',
        'median': '$685,000',
        'seat': 'Auburn',
        'lat': 39.06, 'lng': -120.73,
        'zips': '95747, 95648, 95678, 95765, 95661, 95603, 95677',
        'market_desc': 'Placer County is one of California\'s fastest-growing counties, anchored by the technology-driven economy of Roseville and Rocklin and the natural appeal of Lake Tahoe\'s western slopes. Hewlett-Packard\'s sprawling campus helped establish Roseville as a tech hub, and the county continues to attract affluent families seeking master-planned communities, excellent schools, and suburban lifestyle with mountain recreation nearby.',
        'sell_reasons': 'job changes, retirement downsizing, family changes, and homeowners seeking to trade up or move closer to Tahoe',
        'cities': [
            {'name': 'Roseville', 'slug': 'roseville', 'population': '170,000', 'median': '$630,000', 'zips': '95661, 95678, 95747', 'desc': 'Placer County\'s largest city and a major tech employment hub anchored by HP and a growing roster of technology companies, with master-planned neighborhoods and top-rated schools'},
            {'name': 'Rocklin',   'slug': 'rocklin',   'population': '73,000',  'median': '$650,000', 'zips': '95765, 95677',        'desc': 'a fast-growing Placer County city adjacent to Roseville with a strong community identity, excellent schools, and a diverse mix of newer single-family developments'},
            {'name': 'Lincoln',   'slug': 'lincoln',   'population': '55,000',  'median': '$610,000', 'zips': '95648',               'desc': 'one of the fastest-growing cities in California, popular for its large-lot developments, Del Webb\'s Sun City Lincoln Hills active adult community, and relative affordability within Placer County'},
            {'name': 'Auburn',    'slug': 'auburn',    'population': '14,000',  'median': '$590,000', 'zips': '95603',               'desc': 'the historic Placer County seat in the Sierra Nevada foothills, a gateway to Gold Country tourism and outdoor recreation with a charming old town district'},
        ],
        'faq': [
            ("Do you buy new-construction homes in Roseville or Rocklin?",
             "Yes, though newer construction is less common in our portfolio. We primarily purchase homes where the seller needs certainty and speed over maximizing sale price. If a newer home needs to sell quickly due to relocation, divorce, or financial circumstances, we can absolutely make an offer."),
            ("What is the Placer County housing market like compared to Sacramento?",
             "Placer County commands a premium over Sacramento County, with a median around $685,000. The county has seen strong appreciation driven by tech employment and Bay Area migration. Cash sales remain a strong option for sellers who need certainty, have properties with deferred maintenance, or want to avoid the listing process."),
            ("Can you buy my Placer County cabin or mountain property?",
             "Yes. We purchase mountain properties, cabins, and second homes in Placer County, including communities near Lake Tahoe. These properties often have unique valuation considerations, and we take the time to properly evaluate each one."),
            ("How do I sell my Placer County home if I've already relocated out of state?",
             "This is very common. We can manage the entire transaction remotely. We'll evaluate the property, communicate via phone/email/video, and arrange for mail-away or e-signed closing documents through a reputable local title company."),
        ],
    },
    {
        'name': 'El Dorado County',
        'slug': 'el-dorado-county',
        'population': '193,000',
        'median': '$710,000',
        'seat': 'Placerville',
        'lat': 38.73, 'lng': -120.80,
        'zips': '95667, 95762, 96150, 95682, 95619',
        'market_desc': 'El Dorado County stretches from the Sacramento Valley foothills to the shores of Lake Tahoe, encompassing everything from the Gold Rush charm of Placerville to the alpine resort community of South Lake Tahoe. The county\'s real estate market blends suburban communities like El Dorado Hills and Cameron Park with mountain resort properties, creating diverse selling scenarios from second-home liquidations to primary residence sales.',
        'sell_reasons': 'downsizing seniors, second-home owners selling after the Tahoe market peak, seasonal market timing, and property condition issues',
        'cities': [
            {'name': 'El Dorado Hills', 'slug': 'el-dorado-hills', 'population': '51,000', 'median': '$800,000',   'zips': '95762',        'desc': 'one of the most desirable communities in the greater Sacramento region — a planned community with top schools, upscale amenities, and Folsom Lake access that commands a significant premium'},
            {'name': 'South Lake Tahoe','slug': 'south-lake-tahoe','population': '21,000', 'median': '$700,000',   'zips': '96150',        'desc': 'California\'s iconic alpine resort city on the Nevada border, where tourism, short-term rentals, and seasonal residents create a unique and sometimes volatile real estate market'},
            {'name': 'Cameron Park',    'slug': 'cameron-park',    'population': '19,000', 'median': '$680,000',   'zips': '95682',        'desc': 'an unincorporated master-planned community between Sacramento and Placerville, popular with families for its quiet suburban feel, good schools, and convenient freeway access'},
            {'name': 'Placerville',     'slug': 'placerville',     'population': '11,000', 'median': '$550,000',   'zips': '95667',        'desc': 'the historic El Dorado County seat — \"Old Hangtown\" — a Gold Rush-era foothill community with a walkable historic downtown and a tight-knit local character'},
        ],
        'faq': [
            ("Do you buy vacation homes and second properties at Lake Tahoe?",
             "Yes. We purchase South Lake Tahoe vacation homes, cabins, condos, and lakefront properties. Many Tahoe second-home owners are selling after the post-pandemic price surge, and a cash sale offers a clean, certain exit without managing a complicated short-term rental property through a listing."),
            ("My El Dorado County home needs significant work after years of deferred maintenance — will you buy it?",
             "Absolutely. Deferred maintenance, aging systems, and cosmetic wear are all things we price into our offer. You don't need to invest a dollar in repairs before closing."),
            ("What is the real estate market like in El Dorado Hills versus South Lake Tahoe?",
             "El Dorado Hills has a strong, relatively stable suburban market with high demand from Sacramento-area buyers — median around $800,000. South Lake Tahoe fluctuates more with tourism trends and short-term rental regulations, with a current median around $700,000 after softening from 2022 highs."),
            ("Can you close quickly on an El Dorado County home with title complications?",
             "Yes. We work with experienced local title companies and attorneys who are familiar with El Dorado County's property records, including older properties with complex histories. Title issues rarely prevent us from proceeding — they just require a bit more time."),
        ],
    },
    {
        'name': 'Nevada County',
        'slug': 'nevada-county',
        'population': '102,000',
        'median': '$600,000',
        'seat': 'Nevada City',
        'lat': 39.26, 'lng': -121.02,
        'zips': '95945, 95949, 96161, 95959, 95946',
        'market_desc': 'Nevada County occupies the Sierra Nevada foothills between Sacramento and Lake Tahoe, encompassing the Gold Rush towns of Nevada City and Grass Valley and the mountain community of Truckee. The county has a high senior population, a thriving arts scene, and a growing community of remote workers drawn to its natural beauty. The combination of older housing stock and an aging homeowner base creates steady demand for as-is sales.',
        'sell_reasons': 'aging population selling family homes, property condition issues from deferred maintenance, high interest rates affecting buyer pool, and remote workers returning to cities',
        'cities': [
            {'name': 'Truckee',      'slug': 'truckee',      'population': '17,000', 'median': '$900,000', 'zips': '96161', 'desc': 'a mountain resort town near Lake Tahoe\'s north shore, renowned for world-class skiing at Northstar, Squaw Valley, and Sugar Bowl, and increasingly popular with year-round remote workers and outdoor enthusiasts'},
            {'name': 'Grass Valley', 'slug': 'grass-valley', 'population': '14,000', 'median': '$560,000', 'zips': '95945, 95949', 'desc': 'the largest city in Nevada County, a vibrant Gold Rush town with a growing arts and culture scene, a mix of historic Victorian homes and newer developments, and a strong sense of community identity'},
            {'name': 'Nevada City',  'slug': 'nevada-city',  'population': '3,000',  'median': '$650,000', 'zips': '95959', 'desc': 'the county seat and one of California\'s best-preserved Gold Rush towns, a walkable historic community beloved for its Victorian architecture, independent shops, and dedicated arts community'},
        ],
        'faq': [
            ("Do you buy older Gold Rush-era homes in Nevada City or Grass Valley?",
             "Yes. We purchase historic and older properties throughout Nevada County, including Victorian-era homes, miner\'s cabins, and properties with aging infrastructure. We price the condition into our offer — you never need to renovate or restore before selling."),
            ("My Nevada County home has a septic system and well — is that a problem?",
             "Not at all. Many Nevada County rural properties have septic and well systems, and we buy them regularly. We may request basic inspection reports on these systems, but they don't prevent a cash sale."),
            ("Do you buy Truckee mountain homes and ski chalets?",
             "Yes. We purchase Truckee properties across all price points, including ski-season chalets, mountain cabins, and luxury resort properties. Many owners are selling after strong appreciation in 2020-2022 and want a clean exit."),
            ("What is the Nevada County real estate market like for sellers?",
             "With a median around $600,000 and a predominantly older housing stock, Nevada County offers a solid seller's market for properties in good condition. However, homes needing significant work or with deferred maintenance can sit on the market for months — making a cash sale a far more predictable option."),
        ],
    },
    {
        'name': 'Mendocino County',
        'slug': 'mendocino-county',
        'population': '89,000',
        'median': '$495,000',
        'seat': 'Ukiah',
        'lat': 39.15, 'lng': -123.21,
        'zips': '95482, 95437, 95490, 95470',
        'market_desc': 'Mendocino County stretches from the rugged Pacific coast to the inland valleys of the Emerald Triangle, known for its cannabis production, wine tourism, and aging rural housing stock. The county\'s combination of economic challenges, a shrinking tax base, and an increasing number of properties in poor condition creates strong demand for as-is cash buyers willing to move quickly in a rural, sometimes remote market.',
        'sell_reasons': 'economic distress, job losses, aging housing stock requiring expensive repairs, fire and climate risk, and absentee owners inheriting rural properties',
        'cities': [
            {'name': 'Ukiah',      'slug': 'ukiah',      'population': '16,600', 'median': '$400,000', 'zips': '95482', 'desc': 'the Mendocino County seat and largest city, an inland valley community at the heart of the wine and cannabis industries — more affordable than the coast but facing economic headwinds'},
            {'name': 'Fort Bragg', 'slug': 'fort-bragg', 'population': '7,000',  'median': '$550,000', 'zips': '95437', 'desc': 'a rugged coastal city on the Mendocino Coast, popular with climate migrants seeking cooler temperatures, home to a mix of fishing heritage and a growing arts and tourism economy'},
            {'name': 'Willits',    'slug': 'willits',    'population': '4,900',  'median': '$370,000', 'zips': '95490', 'desc': 'a small inland Mendocino County city at the crossroads of Highway 101 and Highway 20, with some of the county\'s most affordable housing and a community of rural homesteaders'},
        ],
        'faq': [
            ("Do you buy properties in rural or remote areas of Mendocino County?",
             "Yes. We purchase properties throughout Mendocino County, including rural parcels, off-grid cabins, and properties with limited road access. Remote locations may require additional time for our team to visit and evaluate, but we serve the entire county."),
            ("My Mendocino County home has significant deferred maintenance and code issues — can you still buy it?",
             "Absolutely. This is one of the most common situations we encounter in Mendocino County. Older homes with unpermitted additions, failing systems, or code violations are exactly what we specialize in. No repairs, no permits required from you."),
            ("Is Mendocino County real estate a good market to sell in right now?",
             "The Mendocino County market is soft compared to coastal Bay Area or Sacramento markets, and many listings sit for extended periods — especially properties that need work. A cash sale provides certainty and a defined timeline that the open market simply can't offer in this county."),
            ("Can you buy my Mendocino County property during probate?",
             "Yes. We regularly purchase properties during active probate in Mendocino County. We work with the appointed personal representative and local title companies to ensure the transaction meets court requirements and closes properly."),
        ],
    },
]

MT_COUNTIES = [
    {
        'name': 'Flathead County',
        'slug': 'flathead-county',
        'population': '116,000',
        'median': '$697,000',
        'seat': 'Kalispell',
        'lat': 48.29, 'lng': -114.02,
        'zips': '59901, 59912, 59937, 59911',
        'market_desc': 'Flathead County is Montana\'s premier destination county, encompassing Glacier National Park, the pristine waters of Flathead Lake, and the charming city of Kalispell. A surge of out-of-state buyers during and after the pandemic pushed median home prices near $700,000 — extraordinary for rural Montana. The market has moderated somewhat as the pace of migration slowed, creating opportunity for sellers who purchased before the surge.',
        'sell_reasons': 'market cooling after pandemic surge, aging population cashing out equity, Canadian border-area sellers, and short-term rental operators exiting the market',
        'cities': [
            {'name': 'Kalispell',      'slug': 'kalispell',      'population': '34,000', 'median': '$600,000', 'zips': '59901', 'desc': 'the Flathead County seat and regional commercial hub, a rapidly growing Montana city that serves as the gateway to Glacier National Park and offers amenities far exceeding its size'},
            {'name': 'Whitefish',      'slug': 'whitefish',      'population': '10,000', 'median': '$900,000', 'zips': '59937', 'desc': 'Montana\'s premier ski resort town, home to Whitefish Mountain Resort and a luxury real estate market driven by wealthy out-of-state buyers seeking a scenic mountain lifestyle'},
            {'name': 'Columbia Falls', 'slug': 'columbia-falls', 'population': '6,000',  'median': '$550,000', 'zips': '59912', 'desc': 'a working-class gateway community east of Kalispell, increasingly popular as a more affordable alternative to Whitefish and Kalispell while still offering Glacier access'},
        ],
        'faq': [
            ("Has the Flathead County real estate market cooled from its pandemic peak?",
             "Yes. After extraordinary price appreciation in 2020-2022, Flathead County has seen some market moderation. Homes are taking longer to sell and prices have softened from peak levels, particularly for properties above $800,000. Cash sales remain a strong option for sellers who want certainty over waiting for the right buyer."),
            ("Do you buy Whitefish luxury homes and ski properties?",
             "Yes. We evaluate and purchase Flathead County properties at all price points, including Whitefish Mountain Resort-adjacent properties, lakefront homes on Flathead Lake, and rural ranch parcels. Higher-value properties may require a longer evaluation period."),
            ("Can you buy my Flathead County home if I'm relocating out of Montana?",
             "Absolutely. We work with relocating sellers regularly and can manage the transaction remotely. We'll coordinate with a local Montana title company and close via mail-away or e-signing if needed."),
            ("Do you purchase short-term rental properties in Flathead County?",
             "Yes. Many Flathead County short-term rental owners are choosing to exit as the regulatory environment tightens and occupancy rates normalize. A cash sale is an efficient way to convert a rental property to liquid capital without a lengthy listing process."),
        ],
    },
    {
        'name': 'Missoula County',
        'slug': 'missoula-county',
        'population': '123,000',
        'median': '$550,000',
        'seat': 'Missoula',
        'lat': 46.87, 'lng': -114.01,
        'zips': '59801, 59802, 59803, 59804, 59808, 59847',
        'market_desc': 'Missoula County is Montana\'s most educated and progressive county, anchored by the University of Montana and a diverse economy encompassing education, healthcare, and a growing tech sector. The city of Missoula consistently ranks among the most desirable small cities in the West, attracting outdoor enthusiasts, remote workers, and academics. Housing supply is chronically tight at entry and mid-level price points, supporting strong values even as the market cools from its 2022 peak.',
        'sell_reasons': 'job relocations, family changes, market stabilization encouraging sellers to lock in gains, and rental property owners exiting a complicated landlord environment',
        'cities': [
            {'name': 'Missoula', 'slug': 'missoula', 'population': '80,000', 'median': '$520,000', 'zips': '59801, 59802, 59803, 59804, 59808', 'desc': 'the cultural and economic heart of western Montana, a vibrant university city nestled in five river valleys with world-class fly fishing, hiking, and a nationally recognized arts scene'},
            {'name': 'Lolo',     'slug': 'lolo',     'population': '6,000',  'median': '$480,000', 'zips': '59847', 'desc': 'a growing community just south of Missoula along the Bitterroot Valley, popular with families seeking more space at lower prices while maintaining easy access to Missoula\'s amenities'},
        ],
        'faq': [
            ("Why should I sell my Missoula County home for cash instead of listing it?",
             "Missoula's listing market is competitive but can be unpredictable, especially for properties outside peak price ranges or those needing work. A cash sale provides guaranteed closing, your chosen timeline, zero commissions, and no repair requirements — certainty that the listing market simply can't match."),
            ("Do you purchase rental properties near the University of Montana?",
             "Yes. Student rental properties near the U of M campus are a common purchase for us. Many landlords are choosing to exit after years of managing student rentals, and we can provide a fast, clean exit without the need to stage, clean, or upgrade the property."),
            ("What is the Missoula real estate market like right now?",
             "Missoula's median home price is around $520,000, elevated significantly from pre-pandemic levels. The market has stabilized after 2022's peak, with homes taking somewhat longer to sell. Inventory remains below historical norms, supporting values, but buyers are more selective than during the pandemic surge."),
            ("Can you purchase land or acreage in Missoula County?",
             "Yes. We evaluate vacant land, rural acreage, and mixed-use properties throughout Missoula County, in addition to residential homes. Land purchases may take slightly longer to evaluate but we do consider them."),
        ],
    },
    {
        'name': 'Yellowstone County',
        'slug': 'yellowstone-county',
        'population': '172,000',
        'median': '$390,000',
        'seat': 'Billings',
        'lat': 45.79, 'lng': -108.50,
        'zips': '59102, 59101, 59105, 59106, 59044',
        'market_desc': 'Yellowstone County is Montana\'s most populous county and its economic powerhouse, centered on Billings — the largest city in Montana and a regional hub for healthcare, energy, agriculture, and retail. Unlike the resort-driven markets of Flathead or the university-driven Missoula, Yellowstone County\'s real estate market is driven by practical economic fundamentals, making it more affordable and more stable than other Montana markets.',
        'sell_reasons': 'job relocations for the energy and healthcare sectors, divorce, inherited properties, and homeowners dealing with deferred maintenance on older housing stock',
        'cities': [
            {'name': 'Billings', 'slug': 'billings', 'population': '119,000', 'median': '$375,000', 'zips': '59102, 59101, 59105, 59106', 'desc': 'Montana\'s largest city and the regional economic capital of the Northern Rockies — a practical, growing city anchored by healthcare, energy, and agricultural industries with an affordable and stable real estate market'},
            {'name': 'Laurel',   'slug': 'laurel',   'population': '7,000',   'median': '$310,000', 'zips': '59044', 'desc': 'a small industrial and agricultural community southwest of Billings, offering some of Yellowstone County\'s most affordable housing for working families in the energy and logistics sectors'},
        ],
        'faq': [
            ("Is Billings a good market to sell a home quickly?",
             "Billings has a practical, demand-driven market that supports reasonable listing timelines for move-in-ready homes. However, properties needing repairs, older homes, or those with specific timing constraints (job relocation, divorce, inheritance) often sell faster and with less hassle through a cash buyer."),
            ("Do you buy homes in all Billings neighborhoods?",
             "Yes. We purchase homes in all Billings neighborhoods, from the Heights and the West End to Broadwater and Lockwood. Property location and condition affect the offer price, but we don't exclude any areas."),
            ("What types of Yellowstone County properties do you buy?",
             "We purchase single-family homes, duplexes, small apartment buildings, mobile homes on owned land, and commercial-residential mixed properties throughout Yellowstone County. We also consider rural properties and acreage in unincorporated county areas."),
            ("Can you close quickly on a Yellowstone County home during a job relocation?",
             "Absolutely. Job relocations in the energy and healthcare sectors are extremely common in Billings. We can close in 7 days or match your relocation start date. Many sellers appreciate knowing their home is sold before they start a new position."),
        ],
    },
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SHARED TEMPLATE COMPONENTS (copied from build.py, updated for multi-state)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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
    if '/' in from_page and '/' in to_page:
        # Both in a subdirectory — assume same level for now
        from_dir = from_page.rsplit('/', 1)[0]
        to_dir   = to_page.rsplit('/', 1)[0]
        if from_dir == to_dir:
            return to_page.split('/')[-1]
        return '../' + to_page
    return to_page

def make_head(page_file, title, description, canonical_path='', schema_blocks=None,
              extra_head='', geo_region='US-CA', geo_placename='Sacramento'):
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
  <meta name="geo.region" content="{geo_region}">
  <meta name="geo.placename" content="{geo_placename}">
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
    home  = pp('index.html')
    offer = pp('index.html') + '#get-offer'

    nav_links    = ''
    mobile_links = ''
    for label, href, nav_id in NAV:
        active = ' class="is-active"' if nav_id == active_id else ''
        link = pp(href)
        nav_links    += f'          <li><a href="{link}"{active}>{label}</a></li>\n'
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
    for c in FOOTER_CITIES:
        city_links += f'          <li><a href="{pp(c["state"] + "/sell-my-house-fast-" + c["slug"] + ".html")}">{c["name"]}</a></li>\n'

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
      <p>We buy houses for cash in Sacramento, Elk Grove, Roseville, Kalispell, Missoula, Billings, and throughout Northern California and Montana.</p>
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

CHECKMARK = '<svg class="situation-item__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>'

def situation_item(label):
    return f'              <div class="situation-item">{CHECKMARK}<span>{label}</span></div>\n'

COMMON_SITUATIONS = [
    'Facing Foreclosure', 'Inherited Property', 'Divorce',
    'Behind on Payments', 'Job Relocation', 'Tired Landlord',
    'Major Repairs Needed', 'Code Violations',
]


# ── State Hub Pages ──────────────────────────────────────────

def build_state_hub(state_slug, state_name, state_abbr, counties, geo_region, intro_p1, intro_p2, trust_points):
    pf = f'{state_slug}/index.html'

    breadcrumb_schema = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN},
            {"@type": "ListItem", "position": 2, "name": state_name, "item": f"{DOMAIN}/{state_slug}/"},
        ]
    }
    local_biz = {
        "@context": "https://schema.org", "@type": "RealEstateAgent",
        "name": f"Redwood Real Estate Solutions — {state_name}",
        "url": f"{DOMAIN}/{state_slug}/",
        "areaServed": {"@type": "State", "name": state_name},
        "description": f"We buy houses for cash throughout {state_name}. No repairs, no commissions, close in as little as 7 days."
    }

    total_cities = sum(len(c['cities']) for c in counties)
    content = make_head(
        pf,
        f'We Buy Houses for Cash in {state_name} — Cash Home Buyers | Redwood Real Estate',
        f'Redwood Real Estate Solutions buys houses for cash throughout {state_name}. Serving {len(counties)} counties and {total_cities}+ cities. No repairs, no commissions, close in 7 days.',
        f'{state_slug}/', [breadcrumb_schema, local_biz],
        geo_region=geo_region, geo_placename=counties[0]['seat']
    )
    content += make_header(pf, 'areas')
    content += '  <main id="main">\n'
    content += make_breadcrumb(pf, [(state_name, '')])
    content += make_page_hero(
        f'Cash Home Buyers in {state_name}',
        f'We Buy Houses for Cash in {state_name}',
        f'Serving {len(counties)} counties across {state_name}. Get a fair cash offer within 24 hours — no repairs, no commissions, no hassle.'
    )

    # Intro section
    content += f'''    <section class="section">
      <div class="container container--narrow">
        <div class="section__header fade-in">
          <span class="section__overline">About Our {state_name} Operations</span>
          <h2 class="section__title">Redwood Real Estate in {state_name}</h2>
        </div>
        <div class="fade-in">
          <p>{intro_p1}</p>
          <p>{intro_p2}</p>
        </div>
      </div>
    </section>
'''

    # County grid
    content += f'''    <section class="section section--alt">
      <div class="container">
        <div class="section__header section__header--center fade-in">
          <span class="section__overline">Locations We Serve</span>
          <h2 class="section__title">{state_name} Counties We Buy In</h2>
          <p class="section__desc">Select your county to learn more about our services in your area.</p>
        </div>
        <div class="areas-grid">
'''
    for county in counties:
        num_cities = len(county['cities'])
        content += f'''          <a href="{county['slug']}.html" class="area-card fade-in">
            <h2 class="area-card__city">{county['name']}</h2>
            <p class="area-card__county">{county['seat']} &middot; {state_abbr}</p>
            <p class="area-card__stats">Pop: {county['population']} &middot; Median: {county['median']}</p>
            <span class="area-card__link">Serving {num_cities} cities in this county →</span>
          </a>
'''
    content += '        </div>\n      </div>\n    </section>\n'

    # Trust section
    content += f'''    <section class="section">
      <div class="container container--narrow">
        <div class="section__header section__header--center fade-in">
          <span class="section__overline">Why Redwood</span>
          <h2 class="section__title">Why {state_name} Homeowners Choose Us</h2>
        </div>
        <div class="fade-in">
          <div class="situations-list situations-list--compact">
'''
    for point in trust_points:
        content += f'            <div class="situation-item">{CHECKMARK}<span>{point}</span></div>\n'
    content += '''          </div>
        </div>
      </div>
    </section>
'''

    content += make_cta_section(pf, f'offer-form-{state_slug}-hub')
    content += '  </main>\n'
    content += make_footer(pf)
    write_page(pf, content)


# ── County Pages ─────────────────────────────────────────────

def build_county_page(state_slug, state_name, state_abbr, county):
    slug   = county['slug']
    name   = county['name']
    pf     = f'{state_slug}/{slug}.html'
    seat   = county['seat']
    lat    = county['lat']
    lng    = county['lng']

    geo_region = 'US-CA' if state_slug == 'california' else 'US-MT'

    breadcrumb_schema = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN},
            {"@type": "ListItem", "position": 2, "name": state_name, "item": f"{DOMAIN}/{state_slug}/"},
            {"@type": "ListItem", "position": 3, "name": name, "item": f"{DOMAIN}/{state_slug}/{slug}.html"},
        ]
    }
    local_biz = {
        "@context": "https://schema.org", "@type": "RealEstateAgent",
        "name": f"Redwood Real Estate Solutions — {name}",
        "url": f"{DOMAIN}/{state_slug}/{slug}.html",
        "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng},
        "address": {"@type": "PostalAddress", "addressLocality": seat, "addressRegion": state_abbr, "addressCountry": "US"},
        "areaServed": {"@type": "AdministrativeArea", "name": name},
        "description": f"We buy houses for cash in {name}, {state_abbr}. No repairs, no commissions, close in as little as 7 days."
    }
    faq_schema = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in county['faq']
        ]
    }

    content = make_head(
        pf,
        f'Sell My House Fast for Cash in {name}, {state_abbr} | Redwood Real Estate Solutions',
        f'We buy houses for cash in {name}, {state_abbr}. Population {county["population"]}, median home price {county["median"]}. No repairs, no commissions, close in 7 days. Get your free offer.',
        f'{state_slug}/{slug}.html', [breadcrumb_schema, local_biz, faq_schema],
        geo_region=geo_region, geo_placename=seat
    )
    content += make_header(pf, 'areas')
    content += '  <main id="main">\n'
    content += make_breadcrumb(pf, [(state_name, 'index.html'), (name, '')])
    content += make_page_hero(
        f'We Buy Houses in {name}',
        f'Sell Your House Fast for Cash in {name}, {state_abbr}',
        f'Fair cash offer within 24 hours. No repairs, no commissions, no hassle — close on your timeline.'
    )

    # County overview + cities grid
    content += f'''    <section class="section">
      <div class="container">
        <div class="city-content">
          <div class="city-content__main fade-in">
            <h2>Cash Home Buyers in {name}, {state_abbr}</h2>
            <p>{county['market_desc']}</p>
            <p>Whether you're dealing with {county['sell_reasons']}, Redwood Real Estate Solutions offers a straightforward alternative to the traditional listing process. We buy homes in any condition throughout {name} — no repairs, no staging, no open houses, no waiting.</p>
            <p>With a population of {county['population']} and a median home price of {county['median']}, {name} is a dynamic real estate market with unique local factors. We understand those factors deeply and use real local sales data to make fair, well-documented offers.</p>

            <h3>Why {name} Homeowners Choose Redwood</h3>
            <ul class="city-benefits">
              <li><strong>Cash Offer in 24 Hours:</strong> We present a fair, all-cash offer within 24 hours of receiving your property details.</li>
              <li><strong>Close on Your Schedule:</strong> Whether you need 7 days or 60 days, you pick the closing date.</li>
              <li><strong>No Repairs Required:</strong> We buy homes as-is throughout {name} — any condition, any situation.</li>
              <li><strong>Zero Fees or Commissions:</strong> No agent commissions, no closing costs charged to you, no hidden fees.</li>
              <li><strong>Local Market Knowledge:</strong> We know {name} neighborhoods, pricing, and the specific factors that affect property values here.</li>
            </ul>

            <h3>Common Situations We Help With in {name}</h3>
            <div class="situations-list situations-list--compact">
'''
    for sit in COMMON_SITUATIONS:
        content += situation_item(sit)
    content += f'''            </div>
          </div>
          <div class="city-content__sidebar fade-in">
            <div class="city-stats-card">
              <h3 class="city-stats-card__title">{name} at a Glance</h3>
              <div class="city-stat"><span class="city-stat__label">Population</span><span class="city-stat__value">{county['population']}</span></div>
              <div class="city-stat"><span class="city-stat__label">Median Home Price</span><span class="city-stat__value">{county['median']}</span></div>
              <div class="city-stat"><span class="city-stat__label">County Seat</span><span class="city-stat__value">{seat}</span></div>
              <div class="city-stat"><span class="city-stat__label">ZIP Codes</span><span class="city-stat__value">{county['zips']}</span></div>
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
'''

    # Cities grid
    content += f'''    <section class="section section--alt">
      <div class="container">
        <div class="section__header section__header--center fade-in">
          <span class="section__overline">Cities We Serve</span>
          <h2 class="section__title">Cities We Buy Houses In — {name}</h2>
          <p class="section__desc">Select your city for location-specific information about selling your home for cash.</p>
        </div>
        <div class="areas-grid">
'''
    for city in county['cities']:
        content += f'''          <a href="sell-my-house-fast-{city['slug']}.html" class="area-card fade-in">
            <h3 class="area-card__city">{city['name']}</h3>
            <p class="area-card__county">{name}</p>
            <p class="area-card__stats">Pop: {city['population']} &middot; Median: {city['median']}</p>
            <span class="area-card__link">Sell My House in {city['name']} →</span>
          </a>
'''
    content += '        </div>\n      </div>\n    </section>\n'

    # FAQ
    content += f'''    <section class="section">
      <div class="container container--narrow">
        <div class="section__header section__header--center fade-in">
          <h2 class="section__title">Frequently Asked Questions — {name}</h2>
        </div>
        <div class="faq-list">
'''
    for q, a in county['faq']:
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


# ── City Pages ───────────────────────────────────────────────

def build_city_page(state_slug, state_name, state_abbr, county, city):
    city_slug    = city['slug']
    city_name    = city['name']
    county_name  = county['name']
    county_slug  = county['slug']
    pf           = f'{state_slug}/sell-my-house-fast-{city_slug}.html'

    geo_region = 'US-CA' if state_slug == 'california' else 'US-MT'

    # City-specific FAQs
    faq_items = [
        (f"How fast can you buy my house in {city_name}, {state_abbr}?",
         f"We can close on your {city_name} home in as little as 7 days. Submit your property details today, receive a cash offer within 24 hours, and pick any closing date that fits your schedule."),
        (f"Do you buy houses in any condition in {city_name}?",
         f"Yes. We purchase homes throughout {city_name} regardless of condition — whether your property needs major structural repairs, has fire or water damage, code violations, unpermitted additions, or simply hasn't been updated in decades. Sell as-is."),
        (f"Are there really no fees when selling my {city_name} home to Redwood?",
         f"Correct — zero fees, zero commissions, zero closing costs charged to you. The figure in your cash offer is the full amount you receive at the closing table. We cover all transaction costs on our end."),
        (f"What if I'm facing foreclosure on my {city_name} property?",
         f"Contact us immediately. Selling your {city_name} home for cash can stop the foreclosure process before it completes, protect your credit score, and let you walk away with any remaining equity. The sooner you reach out, the more options you have."),
    ]

    breadcrumb_schema = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN},
            {"@type": "ListItem", "position": 2, "name": state_name, "item": f"{DOMAIN}/{state_slug}/"},
            {"@type": "ListItem", "position": 3, "name": county_name, "item": f"{DOMAIN}/{state_slug}/{county_slug}.html"},
            {"@type": "ListItem", "position": 4, "name": city_name, "item": f"{DOMAIN}/{state_slug}/sell-my-house-fast-{city_slug}.html"},
        ]
    }
    local_biz = {
        "@context": "https://schema.org", "@type": "RealEstateAgent",
        "name": f"Redwood Real Estate Solutions — {city_name}",
        "url": f"{DOMAIN}/{state_slug}/sell-my-house-fast-{city_slug}.html",
        "geo": {"@type": "GeoCoordinates", "latitude": county['lat'], "longitude": county['lng']},
        "address": {"@type": "PostalAddress", "addressLocality": city_name, "addressRegion": state_abbr, "addressCountry": "US"},
        "areaServed": {"@type": "City", "name": city_name},
        "description": f"We buy houses for cash in {city_name}, {state_abbr}. No repairs, no commissions, close in as little as 7 days."
    }
    faq_schema = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq_items
        ]
    }

    content = make_head(
        pf,
        f'Sell My House Fast in {city_name}, {state_abbr} — Cash Offer in 24 Hours | Redwood Real Estate',
        f'Need to sell your house fast in {city_name}, {state_abbr}? Redwood Real Estate Solutions buys homes for cash in any condition. No repairs, no commissions, close in 7 days. Get your free offer.',
        f'{state_slug}/sell-my-house-fast-{city_slug}.html', [breadcrumb_schema, local_biz, faq_schema],
        geo_region=geo_region, geo_placename=city_name
    )
    content += make_header(pf, 'areas')
    content += '  <main id="main">\n'
    content += make_breadcrumb(pf, [
        (state_name,   'index.html'),
        (county_name,  f'{county_slug}.html'),
        (city_name,    ''),
    ])
    content += make_page_hero(
        f'We Buy Houses in {city_name}',
        f'Sell My House Fast in {city_name}, {state_abbr}',
        f'Get a fair, no-obligation cash offer on your {city_name} home within 24 hours. No repairs, no commissions, no hassle.'
    )

    content += f'''    <section class="section">
      <div class="container">
        <div class="city-content">
          <div class="city-content__main fade-in">
            <h2>Cash Home Buyers in {city_name}, {state_abbr}</h2>
            <p>If you need to sell your house fast in {city_name}, Redwood Real Estate Solutions is here to help. We're local cash home buyers serving {city['desc']}. Whether you're facing foreclosure, going through a divorce, dealing with an inherited property, or simply need to sell quickly and without hassle — we buy houses in any condition and close on your timeline.</p>
            <p>Unlike listing with a real estate agent — which typically takes 3–6 months, costs 5–6% in commissions, and requires expensive repairs and showings — selling to Redwood means you get a cash offer within 24 hours, pay zero fees, make zero repairs, and close in as few as 7 days.</p>

            <h3>Why {city_name} Homeowners Choose Redwood</h3>
            <ul class="city-benefits">
              <li><strong>Fast Cash Offers:</strong> We present a fair, all-cash offer within 24 hours of learning about your property.</li>
              <li><strong>Close on Your Schedule:</strong> Whether you need 7 days or 60 days, you pick the closing date.</li>
              <li><strong>No Repairs Required:</strong> Foundation issues, roof damage, mold, code violations — we buy homes as-is.</li>
              <li><strong>Zero Fees:</strong> No agent commissions, no closing costs, no hidden charges — ever.</li>
              <li><strong>Local Expertise:</strong> We know the {city_name} market, including ZIP codes {city['zips']} and the unique factors that affect your home's value.</li>
            </ul>

            <h3>About the {city_name} Housing Market</h3>
            <p>With a population of approximately {city['population']} and a median home price of {city['median']}, {city_name} is {city['desc']}. The local real estate market reflects broader trends in {county_name} while maintaining its own neighborhood dynamics and buyer profile.</p>
            <p>Many {city_name} homeowners come to us after discovering that the traditional selling process doesn't fit their situation. Between agent commissions (typically 5–6% of the sale price), repair costs ($5,000–$30,000+), and months of carrying costs while waiting for the right buyer, the traditional route can cost far more than most people realize. Our cash offer eliminates all of that uncertainty.</p>

            <h3>Situations We Help {city_name} Homeowners With</h3>
            <div class="situations-list situations-list--compact">
'''
    for sit in COMMON_SITUATIONS:
        content += situation_item(sit)
    content += f'''            </div>
          </div>
          <div class="city-content__sidebar fade-in">
            <div class="city-stats-card">
              <h3 class="city-stats-card__title">{city_name} at a Glance</h3>
              <div class="city-stat"><span class="city-stat__label">Population</span><span class="city-stat__value">{city['population']}</span></div>
              <div class="city-stat"><span class="city-stat__label">Median Home Price</span><span class="city-stat__value">{city['median']}</span></div>
              <div class="city-stat"><span class="city-stat__label">County</span><span class="city-stat__value">{county_name}</span></div>
              <div class="city-stat"><span class="city-stat__label">ZIP Codes</span><span class="city-stat__value">{city['zips']}</span></div>
            </div>
            <div class="city-process-card">
              <h3>How It Works</h3>
              <div class="mini-step"><span class="mini-step__num">1</span><span>Tell us about your {city_name} property</span></div>
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
          <h2 class="section__title">Common Questions About Selling in {city_name}</h2>
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

    content += make_cta_section(pf, f'offer-form-{city_slug}')
    content += '  </main>\n'
    content += make_footer(pf)
    write_page(pf, content)


# ── Areas We Serve (master rebuild) ─────────────────────────

def build_areas_we_serve():
    pf = 'areas-we-serve.html'
    breadcrumb_schema = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN},
            {"@type": "ListItem", "position": 2, "name": "Areas We Serve", "item": f"{DOMAIN}/areas-we-serve.html"},
        ]
    }
    total_ca = sum(len(c['cities']) for c in CA_COUNTIES)
    total_mt = sum(len(c['cities']) for c in MT_COUNTIES)

    content = make_head(
        pf,
        'Areas We Serve — Cash Home Buyers in California & Montana | Redwood Real Estate',
        f'Redwood Real Estate Solutions buys houses for cash in {len(CA_COUNTIES)} California counties and {len(MT_COUNTIES)} Montana counties. {total_ca + total_mt}+ cities served. No repairs, no commissions.',
        'areas-we-serve.html', [breadcrumb_schema]
    )
    content += make_header(pf, 'areas')
    content += '  <main id="main">\n'
    content += make_breadcrumb(pf, [('Areas We Serve', '')])
    content += make_page_hero(
        'Areas We Serve',
        'Cash Home Buyers in California & Montana',
        f'We buy houses throughout {len(CA_COUNTIES)} California counties and {len(MT_COUNTIES)} Montana counties. Select your state and county below.'
    )

    # California section
    content += f'''    <section class="section">
      <div class="container">
        <div class="section__header fade-in">
          <span class="section__overline">California</span>
          <h2 class="section__title">We Buy Houses Throughout Northern California</h2>
          <p class="section__desc">Serving {len(CA_COUNTIES)} counties and {total_ca}+ cities across Northern California. <a href="california/">View California hub →</a></p>
        </div>
        <div class="areas-grid">
'''
    for county in CA_COUNTIES:
        num_cities = len(county['cities'])
        content += f'''          <a href="california/{county['slug']}.html" class="area-card fade-in">
            <h3 class="area-card__city">{county['name']}</h3>
            <p class="area-card__county">{county['seat']}, CA</p>
            <p class="area-card__stats">Median: {county['median']} &middot; {num_cities} cities</p>
            <span class="area-card__link">View {county['name']} →</span>
          </a>
'''
    content += '        </div>\n      </div>\n    </section>\n'

    # Montana section
    content += f'''    <section class="section section--alt">
      <div class="container">
        <div class="section__header fade-in">
          <span class="section__overline">Montana</span>
          <h2 class="section__title">We Buy Houses Throughout Montana</h2>
          <p class="section__desc">Serving {len(MT_COUNTIES)} counties and {total_mt}+ cities across Montana. <a href="montana/">View Montana hub →</a></p>
        </div>
        <div class="areas-grid">
'''
    for county in MT_COUNTIES:
        num_cities = len(county['cities'])
        content += f'''          <a href="montana/{county['slug']}.html" class="area-card fade-in">
            <h3 class="area-card__city">{county['name']}</h3>
            <p class="area-card__county">{county['seat']}, MT</p>
            <p class="area-card__stats">Median: {county['median']} &middot; {num_cities} cities</p>
            <span class="area-card__link">View {county['name']} →</span>
          </a>
'''
    content += '        </div>\n      </div>\n    </section>\n'

    content += make_cta_section(pf, 'offer-form-areas')
    content += '  </main>\n'
    content += make_footer(pf)
    write_page(pf, content)


# ── Sitemap ──────────────────────────────────────────────────

def build_sitemap():
    today = datetime.now().strftime('%Y-%m-%d')
    pages = [
        ('',                     '1.0', 'weekly'),
        ('how-it-works.html',    '0.9', 'monthly'),
        ('about.html',           '0.8', 'monthly'),
        ('reviews.html',         '0.8', 'monthly'),
        ('faq.html',             '0.8', 'monthly'),
        ('areas-we-serve.html',  '0.9', 'weekly'),
        ('blog.html',            '0.8', 'weekly'),
        ('california/',          '0.9', 'weekly'),
        ('montana/',             '0.9', 'weekly'),
    ]
    blog_slugs = [
        'sell-house-fast-sacramento', 'avoid-foreclosure-sacramento',
        'inherited-house-california', 'sacramento-market-2026',
        'cash-buyers-vs-agents', 'sell-house-code-violations',
    ]
    for s in blog_slugs:
        pages.append((f'blog-{s}.html', '0.7', 'monthly'))

    for county in CA_COUNTIES:
        pages.append((f'california/{county["slug"]}.html', '0.8', 'weekly'))
        for city in county['cities']:
            pages.append((f'california/sell-my-house-fast-{city["slug"]}.html', '0.8', 'monthly'))

    for county in MT_COUNTIES:
        pages.append((f'montana/{county["slug"]}.html', '0.8', 'weekly'))
        for city in county['cities']:
            pages.append((f'montana/sell-my-house-fast-{city["slug"]}.html', '0.8', 'monthly'))

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for path, priority, freq in pages:
        url = DOMAIN + '/' + path if path else DOMAIN + '/'
        xml += f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{priority}</priority>\n  </url>\n'
    xml += '</urlset>\n'
    write_page('sitemap.xml', xml)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN BUILD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    print('Building Redwood Real Estate Solutions — Multi-Location SEO Architecture')
    print('=' * 70)

    # ── Areas We Serve (master rebuild) ──
    print('\n[areas-we-serve]')
    build_areas_we_serve()

    # ── California State Hub ──
    print('\n[california state hub]')
    build_state_hub(
        state_slug='california',
        state_name='California',
        state_abbr='CA',
        counties=CA_COUNTIES,
        geo_region='US-CA',
        intro_p1=(
            'Redwood Real Estate Solutions has deep roots in Northern California. '
            'We started our business serving Sacramento County homeowners and have grown to cover '
            'ten counties across the region — from the Bay Area-adjacent markets of Marin, Contra Costa, '
            'and Solano counties, through Napa and Sonoma wine country, to the Sierra Nevada foothills '
            'of Placer, El Dorado, and Nevada counties, and north to the rural communities of Mendocino County.'
        ),
        intro_p2=(
            'Our mission in California is simple: provide homeowners with a fast, fair, transparent alternative '
            'to the traditional listing process. Whether your property is a luxury Marin County estate, a '
            'Sacramento suburb home with deferred maintenance, a wildfire-damaged Sonoma County property, or '
            'a rural Mendocino parcel — we evaluate and purchase all types of residential property throughout '
            'Northern California. No repairs, no commissions, no hassle.'
        ),
        trust_points=[
            'Cash offers delivered within 24 hours of contact',
            'Close in as few as 7 days — or on your schedule',
            'Zero commissions, zero closing costs, zero hidden fees',
            'Buy homes in any condition — no repairs required',
            'Experienced with probate, foreclosure, divorce, and inherited properties',
            'Transparent offer process with full documentation',
            'Local market expertise across 10 Northern California counties',
            'BBB-accredited and 5-star rated on Google',
        ]
    )

    # ── California Counties + Cities ──
    print('\n[california counties]')
    for county in CA_COUNTIES:
        build_county_page('california', 'California', 'CA', county)
        for city in county['cities']:
            build_city_page('california', 'California', 'CA', county, city)

    # ── Montana State Hub ──
    print('\n[montana state hub]')
    build_state_hub(
        state_slug='montana',
        state_name='Montana',
        state_abbr='MT',
        counties=MT_COUNTIES,
        geo_region='US-MT',
        intro_p1=(
            'Redwood Real Estate Solutions expanded to Montana to serve a market that saw extraordinary '
            'demand from out-of-state buyers during and after the pandemic. As markets in Flathead, '
            'Missoula, and Yellowstone counties have evolved, a growing number of Montana homeowners '
            'need a fast, certain path to selling — whether they\'re locking in gains from recent '
            'appreciation, dealing with a life change, or simply ready to move on.'
        ),
        intro_p2=(
            'We bring the same cash-buying model to Montana that has helped hundreds of California homeowners: '
            'a fair offer within 24 hours, closing on your schedule, and zero fees or commissions. '
            'We understand that Montana\'s markets — from the resort-driven Flathead Valley to the '
            'university town of Missoula to the practical economy of Billings — each have unique '
            'characteristics, and we price our offers using real, local comparable sales data.'
        ),
        trust_points=[
            'Cash offers within 24 hours across all Montana markets',
            'Close in 7 days or on any timeline you choose',
            'Zero commissions, zero closing costs, zero surprises',
            'Buy as-is — no repairs, cleaning, or staging required',
            'Experienced with mountain, rural, and resort property transactions',
            'Remote closing available for out-of-state sellers',
            'Handles PCS military relocations with fast, flexible timelines',
            'Transparent offer formula — we explain every number',
        ]
    )

    # ── Montana Counties + Cities ──
    print('\n[montana counties]')
    for county in MT_COUNTIES:
        build_county_page('montana', 'Montana', 'MT', county)
        for city in county['cities']:
            build_city_page('montana', 'Montana', 'MT', county, city)

    # ── Sitemap ──
    print('\n[sitemap]')
    build_sitemap()

    print('\n' + '=' * 70)
    print('Build complete! All multi-location pages generated.')


if __name__ == '__main__':
    main()
