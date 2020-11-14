import requests
from fake_useragent import UserAgent
from datetime import datetime
import logging
from lxml import html
import os
from csv import writer
import json

import definitions

#
#
#
def log_sample(location_id, server_name, meteo_data_dict):
  msg=f'{get_identification_string(location_id, server_name)},'
  for k, v in meteo_data_dict.items():
    msg=msg+f' {k}: {v},'
  msg=msg[:-1]
  logging.info(msg)  

#
#
#
def add_server_location_if_doesnot_exist(server):
    headers={'Content-Type': 'application/json; charset=utf-8'}
    location_id=server['location_id']
    server_name=server['name']
    location_response=requests.get(f'http://localhost:8080/api/location/{location_id}', headers=headers)
    location_json=json.loads(location_response.text)
    if location_json and location_json[0] and location_json[0]["id"]==location_id:
        logging.info(f'{get_identification_string(location_id, server_name)}: Found in db')
        return
    logging.info(f'{get_identification_string(location_id, server_name)}: Not found in db. Adding...')
    location_json=server["location"]
    response=requests.post('http://localhost:8080/api/location', headers=headers, json=location_json)
    logging.info(f'Location id: {server["location_id"]}, name: {server["name"]}, response: {response}')

#
# Return an human-readable server identification string
#
def get_identification_string(location_id, server_name=None):
  if server_name:
    return f'Server: {location_id}, {server_name}'
  else:
    return f'Server: {location_id}'

#
#
#
def test_starter(location_id, log_level=logging.NOTSET):
  found_server=None
  for server in definitions.servers:
    if server["location_id"]==location_id:
      found_server=server
  if not found_server:
    return

  server=found_server
  log_format = "%(asctime)s %(thread)d %(threadName)s: %(message)s"
  log_dateformat="%Y-%m-%d %H:%M:%S"
  log_filename=f'app/log/meteo_data_repo_{location_id}_{server["name"]}_test.log'
  logging.basicConfig(filename=log_filename, format=log_format, level=log_level, datefmt=log_dateformat)

  logging.info(f'Starting scanner {get_identification_string(location_id, server["name"])} scanning...')
  server["scanner"](None, server, save=True, log=True)
  logging.info(f'Starting scanner {get_identification_string(location_id, server["name"])} scanner ends.')

#
#
#
def log_xpath_elem(tree, path="//font"):
  elems=tree.xpath(path)
  i=0
  logging.info(f'Found: {len(elems)} in tree for xpath:"{path}".')
  for ele in elems:
    logging.info(f'{i}, {ele.text}')
    i=i+1

#
#
#
def convert_wind_direction_to_deg(wind_direction):

  wind_direction_deg=None
  wind_direction=wind_direction.upper()
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
  elif wind_direction=="SSO" or wind_direction=="SSW":
    wind_direction_deg=202.5
  elif wind_direction=="SO" or wind_direction=="SW":
    wind_direction_deg=225
  elif wind_direction=="OSO" or wind_direction=="WSW":
    wind_direction_deg=247.5
  elif wind_direction=="O" or wind_direction=="W":
    wind_direction_deg=270
  elif wind_direction=="ONO" or wind_direction=="WNW":
    wind_direction_deg=292.5
  elif wind_direction=="NO" or wind_direction=="NW":
    wind_direction_deg=315
  elif wind_direction=="NNO" or wind_direction=="NNW":
    wind_direction_deg=337.5

  return wind_direction_deg

#
# Get the web page and convert it to a DOM tree
#

# TODO: move to kind of an "abstract class"
def get_tree(weather_station_url, location_id, server_name=None):
  
  user_agent = UserAgent().random 
  headers = {'User-Agent': user_agent}

  try:
    page = requests.get(weather_station_url, headers=headers)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception in requests.get, {e}, weather_station_url: "{weather_station_url}".')
    return None, None

  try:
    tree = html.fromstring(page.text)    

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception in html.fromstring, {e}!')
    return None, None

  return (tree, page.text)

#
# Save data to CSV file and REST API server
#

