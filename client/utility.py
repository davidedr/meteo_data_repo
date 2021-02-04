import requests
from fake_useragent import UserAgent
from datetime import datetime
import logging
from lxml import html
import os
from csv import writer
import json

import definitions
import proxy_pool

#
#
#
def check_minimum_data(location_id, server_name, meteo_data_dict):
  timestamp_string=meteo_data_dict.get("timestamp_string")
  if not timestamp_string:
    return False

  found=False
  for col in  definitions.CSV_FILE_HEADER:
    if col=="timestamp_string" or col=="timestamp_string_date" or col=="timestamp_string_time":
      continue
    data=meteo_data_dict.get(col)
    if data is not None:
      found=True
      break
 
  if found:
    return True

  logging.info(f'{get_identification_string(location_id, server_name)}, No scraped data! Skip saving.')
  return False

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
      logging.info(f'{get_identification_string(location_id, server_name)}: Found in db. Update...')
      location_json=server["location"]
      response=requests.patch(f'http://localhost:8080/api/location/{location_id}', headers=headers, json=location_json)
      logging.info(f'Location id: {server["location_id"]}, name: {server["name"]}, PATCH location, response: {response}')

  else:
    logging.info(f'{get_identification_string(location_id, server_name)}: Not found in db. Adding...')
    location_json=server["location"]
    response=requests.post('http://localhost:8080/api/location', headers=headers, json=location_json)
    logging.info(f'Location id: {server["location_id"]}, name: {server["name"]}, POST location, response: {response}')

  ws_capabilities=server.get("ws_capabilities")
  if ws_capabilities is not None:
    ws_capabilities_response=requests.get(f'http://localhost:8080/api/ws_capabilities/location/{location_id}', headers=headers)
    if ws_capabilities_response.status_code==404:
      ws_capabilities_json=server["ws_capabilities"]
      response=requests.post(f'http://localhost:8080/api/ws_capabilities', headers=headers, json=ws_capabilities_json)
      logging.info(f'Location id: {server["location_id"]}, name: {server["name"]}, POST ws_capabilities, response: {response}')
    else:
      ws_capabilities_json=json.loads(ws_capabilities_response.text)
      if ws_capabilities_json and ws_capabilities_json[0] and ws_capabilities_json[0]["location_id"]==location_id:
        id=ws_capabilities_json[0]["id"]
        ws_capabilities_json=server["ws_capabilities"]
        response=requests.patch(f'http://localhost:8080/api/ws_capabilities/{id}', headers=headers, json=ws_capabilities_json)
        logging.info(f'Location id: {server["location_id"]}, name: {server["name"]}, PATCH ws_capabilities, response: {response}')

  return response
  
#
# Return an human-readable server identification string
#
def get_identification_string(location_id, server_name=None):

  if location_id:
    if server_name:
      return f'Server: {location_id}, {server_name}'
    else:
      return f'Server: {location_id}'
  else:
    if server_name:
      return f'Server: {server_name}'
    else:
      return ''

#
# Return an human-readable server identification string
#
def get_identification_string_with_date(location_id, server_name=None):

  timestamp_date_string=datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")
  if location_id:
    if server_name:
      return f'Server: {location_id}, {server_name}, {timestamp_date_string}'
    else:
      return f'Server: {location_id}, {timestamp_date_string}'
  else:
    if server_name:
      return f'Server: {server_name}, {timestamp_date_string}'
    else:
      return f'{timestamp_date_string}'

#
#
#
def find_server(location_id):
  for server in definitions.servers:
    if server["location_id"]==location_id:
      return server
  
  return None

#
#
#
def test_starter(location_id, log_level=logging.NOTSET):
  found_server=find_server(location_id)
  if found_server is None:
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
def convert_wind_direction_to_deg(wind_direction, location_id=None, server_name=None):

  if not wind_direction or wind_direction=="":
    logging.error(f'{get_identification_string(location_id, server_name)}: wind_direction is empty (f{wind_direction})!')
    return None

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
  else:
    logging.info(f'{get_identification_string(location_id, server_name)}, Unknown wind_direction: "{wind_direction}"!')

  return wind_direction_deg

#
# Get the web page and convert it to a DOM tree
#

# TODO: move to kind of an "abstract class"
def get_tree(weather_station_url, location_id, server_name=None):
  
  user_agent = UserAgent().random 
  headers = {'User-Agent': user_agent}

  try:
    proxy=proxy_pool.get_proxy(location_id, server_name)
    proxy=None
    if proxy is None:
      proxies=None
    else:
      proxies={ "http": proxy, "https": proxy }

    page = requests.get(weather_station_url, proxies=proxies, headers=headers)

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
# Routes to up-to-date saver
#
def save(location_id, server_name, meteo_data_dict, save=True):
  return _save_v14(location_id, server_name, meteo_data_dict, save)

