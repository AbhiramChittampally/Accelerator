def fetch_temperature(city):
    # Imagine this calls an external weather API.
    raise NotImplementedError("Real API not implemented")


def temperature_message(city):
    temperature = fetch_temperature(city)
    return f"{city}: {temperature} C"