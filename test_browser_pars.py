"""Parser tests on small HTML samples shaped like each store's result cards.
Real pages are larger and change often: if a store returns nothing, open debug/<store>.html."""
from backend.scrapers.browser_store import parse_listings

AMAZON = """<div data-component-type="s-search-result"><a href="/dp/B0ABCDEFGH?ref=x"><img></a>
<h2><a href="/dp/B0ABCDEFGH?ref=x"><span>Maybelline Fit Me Matte Foundation 128 30ml</span></a></h2>
<span class="a-price"><span>₹549</span></span><span>M.R.P: ₹599</span></div>
<div data-component-type="s-search-result"><h2><a href="/dp/B0ZZZZZZZZ"><span>Lakme Absolute Lipstick 3.6g</span></a></h2><span>₹650</span></div>"""

FLIPKART = """<div><a href="/maybelline-fit-me/p/itm123?pid=1" title="Maybelline Fit Me Foundation 128 30 ml">
<img></a><div>Maybelline Fit Me Foundation 128 30 ml</div><div>₹520</div><div>₹599</div></div>"""

NYKAA = """<div class="card"><a href="/maybelline-fit-me/p/9876"><div>Maybelline New York Fit Me Matte Poreless Foundation 128 30ml</div></a>
<span>₹599</span><span>14% off</span></div>"""

PURPLLE = """<li><a href="/product/maybelline-fit-me-foundation-128"><p>Maybelline Fit Me Foundation 128 (30ml)</p></a><b>₹579</b></li>"""


def test_amazon_two_products_separated():
    r = parse_listings(AMAZON, "Amazon India", "https://www.amazon.in", r"/dp/[A-Z0-9]{10}")
    assert [(x.price, x.title[:9]) for x in r] == [(549.0, "Maybellin"), (650.0, "Lakme Abs")]


def test_flipkart_nykaa_purplle():
    assert parse_listings(FLIPKART, "Flipkart", "https://www.flipkart.com", r"/p/itm")[0].price == 520.0
    assert parse_listings(NYKAA, "Nykaa", "https://www.nykaa.com", r"/p/\d+")[0].price == 599.0
    assert parse_listings(PURPLLE, "Purplle", "https://www.purplle.com", r"/product/")[0].price == 579.0
