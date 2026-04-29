from weather import get_forecast, get_temperature
from weather.exceptions import InvalidCityError

print(get_forecast("kathmandu"))
print(get_forecast("london"))

try:
    get_temperature("paris")
except InvalidCityError as e:
    print(f"Error: {e}")


if __name__ == "__main__":
    print("Running main weather app")