import requests
import csv
from datetime import datetime
from lxml import html
import requests


#
#
#
def scan(last_seen_timestamp, server, save=True, log=True):

  location_id=server["location_id"]
  name=server["name"]
  weather_station_url=server["url"]

  try:
    page = requests.get(weather_station_url)
  except requests.exceptions.Timeout as err:
    logging.info(f'Server: {location_id}, requests.exceptions.Timeout!')
    logging.info(f'Server: {location_id}, {err}')
    return last_seen_timestamp
  except requests.exceptions.RequestException as err:
    logging.info(f'Server: {location_id}, requests.exceptions.RequestException!') 
    logging.info(f'Server: {location_id}, {err}')
    return last_seen_timestamp
  except Exception as err:
    logging.info(f'Server: {location_id}, Exception!')
    logging.info(f'Server: {location_id}, {err}')
    return last_seen_timestamp

  timestamp_string=None
  timestamp_string_date=None
  timestamp_string_time=None
  try: 
    tree = html.fromstring(page.content)
    timestamp_list = tree.xpath('/html/body/div[2]/table[2]/tbody/tr[1]/td[1]')
    timestamp_ele=timestamp_list[0].text
    timestamp_ele_1=timestamp_ele[1:11]
    timestamp_ele_2=timestamp_ele[14:20]

    timestamp_string=timestamp_ele_1+" "+timestamp_ele_2
    timestamp_obj=datetime.strptime(timestamp_string, "%d.%m.%Y %H:%M")

    timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
    if (log):  
      logging.info(f'Server: {location_id}, timestamp_string: {timestamp_string}')
    
    if last_seen_timestamp and last_seen_timestamp==timestamp_string:
      return last_seen_timestamp

    timestamp_string_date=timestamp_obj.strftime("%d/%m/%Y")
    if (log):
      logging.info(f'Server: {location_id}, timestamp_string_date: {timestamp_string_date}')

    timestamp_string_time=timestamp_obj.strftime("%H:%M:%S")
    if (log):
      logging.info(f'Server: {location_id}, timestamp_string_time: {timestamp_string_time}')

  except Exception as err:
    logging.info(f'Server: {location_id}, {err}')

  wind_speed=None
  try:
    wind_speed_elem = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[1]')
    wind_speed=wind_speed_elem[0].text
    wind_speed=float(wind_speed)
    if (log):
      logging.info(f'Server: {location_id}, wind_speed: {wind_speed}')
  except Exception as err:
    logging.info(f'Server: {location_id}, {err}')

  wind_gust=None
  try:
    wind_gust_elem = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[3]')
    wind_gust=wind_gust_elem[0].text.strip()
    wind_gust=float(wind_gust)
    if (log):
      logging.info(f'Server: {location_id}, wind_gust: {wind_gust}')
  except Exception as err:
    logging.info(f'Server: {location_id}, {err}')

  wind_direction=None
  try:
    wind_direction = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[2]')
    wind_direction=wind_direction[0].text
    wind_direction=wind_direction.split('°')[0].strip()
    if (log):
      logging.info(f'Server: {location_id}, wind_direction: {wind_direction}')
  except Exception as err:
    logging.info(f'Server: {location_id}, {err}')

  pressure=None
  try:
    pressure_elem = tree.xpath('/html/body/div/table[2]/tbody/tr[11]/td[2]')
    pressure=pressure_elem[0].text
    pressure=pressure.split('hPa')[0].strip()
    if (log):
      logging.info(f'Server: {location_id}, pressure: {pressure}')
  except Exception as err:
    logging.info(f'Server: {location_id}, {err}')

  rain_today=None
  try:
    rain_today_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[12]/td[3]')
    rain_today=rain_today_ele[0].text
    rain_today=rain_today.split(';')[0]
    rain_today=rain_today[5:]
    rain_today=rain_today[:-3].strip()
    if (log):
      logging.info(f'Server: {location_id}, rain_today: {rain_today}')
  except Exception as err:
    logging.info(f'Server: {location_id}, {err}')

  rain_rate=None
  try:
    rain_rate_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[12]/td[2]')
    rain_rate=rain_rate_ele[0].text
    rain_rate=rain_rate.split('mm/h')[0].strip()
    if (log):
      logging.info(f'Server: {location_id}, rain_rate: {rain_rate}')
  except Exception as err:
    logging.info(f'Server: {location_id}, {err}')

  temperature=None
  try:
    temperature_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[7]/td[2]')
    temperature=temperature_ele[0].text
    temperature=temperature.split('°')[0].strip()
    if (log):
      logging.info(f'Server: {location_id}, temperature: {temperature}')
  except Exception as err:
    logging.info(f'Server: {location_id}, {err}')

  humidity=None
  try:
    humidity_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[9]/td[2]')
    humidity=humidity_ele[0].text
    humidity=humidity[:len(humidity)-len(" %")].strip()
    if (log):
      logging.info(f'Server: {location_id}, humidity: {humidity}')
  except Exception as err:
    logging.info(f'Server: {location_id}, {err}')

  heat_index=None
  try:
    heat_index_cels_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[8]/td[2]')
    heat_index=heat_index_cels_ele[0].text
    heat_index=heat_index.split('°')[0]
    if (log):
      logging.info(f'Server: {location_id}, heat_index: {heat_index}')
  except Exception as err:
    logging.info(f'Server: {location_id}, {err}')

  dew_point_cels=None
  try:
    dew_point_cels_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[10]/td[2]')
    dew_point_cels=dew_point_cels_ele[0].text
    dew_point_cels=dew_point_cels.split('°')[0]
    if (log):
      logging.info(f'Server: {location_id}, dew_point_cels: {dew_point_cels}')
  except Exception as err:
    logging.info(f'Server: {location_id}, {err}')

  uv_index=None # Unsupported by these weather stations
  if not(timestamp_string and (wind_speed or wind_direction or pressure or rain_today or rain_rate or temperature or humidity or uv_index or heat_index or wind_gust or dew_point_cels)):
    logging.info(f'Server: {location_id}, Not enough scraped data. Skip saving data...')
    logging.info(f'Server: {location_id}, timestamp_string: {timestamp_string}, wind_speed: {wind_speed}, wind_direction: {wind_direction}, pressure: {pressure}, rain_today: {rain_today}, rain_rate: {rain_rate},  temperature: {temperature}, humidity: {humidity}, uv_index: {uv_index}, heat_index: {heat_index}, wind_gust: {wind_gust}, dew_point_cels: {dew_point_cels}')
    return last_seen_timestamp

  # Backup to CSV file
  if (save):
    
    weather=[timestamp_string, timestamp_string_date, timestamp_string_time, wind_speed, wind_direction, pressure, rain_today, rain_rate, temperature, humidity, uv_index, heat_index, wind_gust, dew_point_cels]
    file_name=f"C:\\temp\\meteo_data_repo\\data\\weather_{name}_v3.txt"
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
      "location_id": location_id,
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
    logging.info(f'Server: {location_id}, {timestamp}, response {response}')
  
  return timestamp_ele