# TODO: move to kind of an "abstract class"
def save_v6(location_id, server_name, meteo_data_dict, save=True):

  if not save:
    logging.info(f'{get_identification_string(location_id, server_name)}: Save disabled!')
    return

  timestamp_string=meteo_data_dict.get("timestamp_string")
  timestamp_string_date=meteo_data_dict.get("timestamp_string_date")
  timestamp_string_time=meteo_data_dict.get("timestamp_string_time")
  wind_speed_knots=meteo_data_dict.get("wind_speed_knots")
  wind_direction_deg=meteo_data_dict.get("wind_direction_deg")
  barometric_pressure_hPa=meteo_data_dict.get("barometric_pressure_hPa")
  rain_today_mm=meteo_data_dict.get("rain_today_mm")
  rain_rate_mmph=meteo_data_dict.get("rain_rate_mmph")
  temperature_cels=meteo_data_dict.get("temperature_cels")
  rel_humidity=meteo_data_dict.get("rel_humidity")
  uv_index=meteo_data_dict.get("uv_index")
  heat_index_cels=meteo_data_dict.get("heat_index_cels")
  wind_gust_knots=meteo_data_dict.get("wind_gust_knots")
  dew_point_cels=meteo_data_dict.get("dew_point_cels")
  wind_chill_cels=meteo_data_dict.get("wind_chill_cels")
  ground_temperature_cels=meteo_data_dict.get("ground_temperature_cels")
  solar_irradiance_wpsm=meteo_data_dict.get("solar_irradiance_wpsm")
  rel_leaf_wetness=meteo_data_dict.get("rel_leaf_wetness")
  soil_moisture_cb=meteo_data_dict.get("soil_moisture_cb")
  rain_this_month_mm=meteo_data_dict.get("rain_this_month_mm")
  rain_this_year_mm=meteo_data_dict.get("rain_this_year_mm")
  evapotranspiration_today_mm=meteo_data_dict.get("evapotranspiration_today_mm")
  evapotranspiration_this_month_mm=meteo_data_dict.get("evapotranspiration_this_month_mm")
  evapotranspiration_this_year_mm=meteo_data_dict.get("evapotranspiration_this_year_mm")
  
  #
  # Saving to csv backup file and database server
  #

  # Header
  csv_file_header=["timestamp_string", "timestamp_string_date", "timestamp_string_time", "wind_speed_knots", "wind_direction_deg", "barometric_pressure_hPa", "rain_today_mm", "rain_rate_mmph", "temperature_cels", "rel_humidity", "uv_index", "heat_index_cels", "wind_gust_knots", "dew_point_cels", "wind_chill_cels", "ground_temperature_cels", "solar_irradiance_wpsm", "rel_leaf_wetness", "soil_moisture_cb", "rain_this_month_mm", "rain_this_year_mm", "evapotranspiration_today_mm", "evapotranspiration_this_month_mm", "evapotranspiration_this_year_mm"]

  save_to_csv_ok=True
  save_to_rest_ok=True
  file_name=f"data/weather_{location_id}_{server_name}_v6.txt"
  try:
    with open(file_name, 'a+', newline='') as write_obj:
      csv_writer = writer(write_obj, delimiter=";")
      if os.stat(file_name).st_size == 0:
        csv_writer.writerow(csv_file_header)

      weather=[timestamp_string, timestamp_string_date, timestamp_string_time, wind_speed_knots, wind_direction_deg, barometric_pressure_hPa, rain_today_mm, rain_rate_mmph, temperature_cels, rel_humidity, uv_index, heat_index_cels, wind_gust_knots, dew_point_cels, wind_chill_cels, ground_temperature_cels, solar_irradiance_wpsm, rel_leaf_wetness, soil_moisture_cb, rain_this_month_mm, rain_this_year_mm, evapotranspiration_today_mm, evapotranspiration_this_month_mm, evapotranspiration_this_year_mm]
      csv_writer.writerow(weather)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} saving to csv file: {file_name}!')
    save_to_csv_ok=False

  # Insert into database

  # Convert to PGSQL format
  timestamp = datetime.strptime(timestamp_string, "%d/%m/%Y %H:%M:%S")
  timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")+".000"

  data_json = {
    "location_id": location_id,   
    "timestamp_ws": timestamp,
    "wind_speed_knots": wind_speed_knots,
    "wind_direction_deg": wind_direction_deg,
    "barometric_pressure_hPa": barometric_pressure_hPa,
    "rain_today_mm": rain_today_mm,
    "rain_rate_mmph": rain_rate_mmph,
    "temperature_cels": temperature_cels,
    "rel_humidity": rel_humidity,
    "uv_index": uv_index,
    "heat_index_cels": heat_index_cels,
    "wind_gust_knots": wind_gust_knots,
    "dew_point_cels": dew_point_cels,
    "wind_chill_cels": wind_chill_cels,
    "ground_temperature_cels": ground_temperature_cels,
    "solar_irradiance_wpsm": solar_irradiance_wpsm,
    "rel_leaf_wetness": rel_leaf_wetness,
    "soil_moisture_cb": soil_moisture_cb,
    "rain_this_month_mm": rain_this_month_mm,
    "rain_this_year_mm": rain_this_year_mm,
    "evapotranspiration_today_mm": evapotranspiration_today_mm,
    "evapotranspiration_this_month_mm": evapotranspiration_this_month_mm,
    "evapotranspiration_this_year_mm": evapotranspiration_this_year_mm
  }

  headers={'Content-Type': 'application/json; charset=utf-8'}
  try:
    rest_server='http://localhost:8080/api/meteo_data'
    response=requests.post(rest_server, headers=headers, json=data_json)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} POSTing to: {rest_server}!')
    save_to_rest_ok=False

  if save_to_csv_ok and save_to_rest_ok:
    logging.info(f'{get_identification_string(location_id, server_name)}, {timestamp}, saving to CSV and REST api (response {response}) ok.')

  return
