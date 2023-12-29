from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Замените на свой API-ключ для Yandex Weather
API_KEY = "your_yandex_weather_api_key"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form['city']

    # Получаем координаты города с помощью геокодера DaData
    dadata_url = 'https://cleaner.dadata.ru/api/v1/clean/address'
    headers = {
        'Authorization': 'Bearer your_dadata_api_key',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    dadata_payload = {
        'query': city,
        'count': 1
    }
    dadata_response = requests.post(dadata_url, headers=headers, data=json.dumps(dadata_payload))
    coordinates = dadata_response.json()[0]['data']['geo_lat'], dadata_response.json()[0]['data']['geo_lon']

    # Получаем данные о погоде с помощью Yandex Weather API
    weather_url = f'https://api.weather.yandex.ru/v2/informers?lat={coordinates[0]}&lon={coordinates[1]}'
    headers = {
        'X-Yandex-API-Key': API_KEY
    }
    weather_response = requests.get(weather_url, headers=headers)
    weather_data = weather_response.json()

    # Передаем данные в HTML-шаблон
    return render_template('weather.html', city=city, weather=weather_data)


if __name__ == '__main__':
    app.run(debug=True)
