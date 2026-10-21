import re
import unicodedata


def _normalize(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.casefold())
    without_accents = "".join(
        char for char in normalized if not unicodedata.combining(char)
    )
    return re.sub(r"\s+", " ", without_accents).strip()


def find_matching_products(text, products):
    normalized_text = _normalize(text)
    matches = []
    for product in products:
        excluded = any(
            _normalize(exclusion) in normalized_text
            for exclusion in product.get("exclude_words", [])
            if exclusion.strip()
        )
        if excluded:
            continue

        if any(
            _normalize(keyword) in normalized_text
            for keyword in product.get("keywords", [])
            if keyword.strip()
        ):
            matches.append((product["id"], product["name"]))
    return matches


def find_matching_product(text, products):
    matches = find_matching_products(text, products)
    return matches[0] if matches else (None, None)
