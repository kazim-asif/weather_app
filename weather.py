import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# It's good practice to keep the fallback for local dev, but move the real key to .env
API_KEY = os.environ.get('WEATHER_API_KEY')

@app.route('/', methods=['POST', 'GET'])
def weather():
    # Cleaner way to handle the default city
    city = request.form.get('city', 'Karachi') if request.method == 'POST' else 'Karachi'

    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status() 
        w_data = response.json()

        # Extract data using the correct keys
        data = {
            "cityname": w_data.get('name'), # Note: 'name' is top-level
            "country_code": w_data['sys'].get('country'),
            "coordinate": f"{w_data['coord']['lon']}, {w_data['coord']['lat']}",
            "temp": f"{w_data['main']['temp']}°C",
            "pressure": f"{w_data['main']['pressure']} hPa",
            "humidity": f"{w_data['main']['humidity']}%",
        }

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        # Passing an error key allows you to use {% if data.error %} in HTML
        data = {"error": f"City '{city}' not found. Please try again."}

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)