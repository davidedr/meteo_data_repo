import requests
import csv
from datetime import datetime
from lxml import html
import requests
import unicodedata

#
#
#
def scan(last_seen_timestamp, log=False):

  try:
    page = requests.get('https://www.hotelmarcopolocaorle.it/meteo/hmpolocaorle.php')
  except requests.exceptions.Timeout as err:
    logging.info(f'Server: {location_id}, requests.exceptions.Timeout!')
    logging.info(f'Server: {location_id}, {err}')

  tree = html.fromstring(page.content)

  timestamp_list = tree.xpath('/html/body/span')
  if (log):
    print(type(timestamp_list))
    for timestamp_ele in timestamp_list:
      print(type(timestamp_ele))
      print(timestamp_ele.text)

  timestamp_ele=timestamp_list[0].text
  # if (last_seen_timestamp == timestamp_ele):
  #   return timestamp_ele

  timestamp_string=timestamp_ele[-len('Dati in real-time aggiornati alle: ')+4:]
  from datetime import datetime
  timestamp_obj=datetime.strptime(timestamp_string, "%a, %d %b %Y %H:%M:%S %z")
  if (log):
    print("timestamp_obj")
    print(timestamp_obj)

  timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
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

  wind_speed_elems = tree.xpath('/html/body/table/tbody/tr[2]/td[2]/h1[2]/big/big/big/span/text()')
  wind_speed=wind_speed_elems[0]
  wind_speed=wind_speed.strip()
  wind_speed=float(wind_speed)/1.852
  if (log):
    print("wind_speed")
    print(wind_speed)

  wind_direction = tree.xpath('/html/body/table/tbody/tr[2]/td[2]/h4/big/big/span/big/big/text()')
  wind_direction=wind_direction[0]
  if (log):
    print("wind_direction")
    print(wind_direction)

  pressure_ele = tree.xpath('/html/body/table/tbody/tr[2]/td[3]/h1[2]/big/span')
  pressure=pressure_ele[0].text
  pressure=pressure.strip()
  if (log):
    print("pressure")
    print(pressure)

  rain_today_ele = tree.xpath('/html/body/table/tbody/tr[4]/td[2]/h1[2]/big/span')
  rain_today=rain_today_ele[0].text
  rain_today=rain_today[:1]
  rain_today=rain_today.strip()
  if (log):
    print("rain_today")
    print(rain_today)

  rain_rate_ele = tree.xpath('/html/body/table/tbody/tr[4]/td[2]/h2')
  rain_rate=rain_rate_ele[0].text
  rain_rate=rain_rate[len('IntensitÃƒ'):]
  rain_rate=rain_rate[:3]
  rain_rate=rain_rate.strip()
  if (log):
    print("rain_rate")
    print(rain_rate)

  temperature_ele = tree.xpath('/html/body/table/tbody/tr[2]/td[1]/h1[3]/big/big/big')
  temperature=temperature_ele[0].text
  temperature=temperature[:len(temperature)-len("Â°C")+1]
  temperature=temperature.strip()
  if (log):
    print("temperature")
    print(temperature)

  humidity_ele = tree.xpath('/html/body/table/tbody/tr[3]/td/h1[2]/big/span')
  humidity=humidity_ele[0].text
  humidity=humidity[:len(humidity)-len(" %")]
  humidity=humidity.strip()
  if (log):
    print("humidity")
    print(humidity)

  uv_index_ele = tree.xpath('/html/body/table/tbody/tr[4]/td[1]/h1[2]/big/span')
  uv_index=uv_index_ele[0].text
  uv_index=uv_index.strip()
  if (log):
    print("uv_index")
    print(uv_index)

  heat_index_cels_ele = tree.xpath('/html/body/table/tbody/tr[2]/td[1]/h3[4]/big/span')
  heat_index=heat_index_cels_ele[0].text
  heat_index=heat_index[len('Indice di calore: '):]
  heat_index=heat_index[:len(heat_index)-len("°C")-1]
  heat_index=heat_index.strip()
  if (log):
    print("heat_index")
    print(heat_index)

  # Backup to CSV file
  wind_gust=None
  dew_point_cels=None
  weather=[timestamp_string, timestamp_string_date, timestamp_string_time, wind_speed, wind_direction, pressure, rain_today, rain_rate, temperature, humidity, uv_index, heat_index, wind_gust, dew_point_cels]
  file_name="C:\\temp\\meteo_data_repo\\data\\weather_hotelmarcopolo_caorle_v3.txt"
  from csv import writer
  with open(file_name, 'a+', newline='') as write_obj:
    # Create a writer object from csv module
    csv_writer = writer(write_obj, delimiter=";")
    # Add contents of list as last row in the csv file
    csv_writer.writerow(weather)

  # Insert into database
  wind_direction_deg=None
  if wind_direction=="N":
    wind_direction_deg=0
  elif wind_direction=="NNE":
    wind_direction_deg=22.5
  elif wind_direction=="NE":
    wind_direction_deg=45
  elif wind_direction=="ENE":
    wind_direction_deg=67.5
  elif wind_direction=="E":
    wind_direction_deg=90
  elif wind_direction=="ESE":
    wind_direction_deg=112.5
  elif wind_direction=="SE":
    wind_direction_deg=135
  elif wind_direction=="SSE":
    wind_direction_deg=157.5
  elif wind_direction=="S":
    wind_direction_deg=180
  elif wind_direction=="SSO":
    wind_direction_deg=202.5
  elif wind_direction=="SO":
    wind_direction_deg=225
  elif wind_direction=="OSO":
    wind_direction_deg=247.5
  elif wind_direction=="O":
    wind_direction_deg=270
  elif wind_direction=="ONO":
    wind_direction_deg=292.5
  elif wind_direction=="NO":
    wind_direction_deg=315
  elif wind_direction=="NNO":
    wind_direction_deg=337.5
  else:
    print("Unknown wind_direction: '{wind_direction}'!")

  # Convert to PGSQL format
  timestamp = datetime.strptime(timestamp_string, "%d/%m/%Y %H:%M:%S")
  timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")+".000"

  # Guard against empty values
  temperature_cels=None
  if temperature:
    temperature_cels=float(temperature)

  rel_humidity=None
  if humidity:
    rel_humidity=float(humidity)/100

  data_json = {
    "location_id": 1,   
    "timestamp": timestamp,
    "wind_speed_knots": float(wind_speed),
    "wind_direction_deg": wind_direction_deg,
    "barometric_pressure_hPa": float(pressure),
    "rain_today_mm": float(rain_today),
    "rain_rate_mmph": float(rain_rate),
    "temperature_cels": temperature_cels,
    "rel_humidity": rel_humidity,
    "uv_index": uv_index,
    "heat_index_cels": heat_index
  }

  headers={'Content-Type': 'application/json; charset=utf-8'}
  response=requests.post('http://localhost:8080/api/meteo_data', headers = headers, json = data_json)
  print(f'{timestamp}, response {response}')
  
  return timestamp_ele

import time
last_seen_timestamp=''
last_seen_timestamp=scan(last_seen_timestamp)
scan_no=0
while True:
  time.sleep(50)
  scan_no=scan_no+1
  print("scan "+ str(scan_no)+"...")
  last_seen_timestamp=scan(last_seen_timestamp)