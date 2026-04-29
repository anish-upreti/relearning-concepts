from weather.temperature import get_temperature

def get_forecast(city):
    temp = get_temperature(city)

    if temp < 15:
        return f"{city}: Cold day, {temp}°C"
    elif temp < 22:
        return f"{city}: Nice day, {temp}°C"
    else:
        return f"{city}: Hot day, {temp}°C"


if __name__ == "__main__":
    print(get_forecast("tokyo"))