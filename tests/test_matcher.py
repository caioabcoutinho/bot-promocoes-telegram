from src.matcher import find_matching_products


PRODUCTS = [
    {
        "id": 1,
        "name": "Ryzen 7 9800X3D",
        "keywords": ["ryzen 7 9800x3d", "9800x3d"],
        "exclude_words": ["usado"],
    },
    {
        "id": 2,
        "name": "RTX 4070",
        "keywords": ["rtx 4070"],
        "exclude_words": [],
    },
]


def test_matching_is_case_and_accent_insensitive_and_returns_all_products():
    assert find_matching_products("RTX 4070 e RYZEN 7 9800X3D", PRODUCTS) == [
        (1, "Ryzen 7 9800X3D"),
        (2, "RTX 4070"),
    ]


def test_exclusion_wins_over_keyword():
    assert find_matching_products("Ryzen 7 9800X3D usado", PRODUCTS) == []