#
#
#
def add_server_locations(servers):
  for server in servers:
    if server["location_id"]!=4:
      location_json=server["location"]
      headers={'Content-Type': 'application/json; charset=utf-8'}
      response=requests.post('http://localhost:8080/api/location', headers = headers, json = location_json)
      logging.info(f'Location id: {server["location_id"]}, name: {server["name"]}, response: {response}')

locations_json = [{
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
    "note": "Meteo station @ https://www.meteo-caorle.it/, Porto Santa Margherita, Spiaggia Est, Caorle, Venezia"
}, {
    "name": 'San Giorgio, Venezia',
    "latitude": 45.429939,
    "longitude": 12.342716,
    "address_complete": "30100 Venezia, Città Metropolitana di Venezia",
    "street_1": "",
    "street_2": "",
    "zip": "30100",
    "town": "Venezia",
    "province": "Città Metropolitana di Venezia",
    "country": "IT",
    "note": "Meteo station @ https://www.meteo-venezia.net/compagnia01.php, Isola di San Giorgio Maggiore, Venezia"
}, {
    "name": 'Punta San Giuliano, Mestre-Venezia',
    "latitude": 45.629892,
    "longitude": 12.997956,
    "address_complete": "Via S. Giuliano, 23, 30174 Venezia VE",
    "street_1": "Via S. Giuliano, 23",
    "street_2": "",
    "zip": "30174",
    "town": "Mestre",
    "province": "VE",
    "country": "IT",
    "note": "Meteo station @ https://www.meteo-venezia.net/, Punta San Giuliano, Mestre-Venezia"
},{
    "name": 'Laguna Park Hotel, Bibione, Venezia',
    "latitude": 45.466542,
    "longitude": 12.282729,
    "address_complete": "Via Passeggiata al Mare, 20, 30028 Bibione VE",
    "street_1": "Via Passeggiata al Mare, 20",
    "street_2": "",
    "zip": "30028",
    "town": "Bibione",
    "province": "VE",
    "country": "IT",
    "note": "Meteo station @ https://www.bibione-meteo.it/, Bibione, Venezia"
}]

servers = [
  { "location_id": 4, "location": locations_json[0], "name": "bagnomargherita_caorle", "url": "https://www.meteo-caorle.it/" },
  { "location_id": 8, "location": locations_json[1], "name": "sangiorgio_venezia", "url": "https://www.meteo-venezia.net/compagnia01.php" },
  { "location_id": 9, "location": locations_json[2], "name": "puntasangiuliano_mestre", "url": "https://www.meteo-venezia.net/" },
  { "location_id": 10, "location": locations_json[3], "name": "lagunaparkhotel_bibione", "url": "https://www.bibione-meteo.it/" }
]

#add_server_locations(servers)

#
#
#
def main_logger(server):
  logging.info(f'Thread ident: {threading.get_ident()}, Client for server: {server["location_id"]}, {server["name"]}, url: {server["url"]} up and running.')
  while True:
    last_seen_timestamp=server.get("last_seen_timestamp", None)
    scan_no=server.get("scan_no", 0)
    scan_no=scan_no+1
    logging.info(f'Server: {server["location_id"]}, {server["name"]}, scan: {scan_no}...')
    last_seen_timestamp=scan(last_seen_timestamp, server, True, False)
    server["last_seen_timestamp"]=last_seen_timestamp
    server["scan_no"]=scan_no
    time.sleep(50)

#
#
#
import logging
import threading
import time

if __name__=="__main__":
  format = "%(asctime)s %(thread)d %(threadName)s: %(message)s"
  logging.basicConfig(format=format, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")
  nclients=0
  for server in servers:
    logging.info(f'Starting client for server: {server["location_id"]}, {server["name"]}, url: {server["url"]}...')
    threading.Thread(target=main_logger, args=(server, )).start()
    nclients=nclients+1

  logging.info(f'Client starting complete. Started: {nclients} clients.')
