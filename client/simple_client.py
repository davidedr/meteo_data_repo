# Simple Python client
import requests
import json

data_json = {
    "location_id": 1,
    "wind_speed_knots": 20,
    "wind_direction_deg": 21,
    "barometric_pressure_ssl_hPa": 22.1,
    "rain_today_mm": 23,
    "rain_rate_mmh": 24.1,
    "temperature_cels": 25.1,
    "rel_humidity": 0.26,
    "uv_index": 27.1,
    "heat_index_cels": 28.1
}

headers = {'Content-Type': 'application/json; charset=utf-8'}
response = requests.post('http://localhost:8080/api/meteo_data', headers = headers, json = data_json)
print("response")
print(response.status_code)
print(response)
