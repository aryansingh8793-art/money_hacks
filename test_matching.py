from backend.matching import extract_size, group_listings
from backend.scrapers.base import Listing


def L(store, title, price=100):
    return Listing(store, title, price, "https://x")


def test_extract_size():
    assert extract_size("Serum 30ml") == (30.0, "ml")
    assert extract_size("Cream 1 kg") == (1000.0, "g")
    assert extract_size("Lipstick") is None


def test_same_product_grouped():
    g = group_listings([L("A", "Maybelline Fit Me Foundation 128 30ml"),
                        L("B", "Maybelline Fit Me Matte Foundation 128 (30 ml) - Pack of 1")])
    assert len(g) == 1


def test_different_shade_or_size_split():
    assert len(group_listings([L("A", "Fit Me Foundation 128 30ml"),
                               L("B", "Fit Me Foundation 220 30ml")])) == 2
    assert len(group_listings([L("A", "Hydro Boost Gel 50g"),
                               L("B", "Hydro Boost Gel 100g")])) == 2
