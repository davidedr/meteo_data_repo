import requests
import csv
from datetime import datetime
from lxml import html
import requests
import unicodedata

#
# Add location to database
#
def add_location():
  location_json = {
    "name": 'Bagno Margherita Caorle',
    "latitude": 45.588340,
    "longitude": 12.861544,
    "address_complete": "Viale Lepanto, 13A, 30021 Porto Santa Margherita VE",
    "street_1": "Viale Lepanto, 13A",
    "street_2": "Porto Santa Margherita",
    "zip": "30021",
    "town": "Caorle",
    "province": "VE",
    "country": "IT",
    "note": "Meteo station @ https://www.meteo-caorle.it/, Porto Santa Margherita, Spiaggia Est"
  }

  headers={'Content-Type': 'application/json; charset=utf-8'}
  response=requests.post('http://localhost:8080/api/location', headers = headers, json = location_json)
  print('Response: {response}')

#
#
#
def scan(last_seen_timestamp, log=True):
  page = requests.get('https://www.meteo-caorle.it/')
  tree = html.fromstring(page.content)

  timestamp_list = tree.xpath('/html/body/div[2]/table[2]/tbody/tr[1]/td[1]')
  timestamp_ele=timestamp_list[0].text
  timestamp_ele_1=timestamp_ele[1:11]
  timestamp_ele_2=timestamp_ele[14:20]

  timestamp_string=timestamp_ele_1+" "+timestamp_ele_2
  timestamp_obj=datetime.strptime(timestamp_string, "%d.%m.%Y %H:%M")

  timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
  print("timestamp_string: "+timestamp_string)
  if (log):  
    print("timestamp_string")
    print(timestamp_string)

  timestamp_string_date=timestamp_obj.strftime("%d/%m/%Y")
  if (log):  
    print("timestamp_string_date")
    print(timestamp_string_date)

  timestamp_string_time=timestamp_obj.strftime("%H:%M:%S")
  if (log):  
    print("timestamp_string_time")
    print(timestamp_string_time)

  wind_speed_elem = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[1]')
  wind_speed=wind_speed_elem[0].text
  wind_speed=float(wind_speed)
  if (log):
    print("wind_speed")
    print(wind_speed)

  wind_gust_elem = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[3]')
  wind_gust=wind_gust_elem[0].text.strip()
  wind_gust=float(wind_gust)
  if (log):
    print("wind_gust")
    print(wind_gust)

  wind_direction = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[2]')
  wind_direction=wind_direction[0].text
  wind_direction=wind_direction.split('°')[0].strip()
  if (log):
    print("wind_direction")
    print(wind_direction)

  pressure_elem = tree.xpath('/html/body/div/table[2]/tbody/tr[11]/td[2]')
  pressure=pressure_elem[0].text
  pressure=pressure.split('hPa')[0].strip()
  if (log):
    print("pressure")
    print(pressure)

  rain_today_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[12]/td[3]')
  rain_today=rain_today_ele[0].text
  rain_today=rain_today.split(';')[0]
  rain_today=rain_today[5:]
  rain_today=rain_today[:-3].strip()
  if (log):
    print("rain_today")
    print(rain_today)

  rain_rate_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[12]/td[2]')
  rain_rate=rain_rate_ele[0].text
  rain_rate=rain_rate.split('mm/h')[0].strip()
  if (log):
    print("rain_rate")
    print(rain_rate)

  temperature_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[7]/td[2]')
  temperature=temperature_ele[0].text
  temperature=temperature.split('°')[0].strip()
  if (log):
    print("temperature")
    print(temperature)

  humidity_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[9]/td[2]')
  humidity=humidity_ele[0].text
  humidity=humidity[:len(humidity)-len(" %")].strip()
  if (log):
    print("humidity")
    print(humidity)

  heat_index_cels_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[8]/td[2]')
  heat_index=heat_index_cels_ele[0].text
  heat_index=heat_index.split('°')[0]
  if (log):
    print("heat_index")
    print(heat_index)

  dew_point_cels_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[10]/td[2]')
  dew_point_cels=dew_point_cels_ele[0].text
  dew_point_cels=dew_point_cels.split('°')[0]
  if (log):
    print("dew_point_cels")
    print(dew_point_cels)

  # Backup to CSV file
  uv_index=None
  weather=[timestamp_string, timestamp_string_date, timestamp_string_time, wind_speed, wind_direction, pressure, rain_today, rain_rate, temperature, humidity, uv_index, heat_index, wind_gust, dew_point_cels]
  file_name="C:\\temp\\meteo_data_repo\\data\\weather_bagnomargherita_caorle_v3.txt"
  from csv import writer
  with open(file_name, 'a+', newline='') as write_obj:
    # Create a writer object from csv module
    csv_writer = writer(write_obj, delimiter=";")
    # Add contents of list as last row in the csv file
    csv_writer.writerow(weather)

  # Insert into database

  # Convert to PGSQL format
  timestamp = datetime.strptime(timestamp_string, "%d/%m/%Y %H:%M:%S")
  timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")+".000"

  # Guard against empty values
  if temperature=="":
    temperature_cels=None
  else:
    temperature_cels=float(temperature)
  if humidity=="":
    rel_humidity=None
  else:
    rel_humidity=float(humidity)/100

  data_json = {
    "location_id": 4,
    "timestamp": timestamp,
    "wind_speed_knots": float(wind_speed),
    "wind_direction_deg": wind_direction,
    "barometric_pressure_hPa": float(pressure),
    "rain_today_mm": float(rain_today),
    "rain_rate_mmph": float(rain_rate),
    "temperature_cels": temperature_cels,
    "rel_humidity": rel_humidity,
    "uv_index": uv_index,
    "heat_index_cels": heat_index,
    "wind_gust_knots": wind_gust,
    "dew_point_cels": dew_point_cels
  }

  headers={'Content-Type': 'application/json; charset=utf-8'}
  response=requests.post('http://localhost:8080/api/meteo_data', headers = headers, json = data_json)
  print(f'{timestamp}, response {response}')
  
  return timestamp_ele

# add_location()

import time
last_seen_timestamp=''
last_seen_timestamp=scan(last_seen_timestamp)
scan_no=0

while True:
  time.sleep(50)
  scan_no=scan_no+1
  print("scan "+ str(scan_no)+"...")
  last_seen_timestamp=scan(last_seen_timestamp)