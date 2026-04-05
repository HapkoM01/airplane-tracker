import requests


def test_nominatim():
    """Тест Nominatim API"""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": "Russia",
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "AirplaneTracker/1.0 (test@example.com)"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"Status code: {response.status_code}")
        data = response.json()
        if data:
            print(f"Bounding box: {data[0].get('boundingbox')}")
        else:
            print("No data received")
    except Exception as e:
        print(f"Error: {e}")


def test_opensky():
    """Тест OpenSky API"""
    url = "https://opensky-network.org/api/states/all"
    params = {
        "lamin": 41.0,
        "lamax": 82.0,
        "lomin": 19.0,
        "lomax": 180.0
    }
    headers = {
        "User-Agent": "AirplaneTracker/1.0 (test@example.com)"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        print(f"Status code: {response.status_code}")
        data = response.json()
        states = data.get("states", [])
        print(f"Found {len(states)} aircraft")

        # Выводим первые 5 для проверки
        for state in states[:5]:
            print(f"Callsign: {state[1]}, Country: {state[2]}, Altitude: {state[7]}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("Testing Nominatim API...")
    test_nominatim()

    print("\nTesting OpenSky API...")
    test_opensky()
