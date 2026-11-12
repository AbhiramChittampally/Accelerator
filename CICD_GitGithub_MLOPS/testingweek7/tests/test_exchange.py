
import pytest
from unittest.mock import patch

from src.exchange import (
    get_exchange_rate,
    fetch_exchange_rate_from_api,
)


def test_get_exchange_rate():
    with patch(
        "src.exchange.fetch_exchange_rate_from_api"
    ) as mock_api:

        mock_api.return_value = 85.0

        result = get_exchange_rate("USD")

        assert result == 85.0
        mock_api.assert_called_once_with("USD")


def test_unsupported_currency():
    with patch(
        "src.exchange.fetch_exchange_rate_from_api"
    ) as mock_api:

        mock_api.return_value = None

        with pytest.raises(ValueError):
            get_exchange_rate("XYZ")


def test_fetch_exchange_rate_from_api():
    assert fetch_exchange_rate_from_api("USD") == 83.0
    assert fetch_exchange_rate_from_api("EUR") == 90.0
    assert fetch_exchange_rate_from_api("XYZ") is None
