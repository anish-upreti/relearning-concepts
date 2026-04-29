from weather.exceptions import InvalidCityError

def get_temperature(city):
    data = {
        "kathmandu": 18,
        "london": 12,
        "tokyo": 25
    }

    city = city.lower()
    
    if city not in data:
        raise InvalidCityError(f"{city} is not in our database")
    
    return data[city]

def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

if __name__ == "__main__":
    print(get_temperature("kathmandu"))
    print(celsius_to_fahrenheit(18))
