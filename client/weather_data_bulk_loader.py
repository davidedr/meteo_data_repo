import requests
import csv
import json
from datetime import datetime

headers = {'Content-Type': 'application/json; charset=utf-8'}

# weather=[timestamp_string, timestamp_string_date, timestamp_string_time, wind_speed, wind_direction, pressure, rain_today, rain_rate, temperature, humidity]

cvs_file_name = 'C:\\temp\\meteo_data_repo\\data\\weather_hotelmarcopolo_caorle_v1.txt'
fieldnames = ("timestamp_string", "timestamp_string_date", "timestamp_string_time", "wind_speed", "wind_direction", "pressure", "rain_today", "rain_rate", "temperature", "humidity")

csv_reader = csv.reader(open(cvs_file_name), fieldnames, delimiter=";")
csv_data=list(csv_reader)
line_no=0
for ele in csv_data:
  if ele[4]=="N":
    wind_direction_deg=0
  elif ele[4]=="NNE":
    wind_direction_deg=22.5
  elif ele[4]=="NE":
    wind_direction_deg=45
  elif ele[4]=="ENE":
    wind_direction_deg=67.5
  elif ele[4]=="E":
    wind_direction_deg=90
  elif ele[4]=="ESE":
    wind_direction_deg=112.5
  elif ele[4]=="SE":
    wind_direction_deg=135
  elif ele[4]=="SSE":
    wind_direction_deg=157.5
  elif ele[4]=="S":
    wind_direction_deg=180
  elif ele[4]=="SSO":
    wind_direction_deg=202.5
  elif ele[4]=="SO":
    wind_direction_deg=225
  elif ele[4]=="WSO":
    wind_direction_deg=247.5
  elif ele[4]=="O":
    wind_direction_deg=270
  elif ele[4]=="ONO":
    wind_direction_deg=292.5
  elif ele[4]=="NO":
    wind_direction_deg=315
  elif ele[4]=="NNO":
    wind_direction_deg=337.5

  timestamp = datetime.strptime(ele[0], "%d/%m/%Y %H:%M:%S")
  if ele[8]=="":
    temperature_cels=None
  else:
    temperature_cels=float(ele[8])
  if ele[9]=="":
    rel_humidity=None
  else:
    rel_humidity=float(ele[9])/100

  data_json = {
    "location_id": 1,   
    "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")+".000",
    "wind_speed_knots": float(ele[3])/1.852,
    "wind_direction_deg": wind_direction_deg,
    "barometric_pressure_ssl_hPa": float(ele[5]),
    "rain_today_mm": float(ele[6]),
    "rain_rate_mmh": float(ele[7]),
    "temperature_cels": temperature_cels,
    "rel_humidity": rel_humidity
  }

  headers = {'Content-Type': 'application/json; charset=utf-8'}
  response = requests.post('http://localhost:8080/api/meteo_data', headers = headers, json = data_json)

  line_no=line_no+1
  print(f'Line no: {line_no}, response {response}')

