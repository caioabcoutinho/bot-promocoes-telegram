from src.stores import identify_store


STORES = [
    ("KaBuM!", ["kabum"], ["kabum.com.br"], False),
    ("Shopee", ["shopee"], ["shopee.com.br"], True),
]


def test_url_domain_has_priority_over_message_text():
    assert identify_store("Oferta na Amazon", "https://www.kabum.com.br/item", STORES) == (
        "KaBuM!",
        False,
    )


def test_unknown_store_is_allowed():
    assert identify_store("Oferta imperdível", "https://example.com/item", STORES) == (
        "Desconhecida",
        False,
    )


def test_blocked_store_is_reported():
    assert identify_store("Oferta Shopee", "https://shopee.com.br/item", STORES) == (
        "Shopee",
        True,
    )
