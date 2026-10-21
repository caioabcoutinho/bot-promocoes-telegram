from urllib.parse import urlparse

from src.matcher import _normalize


DEFAULT_STORES = (
    ("KaBuM!", ("kabum",), ("kabum.com.br",)),
    ("Pichau", ("pichau",), ("pichau.com.br",)),
    ("Terabyte", ("terabyte",), ("terabyteshop.com.br",)),
    ("Amazon", ("amazon",), ("amazon.com.br", "amazon.com")),
    (
        "Mercado Livre",
        ("mercado livre", "mercadolivre"),
        ("mercadolivre.com.br",),
    ),
    ("AliExpress", ("aliexpress",), ("aliexpress.com",)),
)


def _host(url):
    if not url:
        return ""
    parsed = urlparse(url if "://" in url else f"https://{url}")
    return parsed.hostname.casefold().removeprefix("www.") if parsed.hostname else ""


def identify_store(text, url, stores=()):
    host = _host(url)
    normalized_text = _normalize(text)
    for name, aliases, domains, blocked in stores:
        if any(host == domain or host.endswith(f".{domain}") for domain in domains):
            return name, blocked
        if any(_normalize(alias) in normalized_text for alias in aliases):
            return name, blocked
    return "Desconhecida", False
