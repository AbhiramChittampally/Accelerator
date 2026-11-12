
def fetch_exchange_rate_from_api(currency):
    """
    Simulates fetching exchange rate from an external API.
    """
    print(f"Calling external API for {currency}")

    rates = {
        "USD": 83.0,
        "EUR": 90.0,
    }

    return rates.get(currency)


def get_exchange_rate(currency):
    rate = fetch_exchange_rate_from_api(currency)

    if rate is None:
        raise ValueError("Unsupported currency")

    return rate