#
# Save data to CSV file and REST API server
#
# TODO: move to kind of an "abstract class"
def _save_v14(location_id, server_name, meteo_data_dict, save=True):

  if not save:
    logging.info(f'{get_identification_string(location_id, server_name)}: Save disabled!')
    return

  timestamp_string=meteo_data_dict.get("timestamp_string")
  timestamp_string_date=meteo_data_dict.get("timestamp_string_date")
  timestamp_string_time=meteo_data_dict.get("timestamp_string_time")
  wind_speed_knots=meteo_data_dict.get("wind_speed_knots")
  wind_direction_deg=meteo_data_dict.get("wind_direction_deg")
  barometric_pressure_ssl_hPa=meteo_data_dict.get("barometric_pressure_ssl_hPa")
  rain_today_mm=meteo_data_dict.get("rain_today_mm")
  rain_rate_mmh=meteo_data_dict.get("rain_rate_mmh")
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
  perceived_temperature_cels=meteo_data_dict.get("perceived_temperature_cels")
  humidex_cels=meteo_data_dict.get("humidex_cels")
  wind_temperature_cels=meteo_data_dict.get("wind_temperature_cels")
  current_weather=meteo_data_dict.get("current_weather")
  wet_bulb_temperature_cels=meteo_data_dict.get("wet_bulb_temperature_cels")
  absolute_humidity_gm3=meteo_data_dict.get("absolute_humidity_gm3")
  saturated_vapor_pressure_hPa=meteo_data_dict.get("saturated_vapor_pressure_hPa")
  windrun_km=meteo_data_dict.get("windrun_km")
  barometric_pressure_wsl_hPa=meteo_data_dict.get("barometric_pressure_wsl_hPa")
  average_wind_speed_knots=meteo_data_dict.get("average_wind_speed_knots")
  storm_rain_mmm=meteo_data_dict.get("storm_rain_mmm")
  rain_in_last_storm_event_mm=meteo_data_dict.get("rain_in_last_storm_event_mm")
  cloud_height_m=meteo_data_dict.get("cloud_height_m")
  air_density_kgm3=meteo_data_dict.get("air_density_kgm3")
  rel_equilibrium_moisture_content=meteo_data_dict.get("rel_equilibrium_moisture_content")
  wind_force_beaufort_desc=meteo_data_dict.get("wind_force_beaufort_desc")
  moon_phase_desc=meteo_data_dict.get("moon_phase_desc")
  sunrise_timestamp=meteo_data_dict.get("sunrise_timestamp")
  sunset_timestamp=meteo_data_dict.get("sunset_timestamp")

  #
  # Saving to csv backup file and database server
  #

  # Header
  csv_file_header=definitions.CSV_FILE_HEADER

  # csv_file_header_temp=[]
  # for key in meteo_data_dict:
  #   csv_file_header_temp.append(str(key))

  save_to_csv_ok=True
  save_to_rest_ok=True
  file_name=f"data/weather_{location_id}_{server_name}_v14.txt"
  try:
    with open(file_name, 'a+', newline='') as write_obj:
      csv_writer = writer(write_obj, delimiter=";")
      if os.stat(file_name).st_size == 0:
        csv_writer.writerow(csv_file_header)

      weather=[
        timestamp_string, timestamp_string_date, timestamp_string_time, wind_speed_knots, wind_direction_deg, barometric_pressure_ssl_hPa,\
        rain_today_mm, rain_rate_mmh, temperature_cels, rel_humidity, uv_index, heat_index_cels, wind_gust_knots, dew_point_cels, wind_chill_cels,\
        ground_temperature_cels, solar_irradiance_wpsm, rel_leaf_wetness, soil_moisture_cb, rain_this_month_mm, rain_this_year_mm,\
        evapotranspiration_today_mm, evapotranspiration_this_month_mm, evapotranspiration_this_year_mm, perceived_temperature_cels, humidex_cels,
        wind_temperature_cels, current_weather, wet_bulb_temperature_cels, absolute_humidity_gm3, saturated_vapor_pressure_hPa, windrun_km,\
        barometric_pressure_wsl_hPa, average_wind_speed_knots, storm_rain_mmm, rain_in_last_storm_event_mm, cloud_height_m,
        air_density_kgm3, rel_equilibrium_moisture_content, wind_force_beaufort_desc, moon_phase_desc, sunrise_timestamp, sunset_timestamp
      ]
      csv_writer.writerow(weather)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} saving to csv file: {file_name}!')
    save_to_csv_ok=False

  # Insert into database

  # Convert to PGSQL format
  try:
    timestamp = datetime.strptime(timestamp_string, "%d/%m/%Y %H:%M:%S")

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} parsing: "{timestamp_string}"!')
    save_to_rest_ok=False
    return

  try:
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")+".000"

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} in timestamp.strftime for: "{timestamp}"!')
    save_to_rest_ok=False
    return

  data_json = {
    "location_id": location_id,   
    "timestamp_ws": timestamp,
    "wind_speed_knots": wind_speed_knots,
    "wind_direction_deg": wind_direction_deg,
    "barometric_pressure_ssl_hPa": barometric_pressure_ssl_hPa,
    "rain_today_mm": rain_today_mm,
    "rain_rate_mmh": rain_rate_mmh,
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
    "evapotranspiration_this_year_mm": evapotranspiration_this_year_mm,
    "perceived_temperature_cels": perceived_temperature_cels,
    "humidex_cels": humidex_cels,
    "wind_temperature_cels": wind_temperature_cels,
    "current_weather": current_weather,
    "wet_bulb_temperature_cels": wet_bulb_temperature_cels,
    "absolute_humidity_gm3": absolute_humidity_gm3,
    "saturated_vapor_pressure_hPa": saturated_vapor_pressure_hPa,
    "windrun_km": windrun_km,
    "barometric_pressure_wsl_hPa": barometric_pressure_wsl_hPa,
    "average_wind_speed_knots": average_wind_speed_knots,
    "storm_rain_mmm": storm_rain_mmm,
    "rain_in_last_storm_event_mm": rain_in_last_storm_event_mm,
    "cloud_height_m": cloud_height_m,
    "air_density_kgm3": air_density_kgm3,
    "rel_equilibrium_moisture_content": rel_equilibrium_moisture_content,
    "wind_force_beaufort_desc": wind_force_beaufort_desc,
    "moon_phase_desc": moon_phase_desc,
    "sunrise_timestamp": sunrise_timestamp,
    "sunset_timestamp": sunset_timestamp
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

#
# Save data to CSV file and REST API server
#
# TODO: move to kind of an "abstract class"
def _save_v13(location_id, server_name, meteo_data_dict, save=True):

  if not save:
    logging.info(f'{get_identification_string(location_id, server_name)}: Save disabled!')
    return

  timestamp_string=meteo_data_dict.get("timestamp_string")
  timestamp_string_date=meteo_data_dict.get("timestamp_string_date")
  timestamp_string_time=meteo_data_dict.get("timestamp_string_time")
  wind_speed_knots=meteo_data_dict.get("wind_speed_knots")
  wind_direction_deg=meteo_data_dict.get("wind_direction_deg")
  barometric_pressure_ssl_hPa=meteo_data_dict.get("barometric_pressure_ssl_hPa")
  rain_today_mm=meteo_data_dict.get("rain_today_mm")
  rain_rate_mmh=meteo_data_dict.get("rain_rate_mmh")
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
  perceived_temperature_cels=meteo_data_dict.get("perceived_temperature_cels")
  humidex_cels=meteo_data_dict.get("humidex_cels")
  wind_temperature_cels=meteo_data_dict.get("wind_temperature_cels")
  current_weather=meteo_data_dict.get("current_weather")
  wet_bulb_temperature_cels=meteo_data_dict.get("wet_bulb_temperature_cels")
  absolute_humidity_gm3=meteo_data_dict.get("absolute_humidity_gm3")
  saturated_vapor_pressure_hPa=meteo_data_dict.get("saturated_vapor_pressure_hPa")
  windrun_km=meteo_data_dict.get("windrun_km")
  barometric_pressure_wsl_hPa=meteo_data_dict.get("barometric_pressure_wsl_hPa")
  average_wind_speed_knots=meteo_data_dict.get("average_wind_speed_knots")
  storm_rain_mmm=meteo_data_dict.get("storm_rain_mmm")
  rain_in_last_storm_event_mm=meteo_data_dict.get("rain_in_last_storm_event_mm")
  cloud_height_m=meteo_data_dict.get("cloud_height_m")
  air_density_kgm3=meteo_data_dict.get("air_density_kgm3")
  rel_equilibrium_moisture_content=meteo_data_dict.get("rel_equilibrium_moisture_content")
  wind_force_beaufort_desc=meteo_data_dict.get("wind_force_beaufort_desc")

  #
  # Saving to csv backup file and database server
  #

  # Header
  csv_file_header=definitions.CSV_FILE_HEADER

  # csv_file_header_temp=[]
  # for key in meteo_data_dict:
  #   csv_file_header_temp.append(str(key))

  save_to_csv_ok=True
  save_to_rest_ok=True
  file_name=f"data/weather_{location_id}_{server_name}_v13.txt"
  try:
    with open(file_name, 'a+', newline='') as write_obj:
      csv_writer = writer(write_obj, delimiter=";")
      if os.stat(file_name).st_size == 0:
        csv_writer.writerow(csv_file_header)

      weather=[
        timestamp_string, timestamp_string_date, timestamp_string_time, wind_speed_knots, wind_direction_deg, barometric_pressure_ssl_hPa,\
        rain_today_mm, rain_rate_mmh, temperature_cels, rel_humidity, uv_index, heat_index_cels, wind_gust_knots, dew_point_cels, wind_chill_cels,\
        ground_temperature_cels, solar_irradiance_wpsm, rel_leaf_wetness, soil_moisture_cb, rain_this_month_mm, rain_this_year_mm,\
        evapotranspiration_today_mm, evapotranspiration_this_month_mm, evapotranspiration_this_year_mm, perceived_temperature_cels, humidex_cels,
        wind_temperature_cels, current_weather, wet_bulb_temperature_cels, absolute_humidity_gm3, saturated_vapor_pressure_hPa, windrun_km,\
        barometric_pressure_wsl_hPa, average_wind_speed_knots, storm_rain_mmm, rain_in_last_storm_event_mm, cloud_height_m,
        air_density_kgm3, rel_equilibrium_moisture_content, wind_force_beaufort_desc
      ]
      csv_writer.writerow(weather)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} saving to csv file: {file_name}!')
    save_to_csv_ok=False

  # Insert into database

  # Convert to PGSQL format
  try:
    timestamp = datetime.strptime(timestamp_string, "%d/%m/%Y %H:%M:%S")

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} parsing: "{timestamp_string}"!')
    save_to_rest_ok=False
    return

  try:
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")+".000"

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} in timestamp.strftime for: "{timestamp}"!')
    save_to_rest_ok=False
    return

  data_json = {
    "location_id": location_id,   
    "timestamp_ws": timestamp,
    "wind_speed_knots": wind_speed_knots,
    "wind_direction_deg": wind_direction_deg,
    "barometric_pressure_ssl_hPa": barometric_pressure_ssl_hPa,
    "rain_today_mm": rain_today_mm,
    "rain_rate_mmh": rain_rate_mmh,
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
    "evapotranspiration_this_year_mm": evapotranspiration_this_year_mm,
    "perceived_temperature_cels": perceived_temperature_cels,
    "humidex_cels": humidex_cels,
    "wind_temperature_cels": wind_temperature_cels,
    "current_weather": current_weather,
    "wet_bulb_temperature_cels": wet_bulb_temperature_cels,
    "absolute_humidity_gm3": absolute_humidity_gm3,
    "saturated_vapor_pressure_hPa": saturated_vapor_pressure_hPa,
    "windrun_km": windrun_km,
    "barometric_pressure_wsl_hPa": barometric_pressure_wsl_hPa,
    "average_wind_speed_knots": average_wind_speed_knots,
    "storm_rain_mmm": storm_rain_mmm,
    "rain_in_last_storm_event_mm": rain_in_last_storm_event_mm,
    "cloud_height_m": cloud_height_m,
    "air_density_kgm3": air_density_kgm3,
    "rel_equilibrium_moisture_content": rel_equilibrium_moisture_content,
    "wind_force_beaufort_desc": wind_force_beaufort_desc
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

#
# Save data to CSV file and REST API server
#
# TODO: move to kind of an "abstract class"
def _save_v12(location_id, server_name, meteo_data_dict, save=True):

  if not save:
    logging.info(f'{get_identification_string(location_id, server_name)}: Save disabled!')
    return

  timestamp_string=meteo_data_dict.get("timestamp_string")
  timestamp_string_date=meteo_data_dict.get("timestamp_string_date")
  timestamp_string_time=meteo_data_dict.get("timestamp_string_time")
  wind_speed_knots=meteo_data_dict.get("wind_speed_knots")
  wind_direction_deg=meteo_data_dict.get("wind_direction_deg")
  barometric_pressure_ssl_hPa=meteo_data_dict.get("barometric_pressure_ssl_hPa")
  rain_today_mm=meteo_data_dict.get("rain_today_mm")
  rain_rate_mmh=meteo_data_dict.get("rain_rate_mmh")
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
  perceived_temperature_cels=meteo_data_dict.get("perceived_temperature_cels")
  humidex_cels=meteo_data_dict.get("humidex_cels")
  wind_temperature_cels=meteo_data_dict.get("wind_temperature_cels")
  current_weather=meteo_data_dict.get("current_weather")
  wet_bulb_temperature_cels=meteo_data_dict.get("wet_bulb_temperature_cels")
  absolute_humidity_gm3=meteo_data_dict.get("absolute_humidity_gm3")
  saturated_vapor_pressure_hPa=meteo_data_dict.get("saturated_vapor_pressure_hPa")
  windrun_km=meteo_data_dict.get("windrun_km")
  barometric_pressure_wsl_hPa=meteo_data_dict.get("barometric_pressure_wsl_hPa")
  average_wind_speed_knots=meteo_data_dict.get("average_wind_speed_knots")
  storm_rain_mmm=meteo_data_dict.get("storm_rain_mmm")
  rain_in_last_storm_event_mm=meteo_data_dict.get("rain_in_last_storm_event_mm")
  cloud_height_m=meteo_data_dict.get("cloud_height_m")
  air_density_kgm3=meteo_data_dict.get("air_density_kgm3")
  rel_equilibrium_moisture_content=meteo_data_dict.get("rel_equilibrium_moisture_content")

  #
  # Saving to csv backup file and database server
  #

  # Header
  csv_file_header=definitions.CSV_FILE_HEADER

  # csv_file_header_temp=[]
  # for key in meteo_data_dict:
  #   csv_file_header_temp.append(str(key))

  save_to_csv_ok=True
  save_to_rest_ok=True
  file_name=f"data/weather_{location_id}_{server_name}_v12.txt"
  try:
    with open(file_name, 'a+', newline='') as write_obj:
      csv_writer = writer(write_obj, delimiter=";")
      if os.stat(file_name).st_size == 0:
        csv_writer.writerow(csv_file_header)

      weather=[
        timestamp_string, timestamp_string_date, timestamp_string_time, wind_speed_knots, wind_direction_deg, barometric_pressure_ssl_hPa,\
        rain_today_mm, rain_rate_mmh, temperature_cels, rel_humidity, uv_index, heat_index_cels, wind_gust_knots, dew_point_cels, wind_chill_cels,\
        ground_temperature_cels, solar_irradiance_wpsm, rel_leaf_wetness, soil_moisture_cb, rain_this_month_mm, rain_this_year_mm,\
        evapotranspiration_today_mm, evapotranspiration_this_month_mm, evapotranspiration_this_year_mm, perceived_temperature_cels, humidex_cels,
        wind_temperature_cels, current_weather, wet_bulb_temperature_cels, absolute_humidity_gm3, saturated_vapor_pressure_hPa, windrun_km,\
        barometric_pressure_wsl_hPa, average_wind_speed_knots, storm_rain_mmm, rain_in_last_storm_event_mm, cloud_height_m,
        air_density_kgm3, rel_equilibrium_moisture_content
      ]
      csv_writer.writerow(weather)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} saving to csv file: {file_name}!')
    save_to_csv_ok=False

  # Insert into database

  # Convert to PGSQL format
  try:
    timestamp = datetime.strptime(timestamp_string, "%d/%m/%Y %H:%M:%S")

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} parsing: "{timestamp_string}"!')
    save_to_rest_ok=False
    return

  try:
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")+".000"

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} in timestamp.strftime for: "{timestamp}"!')
    save_to_rest_ok=False
    return

  data_json = {
    "location_id": location_id,   
    "timestamp_ws": timestamp,
    "wind_speed_knots": wind_speed_knots,
    "wind_direction_deg": wind_direction_deg,
    "barometric_pressure_ssl_hPa": barometric_pressure_ssl_hPa,
    "rain_today_mm": rain_today_mm,
    "rain_rate_mmh": rain_rate_mmh,
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
    "evapotranspiration_this_year_mm": evapotranspiration_this_year_mm,
    "perceived_temperature_cels": perceived_temperature_cels,
    "humidex_cels": humidex_cels,
    "wind_temperature_cels": wind_temperature_cels,
    "current_weather": current_weather,
    "wet_bulb_temperature_cels": wet_bulb_temperature_cels,
    "absolute_humidity_gm3": absolute_humidity_gm3,
    "saturated_vapor_pressure_hPa": saturated_vapor_pressure_hPa,
    "windrun_km": windrun_km,
    "barometric_pressure_wsl_hPa": barometric_pressure_wsl_hPa,
    "average_wind_speed_knots": average_wind_speed_knots,
    "storm_rain_mmm": storm_rain_mmm,
    "rain_in_last_storm_event_mm": rain_in_last_storm_event_mm,
    "cloud_height_m": cloud_height_m,
    "air_density_kgm3": air_density_kgm3,
    "rel_equilibrium_moisture_content": rel_equilibrium_moisture_content
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

#
# Save data to CSV file and REST API server
#
# TODO: move to kind of an "abstract class"
def _save_v11(location_id, server_name, meteo_data_dict, save=True):

  if not save:
    logging.info(f'{get_identification_string(location_id, server_name)}: Save disabled!')
    return

  timestamp_string=meteo_data_dict.get("timestamp_string")
  timestamp_string_date=meteo_data_dict.get("timestamp_string_date")
  timestamp_string_time=meteo_data_dict.get("timestamp_string_time")
  wind_speed_knots=meteo_data_dict.get("wind_speed_knots")
  wind_direction_deg=meteo_data_dict.get("wind_direction_deg")
  barometric_pressure_ssl_hPa=meteo_data_dict.get("barometric_pressure_ssl_hPa")
  rain_today_mm=meteo_data_dict.get("rain_today_mm")
  rain_rate_mmh=meteo_data_dict.get("rain_rate_mmh")
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
  perceived_temperature_cels=meteo_data_dict.get("perceived_temperature_cels")
  humidex_cels=meteo_data_dict.get("humidex_cels")
  wind_temperature_cels=meteo_data_dict.get("wind_temperature_cels")
  current_weather=meteo_data_dict.get("current_weather")
  wet_bulb_temperature_cels=meteo_data_dict.get("wet_bulb_temperature_cels")
  absolute_humidity_gm3=meteo_data_dict.get("absolute_humidity_gm3")
  saturated_vapor_pressure_hPa=meteo_data_dict.get("saturated_vapor_pressure_hPa")
  windrun_km=meteo_data_dict.get("windrun_km")
  barometric_pressure_wsl_hPa=meteo_data_dict.get("barometric_pressure_wsl_hPa")
  average_wind_speed_knots=meteo_data_dict.get("average_wind_speed_knots")
  storm_rain_mmm=meteo_data_dict.get("storm_rain_mmm")
  rain_in_last_storm_event_mm=meteo_data_dict.get("rain_in_last_storm_event_mm")
  cloud_height_m=meteo_data_dict.get("cloud_height_m")
    
  #
  # Saving to csv backup file and database server
  #

  # Header
  csv_file_header=[
    "timestamp_string", "timestamp_string_date", "timestamp_string_time", "wind_speed_knots", "wind_direction_deg",
    "barometric_pressure_ssl_hPa", "rain_today_mm", "rain_rate_mmh", "temperature_cels", "rel_humidity", "uv_index",
    "heat_index_cels", "wind_gust_knots", "dew_point_cels", "wind_chill_cels", "ground_temperature_cels", "solar_irradiance_wpsm",
    "rel_leaf_wetness", "soil_moisture_cb", "rain_this_month_mm", "rain_this_year_mm", "evapotranspiration_today_mm",
    "evapotranspiration_this_month_mm", "evapotranspiration_this_year_mm", "perceived_temperature_cels", "humidex_cels",
    "wind_temperature_cels", "current_weather", "wet_bulb_temperature_cels", "absolute_humidity_gm3", "saturated_vapor_pressure_hPa",
    "windrun_km", "barometric_pressure_wsl_hPa", "average_wind_speed_knots", "storm_rain_mmm, rain_in_last_storm_event_mm", "cloud_height_m"
  ]

  # csv_file_header_temp=[]
  # for key in meteo_data_dict:
  #   csv_file_header_temp.append(str(key))

  save_to_csv_ok=True
  save_to_rest_ok=True
  file_name=f"data/weather_{location_id}_{server_name}_v11.txt"
  try:
    with open(file_name, 'a+', newline='') as write_obj:
      csv_writer = writer(write_obj, delimiter=";")
      if os.stat(file_name).st_size == 0:
        csv_writer.writerow(csv_file_header)

      weather=[
        timestamp_string, timestamp_string_date, timestamp_string_time, wind_speed_knots, wind_direction_deg, barometric_pressure_ssl_hPa,\
        rain_today_mm, rain_rate_mmh, temperature_cels, rel_humidity, uv_index, heat_index_cels, wind_gust_knots, dew_point_cels, wind_chill_cels,\
        ground_temperature_cels, solar_irradiance_wpsm, rel_leaf_wetness, soil_moisture_cb, rain_this_month_mm, rain_this_year_mm,\
        evapotranspiration_today_mm, evapotranspiration_this_month_mm, evapotranspiration_this_year_mm, perceived_temperature_cels, humidex_cels,
        wind_temperature_cels, current_weather, wet_bulb_temperature_cels, absolute_humidity_gm3, saturated_vapor_pressure_hPa, windrun_km,\
        barometric_pressure_wsl_hPa, average_wind_speed_knots, storm_rain_mmm, rain_in_last_storm_event_mm, cloud_height_m
      ]
      csv_writer.writerow(weather)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} saving to csv file: {file_name}!')
    save_to_csv_ok=False

  # Insert into database

  # Convert to PGSQL format
  try:
    timestamp = datetime.strptime(timestamp_string, "%d/%m/%Y %H:%M:%S")

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} parsing: "{timestamp_string}"!')
    save_to_rest_ok=False
    return

  try:
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")+".000"

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} in timestamp.strftime for: "{timestamp}"!')
    save_to_rest_ok=False
    return

  data_json = {
    "location_id": location_id,   
    "timestamp_ws": timestamp,
    "wind_speed_knots": wind_speed_knots,
    "wind_direction_deg": wind_direction_deg,
    "barometric_pressure_ssl_hPa": barometric_pressure_ssl_hPa,
    "rain_today_mm": rain_today_mm,
    "rain_rate_mmh": rain_rate_mmh,
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
    "evapotranspiration_this_year_mm": evapotranspiration_this_year_mm,
    "perceived_temperature_cels": perceived_temperature_cels,
    "humidex_cels": humidex_cels,
    "wind_temperature_cels": wind_temperature_cels,
    "current_weather": current_weather,
    "wet_bulb_temperature_cels": wet_bulb_temperature_cels,
    "absolute_humidity_gm3": absolute_humidity_gm3,
    "saturated_vapor_pressure_hPa": saturated_vapor_pressure_hPa,
    "windrun_km": windrun_km,
    "barometric_pressure_wsl_hPa": barometric_pressure_wsl_hPa,
    "average_wind_speed_knots": average_wind_speed_knots,
    "storm_rain_mmm": storm_rain_mmm,
    "rain_in_last_storm_event_mm": rain_in_last_storm_event_mm,
    "cloud_height_m": cloud_height_m    
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

#
# Save data to CSV file and REST API server
#
# TODO: move to kind of an "abstract class"
def _save_v10(location_id, server_name, meteo_data_dict, save=True):

  if not save:
    logging.info(f'{get_identification_string(location_id, server_name)}: Save disabled!')
    return

  timestamp_string=meteo_data_dict.get("timestamp_string")
  timestamp_string_date=meteo_data_dict.get("timestamp_string_date")
  timestamp_string_time=meteo_data_dict.get("timestamp_string_time")
  wind_speed_knots=meteo_data_dict.get("wind_speed_knots")
  wind_direction_deg=meteo_data_dict.get("wind_direction_deg")
  barometric_pressure_ssl_hPa=meteo_data_dict.get("barometric_pressure_ssl_hPa")
  rain_today_mm=meteo_data_dict.get("rain_today_mm")
  rain_rate_mmh=meteo_data_dict.get("rain_rate_mmh")
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
  perceived_temperature_cels=meteo_data_dict.get("perceived_temperature_cels")
  humidex_cels=meteo_data_dict.get("humidex_cels")
  wind_temperature_cels=meteo_data_dict.get("wind_temperature_cels")
  current_weather=meteo_data_dict.get("current_weather")
  wet_bulb_temperature_cels=meteo_data_dict.get("wet_bulb_temperature_cels")
  absolute_humidity_gm3=meteo_data_dict.get("absolute_humidity_gm3")
  saturated_vapor_pressure_hPa=meteo_data_dict.get("saturated_vapor_pressure_hPa")
  windrun_km=meteo_data_dict.get("windrun_km")
  barometric_pressure_wsl_hPa=meteo_data_dict.get("barometric_pressure_wsl_hPa")
  average_wind_speed_knots=meteo_data_dict.get("average_wind_speed_knots")
  storm_rain_mmm=meteo_data_dict.get("storm_rain_mmm")
  rain_in_last_storm_event_mm=meteo_data_dict.get("rain_in_last_storm_event_mm")
    
  #
  # Saving to csv backup file and database server
  #

  # Header
  csv_file_header=[
    "timestamp_string", "timestamp_string_date", "timestamp_string_time", "wind_speed_knots", "wind_direction_deg",
    "barometric_pressure_ssl_hPa", "rain_today_mm", "rain_rate_mmh", "temperature_cels", "rel_humidity", "uv_index",
    "heat_index_cels", "wind_gust_knots", "dew_point_cels", "wind_chill_cels", "ground_temperature_cels", "solar_irradiance_wpsm",
    "rel_leaf_wetness", "soil_moisture_cb", "rain_this_month_mm", "rain_this_year_mm", "evapotranspiration_today_mm",
    "evapotranspiration_this_month_mm", "evapotranspiration_this_year_mm", "perceived_temperature_cels", "humidex_cels",
    "wind_temperature_cels", "current_weather", "wet_bulb_temperature_cels", "absolute_humidity_gm3", "saturated_vapor_pressure_hPa",
    "windrun_km", "barometric_pressure_wsl_hPa", "average_wind_speed_knots", "storm_rain_mmm, rain_in_last_storm_event_mm"
  ]

  # csv_file_header_temp=[]
  # for key in meteo_data_dict:
  #   csv_file_header_temp.append(str(key))

  save_to_csv_ok=True
  save_to_rest_ok=True
  file_name=f"data/weather_{location_id}_{server_name}_v10.txt"
  try:
    with open(file_name, 'a+', newline='') as write_obj:
      csv_writer = writer(write_obj, delimiter=";")
      if os.stat(file_name).st_size == 0:
        csv_writer.writerow(csv_file_header)

      weather=[
        timestamp_string, timestamp_string_date, timestamp_string_time, wind_speed_knots, wind_direction_deg, barometric_pressure_ssl_hPa,\
        rain_today_mm, rain_rate_mmh, temperature_cels, rel_humidity, uv_index, heat_index_cels, wind_gust_knots, dew_point_cels, wind_chill_cels,\
        ground_temperature_cels, solar_irradiance_wpsm, rel_leaf_wetness, soil_moisture_cb, rain_this_month_mm, rain_this_year_mm,\
        evapotranspiration_today_mm, evapotranspiration_this_month_mm, evapotranspiration_this_year_mm, perceived_temperature_cels, humidex_cels,
        wind_temperature_cels, current_weather, wet_bulb_temperature_cels, absolute_humidity_gm3, saturated_vapor_pressure_hPa, windrun_km,\
        barometric_pressure_wsl_hPa, average_wind_speed_knots, storm_rain_mmm, rain_in_last_storm_event_mm
      ]
      csv_writer.writerow(weather)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} saving to csv file: {file_name}!')
    save_to_csv_ok=False

  # Insert into database

  # Convert to PGSQL format
  try:
    timestamp = datetime.strptime(timestamp_string, "%d/%m/%Y %H:%M:%S")

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} parsing: "{timestamp_string}"!')
    save_to_rest_ok=False
    return

  try:
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")+".000"

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} in timestamp.strftime for: "{timestamp}"!')
    save_to_rest_ok=False
    return

  data_json = {
    "location_id": location_id,   
    "timestamp_ws": timestamp,
    "wind_speed_knots": wind_speed_knots,
    "wind_direction_deg": wind_direction_deg,
    "barometric_pressure_ssl_hPa": barometric_pressure_ssl_hPa,
    "rain_today_mm": rain_today_mm,
    "rain_rate_mmh": rain_rate_mmh,
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
    "evapotranspiration_this_year_mm": evapotranspiration_this_year_mm,
    "perceived_temperature_cels": perceived_temperature_cels,
    "humidex_cels": humidex_cels,
    "wind_temperature_cels": wind_temperature_cels,
    "current_weather": current_weather,
    "wet_bulb_temperature_cels": wet_bulb_temperature_cels,
    "absolute_humidity_gm3": absolute_humidity_gm3,
    "saturated_vapor_pressure_hPa": saturated_vapor_pressure_hPa,
    "windrun_km": windrun_km,
    "barometric_pressure_wsl_hPa": barometric_pressure_wsl_hPa,
    "average_wind_speed_knots": average_wind_speed_knots,
    "storm_rain_mmm": storm_rain_mmm,
    "rain_in_last_storm_event_mm": rain_in_last_storm_event_mm
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

#
# Save data to CSV file and REST API server
#
# TODO: move to kind of an "abstract class"
def _save_v9(location_id, server_name, meteo_data_dict, save=True):

  if not save:
    logging.info(f'{get_identification_string(location_id, server_name)}: Save disabled!')
    return

  timestamp_string=meteo_data_dict.get("timestamp_string")
  timestamp_string_date=meteo_data_dict.get("timestamp_string_date")
  timestamp_string_time=meteo_data_dict.get("timestamp_string_time")
  wind_speed_knots=meteo_data_dict.get("wind_speed_knots")
  wind_direction_deg=meteo_data_dict.get("wind_direction_deg")
  barometric_pressure_ssl_hPa=meteo_data_dict.get("barometric_pressure_ssl_hPa")
  rain_today_mm=meteo_data_dict.get("rain_today_mm")
  rain_rate_mmh=meteo_data_dict.get("rain_rate_mmh")
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
  perceived_temperature_cels=meteo_data_dict.get("perceived_temperature_cels")
  humidex_cels=meteo_data_dict.get("humidex_cels")
  wind_temperature_cels=meteo_data_dict.get("wind_temperature_cels")
  current_weather=meteo_data_dict.get("current_weather")
  wet_bulb_temperature_cels=meteo_data_dict.get("wet_bulb_temperature_cels")
  absolute_humidity_gm3=meteo_data_dict.get("absolute_humidity_gm3")
  saturated_vapor_pressure_hPa=meteo_data_dict.get("saturated_vapor_pressure_hPa")
  windrun_km=meteo_data_dict.get("windrun_km")
  barometric_pressure_wsl_hPa=meteo_data_dict.get("barometric_pressure_wsl_hPa")
  average_wind_speed_knots=meteo_data_dict.get("average_wind_speed_knots")
  storm_rain_mmm=meteo_data_dict.get("storm_rain_mmm")
  
  #
  # Saving to csv backup file and database server
  #

  # Header
  csv_file_header=[
    "timestamp_string", "timestamp_string_date", "timestamp_string_time", "wind_speed_knots", "wind_direction_deg",
    "barometric_pressure_ssl_hPa", "rain_today_mm", "rain_rate_mmh", "temperature_cels", "rel_humidity", "uv_index",
    "heat_index_cels", "wind_gust_knots", "dew_point_cels", "wind_chill_cels", "ground_temperature_cels", "solar_irradiance_wpsm",
    "rel_leaf_wetness", "soil_moisture_cb", "rain_this_month_mm", "rain_this_year_mm", "evapotranspiration_today_mm",
    "evapotranspiration_this_month_mm", "evapotranspiration_this_year_mm", "perceived_temperature_cels", "humidex_cels",
    "wind_temperature_cels", "current_weather", "wet_bulb_temperature_cels", "absolute_humidity_gm3", "saturated_vapor_pressure_hPa",
    "windrun_km", "barometric_pressure_wsl_hPa", "average_wind_speed_knots", "storm_rain_mmm"
  ]

  # csv_file_header_temp=[]
  # for key in meteo_data_dict:
  #   csv_file_header_temp.append(str(key))

  save_to_csv_ok=True
  save_to_rest_ok=True
  file_name=f"data/weather_{location_id}_{server_name}_v9.txt"
  try:
    with open(file_name, 'a+', newline='') as write_obj:
      csv_writer = writer(write_obj, delimiter=";")
      if os.stat(file_name).st_size == 0:
        csv_writer.writerow(csv_file_header)

      weather=[
        timestamp_string, timestamp_string_date, timestamp_string_time, wind_speed_knots, wind_direction_deg, barometric_pressure_ssl_hPa,\
        rain_today_mm, rain_rate_mmh, temperature_cels, rel_humidity, uv_index, heat_index_cels, wind_gust_knots, dew_point_cels, wind_chill_cels,\
        ground_temperature_cels, solar_irradiance_wpsm, rel_leaf_wetness, soil_moisture_cb, rain_this_month_mm, rain_this_year_mm,\
        evapotranspiration_today_mm, evapotranspiration_this_month_mm, evapotranspiration_this_year_mm, perceived_temperature_cels, humidex_cels,
        wind_temperature_cels, current_weather, wet_bulb_temperature_cels, absolute_humidity_gm3, saturated_vapor_pressure_hPa, windrun_km,\
        barometric_pressure_wsl_hPa, average_wind_speed_knots, storm_rain_mmm
      ]
      csv_writer.writerow(weather)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} saving to csv file: {file_name}!')
    save_to_csv_ok=False

  # Insert into database

  # Convert to PGSQL format
  try:
    timestamp = datetime.strptime(timestamp_string, "%d/%m/%Y %H:%M:%S")

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} parsing: "{timestamp_string}"!')
    save_to_rest_ok=False
    return

  try:
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")+".000"

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} in timestamp.strftime for: "{timestamp}"!')
    save_to_rest_ok=False
    return

  data_json = {
    "location_id": location_id,   
    "timestamp_ws": timestamp,
    "wind_speed_knots": wind_speed_knots,
    "wind_direction_deg": wind_direction_deg,
    "barometric_pressure_ssl_hPa": barometric_pressure_ssl_hPa,
    "rain_today_mm": rain_today_mm,
    "rain_rate_mmh": rain_rate_mmh,
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
    "evapotranspiration_this_year_mm": evapotranspiration_this_year_mm,
    "perceived_temperature_cels": perceived_temperature_cels,
    "humidex_cels": humidex_cels,
    "wind_temperature_cels": wind_temperature_cels,
    "current_weather": current_weather,
    "wet_bulb_temperature_cels": wet_bulb_temperature_cels,
    "absolute_humidity_gm3": absolute_humidity_gm3,
    "saturated_vapor_pressure_hPa": saturated_vapor_pressure_hPa,
    "windrun_km": windrun_km,
    "barometric_pressure_wsl_hPa": barometric_pressure_wsl_hPa,
    "average_wind_speed_knots": average_wind_speed_knots,
    "storm_rain_mmm": storm_rain_mmm
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

#
# Save data to CSV file and REST API server
#
# TODO: move to kind of an "abstract class"
def _save_v8(location_id, server_name, meteo_data_dict, save=True):

  if not save:
    logging.info(f'{get_identification_string(location_id, server_name)}: Save disabled!')
    return

  timestamp_string=meteo_data_dict.get("timestamp_string")
  timestamp_string_date=meteo_data_dict.get("timestamp_string_date")
  timestamp_string_time=meteo_data_dict.get("timestamp_string_time")
  wind_speed_knots=meteo_data_dict.get("wind_speed_knots")
  wind_direction_deg=meteo_data_dict.get("wind_direction_deg")
  barometric_pressure_ssl_hPa=meteo_data_dict.get("barometric_pressure_ssl_hPa")
  rain_today_mm=meteo_data_dict.get("rain_today_mm")
  rain_rate_mmh=meteo_data_dict.get("rain_rate_mmh")
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
  perceived_temperature_cels=meteo_data_dict.get("perceived_temperature_cels")
  humidex_cels=meteo_data_dict.get("humidex_cels")
  wind_temperature_cels=meteo_data_dict.get("wind_temperature_cels")
  current_weather=meteo_data_dict.get("current_weather")
  wet_bulb_temperature_cels=meteo_data_dict.get("wet_bulb_temperature_cels")
  absolute_humidity_gm3=meteo_data_dict.get("absolute_humidity_gm3")
  saturated_vapor_pressure_hPa=meteo_data_dict.get("saturated_vapor_pressure_hPa")
  windrun_km=meteo_data_dict.get("windrun_km")
  barometric_pressure_wsl_hPa=meteo_data_dict.get("barometric_pressure_wsl_hPa")
  average_wind_speed_knots=meteo_data_dict.get("average_wind_speed_knots")

  #
  # Saving to csv backup file and database server
  #

  # Header
  csv_file_header=[
    "timestamp_string", "timestamp_string_date", "timestamp_string_time", "wind_speed_knots", "wind_direction_deg",
    "barometric_pressure_ssl_hPa", "rain_today_mm", "rain_rate_mmh", "temperature_cels", "rel_humidity", "uv_index",
    "heat_index_cels", "wind_gust_knots", "dew_point_cels", "wind_chill_cels", "ground_temperature_cels", "solar_irradiance_wpsm",
    "rel_leaf_wetness", "soil_moisture_cb", "rain_this_month_mm", "rain_this_year_mm", "evapotranspiration_today_mm",
    "evapotranspiration_this_month_mm", "evapotranspiration_this_year_mm", "perceived_temperature_cels", "humidex_cels",
    "wind_temperature_cels", "current_weather", "wet_bulb_temperature_cels", "absolute_humidity_gm3", "saturated_vapor_pressure_hPa",
    "windrun_km", "barometric_pressure_wsl_hPa", "average_wind_speed_knots"
  ]

  # csv_file_header_temp=[]
  # for key in meteo_data_dict:
  #   csv_file_header_temp.append(str(key))

  save_to_csv_ok=True
  save_to_rest_ok=True
  file_name=f"data/weather_{location_id}_{server_name}_v8.txt"
  try:
    with open(file_name, 'a+', newline='') as write_obj:
      csv_writer = writer(write_obj, delimiter=";")
      if os.stat(file_name).st_size == 0:
        csv_writer.writerow(csv_file_header)

      weather=[
        timestamp_string, timestamp_string_date, timestamp_string_time, wind_speed_knots, wind_direction_deg, barometric_pressure_ssl_hPa,\
        rain_today_mm, rain_rate_mmh, temperature_cels, rel_humidity, uv_index, heat_index_cels, wind_gust_knots, dew_point_cels, wind_chill_cels,\
        ground_temperature_cels, solar_irradiance_wpsm, rel_leaf_wetness, soil_moisture_cb, rain_this_month_mm, rain_this_year_mm,\
        evapotranspiration_today_mm, evapotranspiration_this_month_mm, evapotranspiration_this_year_mm, perceived_temperature_cels, humidex_cels,
        wind_temperature_cels, current_weather, wet_bulb_temperature_cels, absolute_humidity_gm3, saturated_vapor_pressure_hPa, windrun_km,\
        barometric_pressure_wsl_hPa, average_wind_speed_knots
      ]
      csv_writer.writerow(weather)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} saving to csv file: {file_name}!')
    save_to_csv_ok=False

  # Insert into database

  # Convert to PGSQL format
  try:
    timestamp = datetime.strptime(timestamp_string, "%d/%m/%Y %H:%M:%S")

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} parsing: "{timestamp_string}"!')
    save_to_rest_ok=False
    return

  try:
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")+".000"

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} in timestamp.strftime for: "{timestamp}"!')
    save_to_rest_ok=False
    return

  data_json = {
    "location_id": location_id,   
    "timestamp_ws": timestamp,
    "wind_speed_knots": wind_speed_knots,
    "wind_direction_deg": wind_direction_deg,
    "barometric_pressure_ssl_hPa": barometric_pressure_ssl_hPa,
    "rain_today_mm": rain_today_mm,
    "rain_rate_mmh": rain_rate_mmh,
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
    "evapotranspiration_this_year_mm": evapotranspiration_this_year_mm,
    "perceived_temperature_cels": perceived_temperature_cels,
    "humidex_cels": humidex_cels,
    "wind_temperature_cels": wind_temperature_cels,
    "current_weather": current_weather,
    "wet_bulb_temperature_cels": wet_bulb_temperature_cels,
    "absolute_humidity_gm3": absolute_humidity_gm3,
    "saturated_vapor_pressure_hPa": saturated_vapor_pressure_hPa,
    "windrun_km": windrun_km,
    "barometric_pressure_wsl_hPa": barometric_pressure_wsl_hPa,
    "average_wind_speed_knots": average_wind_speed_knots
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

#
#
#
def _save_v6(location_id, server_name, meteo_data_dict, save=True):

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
  csv_file_header=["timestamp_string", "timestamp_string_date", "timestamp_string_time", "wind_speed_knots", "wind_direction_deg", "barometric_pressure_ssl_hPa", "rain_today_mm", "rain_rate_mmh", "temperature_cels", "rel_humidity", "uv_index", "heat_index_cels", "wind_gust_knots", "dew_point_cels", "wind_chill_cels", "ground_temperature_cels", "solar_irradiance_wpsm", "rel_leaf_wetness", "soil_moisture_cb", "rain_this_month_mm", "rain_this_year_mm", "evapotranspiration_today_mm", "evapotranspiration_this_month_mm", "evapotranspiration_this_year_mm"]

  # csv_file_header_temp=[]
  # for key in meteo_data_dict:
  #   csv_file_header_temp.append(str(key))

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
  try:
    timestamp = datetime.strptime(timestamp_string, "%d/%m/%Y %H:%M:%S")

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} parsing: "{timestamp_string}"!')
    save_to_rest_ok=False
    return

  try:
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")+".000"

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} in timestamp.strftime for: "{timestamp}"!')
    save_to_rest_ok=False
    return

  data_json = {
    "location_id": location_id,   
    "timestamp_ws": timestamp,
    "wind_speed_knots": wind_speed_knots,
    "wind_direction_deg": wind_direction_deg,
    "barometric_pressure_ssl_hPa": barometric_pressure_hPa,
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
