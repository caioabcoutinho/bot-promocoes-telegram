from src.extractor import extract_price, parse_message


def test_installment_price_is_converted_to_total():
    assert extract_price("Ryzen por R$ 200,00 x 10") == 2000.0


def test_cash_price_takes_precedence_over_installment():
    assert extract_price("R$ 2.000,00 à vista ou R$ 200,00 x 10") == 2000.0


def test_parse_message_returns_coupon_and_trimmed_url():
    assert parse_message(
        "RTX por R$ 3.000,00 cupom: PC10 https://kabum.com.br/oferta)."
    ) == (3000.0, "https://kabum.com.br/oferta", "KaBuM!", "PC10")
