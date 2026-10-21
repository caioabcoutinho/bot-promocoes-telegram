import re
from dataclasses import dataclass
from typing import Optional

from src.stores import DEFAULT_STORES, identify_store as identify_registered_store

_MONEY = r"\d{1,3}(?:\.\d{3})*(?:,\d{2})?|\d+(?:,\d{2})?"
_CASH_PRICE = re.compile(
    rf"(?<!\w)R\$\s*(?P<value>{_MONEY})", re.IGNORECASE
)
_INSTALLMENT_PRICE = re.compile(
    rf"(?:(?P<count>\d+)\s*x\s*(?:de\s*)?R\$\s*(?P<installment_value>{_MONEY})|"
    rf"R\$\s*(?P<total_value>{_MONEY})\s*x\s*(?P<amount_count>\d+))",
    re.IGNORECASE,
)
_FALLBACK_PRICE = re.compile(
    rf"(?i)(?:por|apenas)\s*R?\$?\s*(?P<value>{_MONEY})"
)


@dataclass(frozen=True)
class PriceCandidate:
    value: float
    start: int
    end: int
    installment: bool


def _to_float(value: str) -> float:
    return float(value.replace(".", "").replace(",", "."))


def _price_candidates(text: str) -> list[PriceCandidate]:
    candidates: list[PriceCandidate] = []
    for match in _INSTALLMENT_PRICE.finditer(text):
        amount = match.group("installment_value") or match.group("total_value")
        count = match.group("count") or match.group("amount_count")
        if amount and count:
            candidates.append(
                PriceCandidate(
                    _to_float(amount) * int(count),
                    match.start(),
                    match.end(),
                    True,
                )
            )

    installment_ranges = [(candidate.start, candidate.end) for candidate in candidates]
    for pattern in (_CASH_PRICE, _FALLBACK_PRICE):
        for match in pattern.finditer(text):
            if any(
                match.start() < end and match.end() > start
                for start, end in installment_ranges
            ):
                continue
            candidates.append(
                PriceCandidate(
                    _to_float(match.group("value")),
                    match.start(),
                    match.end(),
                    False,
                )
            )
    return candidates


def extract_price(text: str) -> Optional[float]:
    candidates = _price_candidates(text)
    if not candidates:
        return None
    cash = [candidate for candidate in candidates if not candidate.installment]
    return (cash or candidates)[0].value


def extract_url(text: str) -> Optional[str]:
    match = re.search(r"https?://[^\s]+", text)
    return match.group(0).rstrip(".,);]") if match else None


def identify_store(text: str, url: Optional[str], stores=()) -> str:
    configured = stores or [
        (name, aliases, domains, False)
        for name, aliases, domains in DEFAULT_STORES
    ]
    return identify_registered_store(text, url, configured)[0]


def extract_coupon(text: str) -> Optional[str]:
    match = re.search(r"(?i)(?:cupom|código)[\s:]+([A-Z0-9_-]+)", text)
    return match.group(1).upper() if match else None


def parse_message(text: str):
    url = extract_url(text)
    return extract_price(text), url, identify_store(text, url), extract_coupon(text)
