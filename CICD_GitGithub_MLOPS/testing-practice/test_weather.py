from unittest.mock import patch

from weather import temperature_message


def test_temperature_message():
    with patch("weather.fetch_temperature", return_value=25) as mock_fetch:
        result = temperature_message("Hyderabad")

    assert result == "Hyderabad: 25 C"
    mock_fetch.assert_called_once_with("Hyderabad")