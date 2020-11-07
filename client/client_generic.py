import requests
import csv
from datetime import datetime
from lxml import html
import requests
from fake_useragent import UserAgent
import os
from csv import writer
import logging
import threading
import time

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
# Return an humen-readable server identification string
#
def get_identification_string(location_id, server_name=None):
  if server_name:
    return f'Server: {location_id}, {server_name}'
  else:
    return f'Server: {location_id}'

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
    response=requests.post(rest_server, headers = headers, json = data_json)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}: exception: {e} POSTing to: {rest_server}!')
    save_to_rest_ok=False

  if save_to_csv_ok and save_to_rest_ok:
    logging.info(f'{get_identification_string(location_id, server_name)}, {timestamp}, saving to CSV and REST api (response {response}) ok.')

  return

#
#
#
def scan_meteosystem_alike(last_seen_timestamp, server, save=True, log=True):

  location_id=server["location_id"]
  server_name=server["name"]
  weather_station_url=server["url"]

  tree, _ =get_tree(weather_station_url, location_id)
  if tree is None:
    return last_seen_timestamp

  try:
    date_list = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > div.valori3 > strong:nth-child(1)")
    date_string=date_list[0].text.strip()

    time_list = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > div.valori3 > strong:nth-child(2)")
    time_string=time_list[0].text.strip()

    datetime_string=date_string+" "+time_string
    timestamp_obj=datetime.strptime(datetime_string, "%d/%m/%y %H.%M")
    timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
    timestamp_string_date=timestamp_obj.strftime("%d/%m/%Y")
    timestamp_string_time=timestamp_obj.strftime("%H:%M:%S")

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting the timestamp: "{e}"!')
    return last_seen_timestamp

  if timestamp_string==last_seen_timestamp:
    # Weather station is not updating data
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, last_seen_timestamp: {last_seen_timestamp}, skip saving!')
    # TODO Raise an alert
    return last_seen_timestamp

  wind_speed_knots_elem=None
  try:
    wind_speed_knots_elem = tree.xpath("/html/body/div/div[4]/table/tr/td[2]/table[1]/tr[2]/td/table/tr[17]/td[3]/div/strong")
    wind_speed_knots=wind_speed_knots_elem[0].text.strip()
    wind_speed_knots=wind_speed_knots.split(" ")[0].strip()
    wind_speed_knots=float(wind_speed_knots)/1.852

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

  wind_gust_knots=None
  try:
    wind_gust_kmh_ele=tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(17) > td.sfondotagmax > div > strong")
    wind_gust_kmh=wind_gust_kmh_ele[0].text.split(" ")[0].strip()
    wind_gust_knots=float(wind_gust_kmh)/1.852
      
  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_gust_knots: "{e}"!')

  wind_direction_deg=None
  try:  
    wind_direction_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(18) > td:nth-child(3) > div > strong")
    wind_direction=wind_direction_ele[0].text

    wind_direction_deg=convert_wind_direction_to_deg(wind_direction)
    if not wind_direction_deg:
      logging.info(f'{get_identification_string(location_id, server_name)}, Unknown wind_direction: "{wind_direction}"!')

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  barometric_pressure_hPa=None
  try:
    barometric_pressure_hPa_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(7) > td:nth-child(3) > div > strong')
    barometric_pressure_hPa=float(barometric_pressure_hPa_ele[0].text.split(' ')[0].strip())

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting barometric_pressure_hPa: "{e}"!')

  rain_today_mm=None
  try:
    rain_today_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(21) > td.sfondotagmin > div > strong")
    rain_today_mm=float(rain_today_mm_ele[0].text.split(' ')[0].strip())

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  rain_rate_mmph=None
  try:
    rain_rate_mmph_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(21) > td:nth-child(3) > div > strong")
    rain_rate_mmph=float(rain_rate_mmph_ele[0].text.split(' ')[0].strip())

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_rate_mmph: "{e}"!')

  temperature_cels=None
  try:
    temperature_cels_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(3) > td:nth-child(3) > div > strong")
    temperature_cels=temperature_cels_ele[0].text.split("°")[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  rel_humidity=None
  try:
    rel_humidity_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(4) > td:nth-child(3) > div > strong")
    rel_humidity=rel_humidity_ele[0].text.split("%")[0].strip()
    rel_humidity=float(rel_humidity)/100

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  heat_index_cels=None
  try:
    heat_index_cels_ele=tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(6) > td:nth-child(3) > div > strong")
    heat_index_cels=heat_index_cels_ele[0].text.split("°")[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting heat_index_cels: "{e}"!')

  dew_point_cels=None
  try:
    dew_point_cels_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(5) > td:nth-child(3) > div > strong')
    dew_point_cels=dew_point_cels_ele[0].text.split('°')[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting dew_point_cels: "{e}"!')

  wind_chill_cels=None
  try:
    wind_chill_cels_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(8) > td:nth-child(3) > div > strong')
    wind_chill_cels=wind_chill_cels_ele[0].text.split('°')[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_chill_cels: "{e}"!')

  ground_temperature_cels=None
  try:
    ground_temperature_cels_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(11) > td:nth-child(3) > div > strong')
    ground_temperature_cels=ground_temperature_cels_ele[0].text.split('°')[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting ground_temperature_cels: "{e}"!')

  solar_irradiance_wpsm=None # Watts per square meter
  try:
    solar_irradiance_wpsm_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(13) > td:nth-child(3) > div > strong')
    solar_irradiance_wpsm=solar_irradiance_wpsm_ele[0].text.split(' ')[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting solar_irradiance_wpsm: "{e}"!')

  rel_leaf_wetness=None
  try:
    leaf_wetness_index_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(14) > td:nth-child(3) > div > strong')
    leaf_wetness_index=leaf_wetness_index_ele[0].text.strip() # Leaf wetness index: 0 (completely dry) to 15 (saturated).
    rel_leaf_wetness=float(leaf_wetness_index)/15

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rel_leaf_wetness: "{e}"!')

  soil_moisture_cb=None # Centibars
  try:
    soil_moisture_cb_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(12) > td:nth-child(3) > div > strong')
    soil_moisture_cb=soil_moisture_cb_ele[0].text.split(' ')[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting soil_moisture_cb: "{e}"!')

  rain_this_month_mm=None
  try:
    rain_this_month_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(22) > td.sfondotagmin > div > strong")
    rain_this_month_mm=rain_this_month_mm_ele[0].text.split(' ')[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception rain_this_month_mm: "{e}"!')

  rain_this_year_mm=None
  try:
    rain_this_year_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(23) > td.sfondotagmin > div > strong")
    rain_this_year_mm=rain_this_year_mm_ele[0].text.split(' ')[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception rain_this_year_mm: "{e}"!')

  evapotranspiration_today_mm=None
  try:
    evapotranspiration_today_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(21) > td.sfondotagmax > div > strong")
    evapotranspiration_today_mm=evapotranspiration_today_mm_ele[0].text.split(' ')[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception evapotranspiration_today_mm: "{e}"!')

  evapotranspiration_this_month_mm=None
  try:
    evapotranspiration_this_month_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(22) > td.sfondotagmax > div > strong")
    evapotranspiration_this_month_mm=evapotranspiration_this_month_mm_ele[0].text.split(' ')[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception evapotranspiration_this_month_mm: "{e}"!')

  evapotranspiration_this_year_mm=None
  try:
    evapotranspiration_this_year_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(23) > td.sfondotagmax > div > strong ")
    evapotranspiration_this_year_mm=evapotranspiration_this_year_mm_ele[0].text.split(' ')[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception evapotranspiration_this_year_mm: "{e}"!')

  uv_index=None 
  if (log):
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, wind_speed_knots: {wind_speed_knots}, wind_direction_deg: {wind_direction_deg}, barometric_pressure_hPa: {barometric_pressure_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmph: {rain_rate_mmph},  temperature_cels: {temperature_cels}, rel_humidity: {rel_humidity}, uv_index: {uv_index}, heat_index_cels: {heat_index_cels}, wind_gust_knots: {wind_gust_knots}, dew_point_cels: {dew_point_cels}, wind_chill_cels: {wind_chill_cels}, ground_temperature_cels: {ground_temperature_cels}, solar_irradiance_wpsm: {solar_irradiance_wpsm}, rel_leaf_wetness: {rel_leaf_wetness}, soil_moisture_cb: {soil_moisture_cb}, rain_this_month_mm: {rain_this_month_mm}, rain_this_year_mm: {rain_this_year_mm}, evapotranspiration_today_mm: {evapotranspiration_today_mm}, evapotranspiration_this_month_mm: {evapotranspiration_this_month_mm}, evapotranspiration_this_year_mm: {evapotranspiration_this_year_mm}')

  # UV-index is not supported by this wather station
  if not(timestamp_string and (wind_speed_knots or wind_direction_deg or barometric_pressure_hPa or rain_today_mm or rain_rate_mmph or temperature_cels or rel_humidity or uv_index or heat_index_cels or wind_gust_knots or dew_point_cels or wind_chill_cels or ground_temperature_cels or solar_irradiance_wpsm or rel_leaf_wetness or soil_moisture_cb or rain_this_month_mm or rain_this_year_mm or evapotranspiration_today_mm or evapotranspiration_this_month_mm or evapotranspiration_this_year_mm)):
    logging.info(f'{get_identification_string(location_id, server_name)}, Not enough scraped data. Skip saving data...')
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, wind_speed_knots: {wind_speed_knots}, wind_direction_deg: {wind_direction_deg}, barometric_pressure_hPa: {barometric_pressure_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmph: {rain_rate_mmph},  temperature_cels: {temperature_cels}, rel_humidity: {rel_humidity}, uv_index: {uv_index}, heat_index_cels: {heat_index_cels}, wind_gust_knots: {wind_gust_knots}, dew_point_cels: {dew_point_cels}, wind_chill_cels: {wind_chill_cels}, ground_temperature_cels: {ground_temperature_cels}, solar_irradiance_wpsm: {solar_irradiance_wpsm}, rel_leaf_wetness: {rel_leaf_wetness}, soil_moisture_cb: {soil_moisture_cb}, rain_this_month_mm: {rain_this_month_mm}, rain_this_year_mm: {rain_this_year_mm}, evapotranspiration_today_mm: {evapotranspiration_today_mm}, evapotranspiration_this_month_mm: {evapotranspiration_this_month_mm}, evapotranspiration_this_year_mm: {evapotranspiration_this_year_mm}')
    return last_seen_timestamp

  meteo_data_dict={}
  meteo_data_dict["timestamp_string"]=timestamp_string
  meteo_data_dict["timestamp_string_date"]=timestamp_string_date
  meteo_data_dict["timestamp_string_time"]=timestamp_string_time
  meteo_data_dict["wind_speed_knots"]=wind_speed_knots
  meteo_data_dict["wind_direction_deg"]=wind_direction_deg
  meteo_data_dict["barometric_pressure_hPa"]=barometric_pressure_hPa
  meteo_data_dict["rain_today_mm"]=rain_today_mm
  meteo_data_dict["rain_rate_mmph"]=rain_rate_mmph
  meteo_data_dict["temperature_cels"]=temperature_cels
  meteo_data_dict["rel_humidity"]=rel_humidity
  meteo_data_dict["uv_index"]=uv_index
  meteo_data_dict["heat_index_cels"]=heat_index_cels
  meteo_data_dict["wind_gust_knots"]=wind_gust_knots
  meteo_data_dict["dew_point_cels"]=dew_point_cels
  meteo_data_dict["wind_chill_cels"]=wind_chill_cels
  meteo_data_dict["ground_temperature_cels"]=ground_temperature_cels
  meteo_data_dict["solar_irradiance_wpsm"]=solar_irradiance_wpsm
  meteo_data_dict["rel_leaf_wetness"]=rel_leaf_wetness
  meteo_data_dict["soil_moisture_cb"]=soil_moisture_cb
  meteo_data_dict["rain_this_month_mm"]=rain_this_month_mm
  meteo_data_dict["rain_this_year_mm"]=rain_this_year_mm
  meteo_data_dict["evapotranspiration_today_mm"]=evapotranspiration_today_mm
  meteo_data_dict["evapotranspiration_this_month_mm"]=evapotranspiration_this_month_mm
  meteo_data_dict["evapotranspiration_this_year_mm"]=evapotranspiration_this_year_mm
    
  save_v6(location_id, server_name, meteo_data_dict)
  return timestamp_string

#
#
#
def scan_meteonetwork_alike(last_seen_timestamp, server, save=True, log=True):

  location_id=server["location_id"]
  server_name=server["name"]
  weather_station_url=server["url"]

  tree, _ = get_tree(weather_station_url, location_id)
  if tree is None:
    return last_seen_timestamp

  try:
    timestamp_list = tree.xpath('/html/body/div[3]/div[1]/div/h3[1]')
    timestamp_ele=timestamp_list[0].text

    time_string=timestamp_ele[len('Dati in diretta (aggiornati alle '):len('Dati in diretta (aggiornati alle ')+5]
    date_string=timestamp_ele[43:43+10]
    datetime_string=date_string+" "+time_string
    timestamp_obj=datetime.strptime(datetime_string, "%d/%m/%Y %H:%M")
    timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
    timestamp_string_date=timestamp_obj.strftime("%d/%m/%Y")
    timestamp_string_time=timestamp_obj.strftime("%H:%M:%S")

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting timestamp: "{e}"!')

  if timestamp_string==last_seen_timestamp:
    # Weather station is not updating data
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, last_seen_timestamp: {last_seen_timestamp}, skip saving!')
    # TODO Raise an alert
    return last_seen_timestamp

  temperature_cels=None
  try:
    not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[1]/td[2]/span')
    if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
      temperature_cels_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[1]/td[2]/span/text()')
      temperature_cels=temperature_cels_ele[0].strip().split("°")[0].strip()
      temperature_cels=temperature_cels.replace(" ","")
      temperature_cels=float(temperature_cels)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  rel_humidity=None
  try:
    not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[2]/td[2]/span')
    if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
      rel_humidity_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[2]/td[2]/span/text()')
      rel_humidity=rel_humidity_ele[0].strip().split("%")[0].strip()
      rel_humidity=float(rel_humidity)/100

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  barometric_pressure_hPa=None
  try:
    not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[3]/td[2]/span')
    if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
      barometric_pressure_hPa_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[3]/td[2]/span/text()')
      barometric_pressure_hPa=barometric_pressure_hPa_ele[0].strip().split(" ")[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting pressure: "{e}"!')

  wind_speed_knots=None
  try:
    not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[4]/td[2]/span[1]')
    if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
      wind_speed_kmh_elem=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[4]/td[2]/span[1]')
      wind_speed_kmh=wind_speed_kmh_elem[0].text.strip().split(" ")[0].strip()
      wind_speed_knots=float(wind_speed_kmh)/1.852

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_speed: "{e}"!')

  wind_gust_knots=None
  try:
    not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[4]/td[2]/span[1]')
    if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
      wind_gust_kmh_elem=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[4]/td[2]/span[2]')
      wind_gust_kmh=wind_gust_kmh_elem[0].text.strip().split("Raffica")[0].strip()
      wind_gust_kmh=wind_gust_kmh.split("km/h")[0].strip()
      if wind_gust_kmh:
        wind_gust_knots=float(wind_gust_kmh)/1.852

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_gust_knots: "{e}"!')

  wind_direction_deg=None
  try:  
    wind_direction_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[4]/td[3]/strong')
    wind_direction=wind_direction_ele[0].text.strip()
    wind_direction_deg=convert_wind_direction_to_deg(wind_direction)
    if not wind_direction_deg:
      logging.info(f'{get_identification_string(location_id, server_name)}, Unknown wind_direction: "{wind_direction}"!')

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  rain_today_mm=None
  try:
    not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[5]/td[2]/span')
    if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
      rain_today_mm_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[5]/td[2]/span/text()')
      rain_today_mm=str(rain_today_mm_ele[0]).strip().split(" ")[0].strip()
      rain_today_mm=float(rain_today_mm)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  dew_point_cels=None
  try:
    dew_point_cels_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[6]/td[2]/text()')
    dew_point_cels=dew_point_cels_ele[0].split("°")[0].strip()
    dew_point_cels=float(dew_point_cels)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting dew_point_cels: "{e}"!')

  heat_index=None
  try:
    # Heat index is computed
    heat_index_cels_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[7]/td[2]/text()')
    heat_index_cels=heat_index_cels_ele[0].split("°")[0].strip()
    if not heat_index_cels:
      heat_index_cels=0
    heat_index_cels=float(heat_index_cels)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting heat_index: "{e}"!')

  solar_irradiance_wpsm=None # Watts per square meter
  try:
    not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[8]/td[2]/span')
    if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
      solar_irradiance_wpsm_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[8]/td[2]/span/text()')
      solar_irradiance_wpsm=solar_irradiance_wpsm_ele[0].strip().split(" ")[0].strip()
      solar_irradiance_wpsm=float(solar_irradiance_wpsm)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting solar_irradiance_wpsm: "{e}"!')

  if log:
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, temperature_cels: {temperature_cels}, rel_humidity: {rel_humidity}, barometric_pressure_hPa: {barometric_pressure_hPa}, wind_speed_knots: {wind_speed_knots}, wind_gust_knots: {wind_gust_knots},  temperature_cels: {temperature_cels}, wind_direction_deg: {wind_direction_deg}, rain_today_mm: {rain_today_mm}, dew_point_cels: {dew_point_cels}, heat_index: {heat_index}, solar_irradiance_wpsm: {solar_irradiance_wpsm}')

  if not(timestamp_string and (temperature_cels or rel_humidity or barometric_pressure_hPa or wind_speed_knots or wind_gust_knots or wind_direction_deg or rain_today_mm or dew_point_cels or heat_index or solar_irradiance_wpsm)):
    logging.info(f'{get_identification_string(location_id, server_name)}, Not enough scraped data. Skip saving data...')
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, temperature_cels: {temperature_cels}, rel_humidity: {rel_humidity}, barometric_pressure_hPa: {barometric_pressure_hPa}, wind_speed_knots: {wind_speed_knots}, wind_gust_knots: {wind_gust_knots},  temperature_cels: {temperature_cels}, wind_direction_deg: {wind_direction_deg}, rain_today_mm: {rain_today_mm}, dew_point_cels: {dew_point_cels}, heat_index: {heat_index}, solar_irradiance_wpsm: {solar_irradiance_wpsm}')
    return last_seen_timestamp

  meteo_data_dict={}
  meteo_data_dict["timestamp_string"]=timestamp_string
  meteo_data_dict["timestamp_string_date"]=timestamp_string_date
  meteo_data_dict["timestamp_string_time"]=timestamp_string_time
  meteo_data_dict["temperature_cels"]=temperature_cels
  meteo_data_dict["rel_humidity"]=rel_humidity
  meteo_data_dict["barometric_pressure_hPa"]=barometric_pressure_hPa
  meteo_data_dict["wind_speed_knots"]=wind_speed_knots
  meteo_data_dict["wind_gust_knots"]=wind_gust_knots
  meteo_data_dict["wind_direction_deg"]=wind_direction_deg
  meteo_data_dict["rain_today_mm"]=rain_today_mm
  meteo_data_dict["dew_point_cels"]=dew_point_cels
  meteo_data_dict["heat_index"]=heat_index
  meteo_data_dict["solar_irradiance_wpsm"]=solar_irradiance_wpsm
    
  save_v6(location_id, server_name, meteo_data_dict)
  return timestamp_string

#
#
#
def scan_hotelmarcopolo_caorle_alike(last_seen_timestamp, server, save=True, log=True):

  location_id=server["location_id"]
  server_name=server["name"]
  weather_station_url=server["url"]

  tree, _ =get_tree(weather_station_url, location_id)
  if tree is None:
    return last_seen_timestamp

  timestamp_string=None
  try:
    timestamp_list = tree.xpath('/html/body/span')

    timestamp_ele=timestamp_list[0].text
    timestamp_string=timestamp_ele[-len('Dati in real-time aggiornati alle: ')+4:].strip()
    timestamp_obj=datetime.strptime(timestamp_string, "%a, %d %b %Y %H:%M:%S %z")
    timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
    timestamp_string_date=timestamp_obj.strftime("%d/%m/%Y")
    timestamp_string_time=timestamp_obj.strftime("%H:%M:%S")

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting timestamp: "{e}"!')
    return last_seen_timestamp

  if timestamp_string==last_seen_timestamp:
    # Weather station is not updating data
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, last_seen_timestamp: {last_seen_timestamp}, skip saving!')
    # TODO Raise an alert
    return last_seen_timestamp

  wind_speed_knots=None
  try:
    wind_speed_kmh_elems = tree.xpath('/html/body/table/tbody/tr[2]/td[2]/h1[2]/big/big/big/span/text()')
    wind_speed_kmh=wind_speed_kmh_elems[0].strip()
    wind_speed_knots=float(wind_speed_kmh)/1.852

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

  wind_direction_deg=None
  try:
    wind_direction_ele=tree.xpath('/html/body/table/tbody/tr[2]/td[2]/h4/big/big/span/big/big/text()')
    wind_direction=wind_direction_ele[0]
    wind_direction_deg=convert_wind_direction_to_deg(wind_direction)
    if not wind_direction_deg:
      logging.info(f'{get_identification_string(location_id, server_name)}, Unknown wind_direction: "{wind_direction}"!')

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  barometric_pressure_hPa=None
  try:
    barometric_pressure_hPa_ele = tree.xpath('/html/body/table/tbody/tr[2]/td[3]/h1[2]/big/span')
    barometric_pressure_hPa=barometric_pressure_hPa_ele[0].text.strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting barometric_pressure_hPa: "{e}"!')

  rain_today_mm=None
  try:
    rain_today_mm_ele = tree.xpath('/html/body/table/tbody/tr[4]/td[2]/h1[2]/big/span')
    rain_today_mm=rain_today_mm_ele[0].text
    rain_today_mm=rain_today_mm.split()[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  rain_rate_mmph=None
  try:
    rain_rate_mmph_ele = tree.xpath('/html/body/table/tbody/tr[4]/td[2]/h2')
    rain_rate_mmph=rain_rate_mmph_ele[0].text
    rain_rate_mmph=rain_rate_mmph.split(" ")[1].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_rate_mmph: "{e}"!')

  temperature_cels=None
  try:
    temperature_cels_ele = tree.xpath('/html/body/table/tbody/tr[2]/td[1]/h1[3]/big/big/big')
    temperature_cels=temperature_cels_ele[0].text
    temperature_cels=temperature_cels[:len(temperature_cels)-len("Â°C")+1]
    temperature_cels=temperature_cels.strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  rel_humidity=None
  try:
    humidity_ele = tree.xpath('/html/body/table/tbody/tr[3]/td/h1[2]/big/span')
    humidity=humidity_ele[0].text
    humidity=humidity.split(" %")[0]
    humidity=humidity.strip()
    rel_humidity=float(humidity)/100

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  uv_index=None
  try:
    uv_index_ele = tree.xpath('/html/body/table/tbody/tr[4]/td[1]/h1[2]/big/span')
    uv_index=uv_index_ele[0].text
    uv_index=uv_index.strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting uv_index: "{e}"!')

  heat_index_cels=None
  try:
    heat_index_cels_ele = tree.xpath('/html/body/table/tbody/tr[2]/td[1]/h3[4]/big/span')
    heat_index=heat_index_cels_ele[0].text
    heat_index=heat_index[len('Indice di calore: '):]
    heat_index=heat_index[:len(heat_index)-len("°C")-1]
    heat_index_cels=heat_index.strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting heat_index_cels: "{e}"!')

  if log:
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, wind_speed: {wind_speed_knots}, wind_direction_deg: {wind_direction_deg}, barometric_pressure_hPa: {barometric_pressure_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmph: {rain_rate_mmph},  temperature_cels: {temperature_cels}, rel_humidity: {rel_humidity}, uv_index: {uv_index}, heat_index_cels: {heat_index_cels}')    

  if not(timestamp_string and (wind_speed_knots or wind_direction_deg or barometric_pressure_hPa or rain_today_mm or rain_rate_mmph or temperature_cels or rel_humidity or uv_index or heat_index_cels)):
    logging.info(f'{get_identification_string(location_id, server_name)}, Not enough scraped data. Skip saving data...')
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, wind_speed: {wind_speed_knots}, wind_direction_deg: {wind_direction_deg}, barometric_pressure_hPa: {barometric_pressure_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmph: {rain_rate_mmph},  temperature_cels: {temperature_cels}, rel_humidity: {rel_humidity}, uv_index: {uv_index}, heat_index_cels: {heat_index_cels}')
    return last_seen_timestamp

  #
  meteo_data_dict={}
  meteo_data_dict["timestamp_string"]=timestamp_string
  meteo_data_dict["timestamp_string_date"]=timestamp_string_date
  meteo_data_dict["timestamp_string_time"]=timestamp_string_time
  meteo_data_dict["wind_speed_knots"]=wind_speed_knots
  meteo_data_dict["wind_direction_deg"]=wind_direction_deg
  meteo_data_dict["barometric_pressure_hPa"]=barometric_pressure_hPa
  meteo_data_dict["rain_today_mm"]=rain_today_mm
  meteo_data_dict["rain_rate_mmph"]=rain_rate_mmph
  meteo_data_dict["temperature_cels"]=temperature_cels
  meteo_data_dict["rel_humidity"]=rel_humidity
  meteo_data_dict["uv_index"]=uv_index
  meteo_data_dict["heat_index_cels"]=heat_index_cels
    
  save_v6(location_id, server_name, meteo_data_dict)
  return timestamp_string

#
# Scanner for MeteoVenezia weather stations alike stations
#
def scan_meteovenezia_alike(last_seen_timestamp, server, save=True, log=True):

  location_id=server["location_id"]
  server_name=server["name"]
  weather_station_url=server["url"]

  tree, _ =get_tree(weather_station_url, location_id)
  if tree is None:
    return last_seen_timestamp

  timestamp_string=None
  timestamp_string_date=None
  timestamp_string_time=None
  try: 
    timestamp_list = tree.xpath('/html/body/div[2]/table[2]/tbody/tr[1]/td[1]')
    timestamp_ele=timestamp_list[0].text.split('\xa0\xa0\xa0')
    timestamp_ele_1=timestamp_ele[0]
    timestamp_ele_2=timestamp_ele[1]

    timestamp_string=timestamp_ele_1+" "+timestamp_ele_2
    timestamp_obj=datetime.strptime(timestamp_string, "%d.%m.%Y %H:%M")

    timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
    if last_seen_timestamp and last_seen_timestamp==timestamp_string:
      return last_seen_timestamp

    timestamp_string_date=timestamp_obj.strftime("%d/%m/%Y")
    timestamp_string_time=timestamp_obj.strftime("%H:%M:%S")

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting timestamp: "{e}"!')

  if timestamp_string==last_seen_timestamp:
    # Weather station is not updating data
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, last_seen_timestamp: {last_seen_timestamp}, skip saving!')
    # TODO Raise an alert
    return last_seen_timestamp

  wind_speed_knots=None
  try:
    wind_speed_knots_elem = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[1]')
    wind_speed_knots=wind_speed_knots_elem[0].text
    wind_speed_knots=float(wind_speed_knots)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

  wind_gust_knots=None
  try:
    wind_gust_knots_elem = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[3]')
    wind_gust_knots=wind_gust_knots_elem[0].text.strip()
    wind_gust_knots=float(wind_gust_knots)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_gust_knots: "{e}"!')

  wind_direction_deg=None
  try:
    wind_direction_deg_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[2]')
    wind_direction_deg=wind_direction_deg_ele[0].text
    wind_direction_deg=wind_direction_deg.split('°')[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  barometric_pressure_hPa=None
  try:
    barometric_pressure_hPa_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[11]/td[2]')
    barometric_pressure_hPa=barometric_pressure_hPa_ele[0].text
    barometric_pressure_hPa=barometric_pressure_hPa.split('hPa')[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting barometric_pressure_hPa: "{e}"!')

  rain_today_mm=None
  try:
    rain_today_mm_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[12]/td[3]')
    rain_today_mm=rain_today_mm_ele[0].text
    rain_today_mm=rain_today_mm.split(';')[0]
    rain_today_mm=rain_today_mm[5:]
    rain_today_mm=rain_today_mm[:-3].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  rain_rate_mmph=None
  try:
    rain_rate_mmph_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[12]/td[2]')
    rain_rate_mmph=rain_rate_mmph_ele[0].text
    rain_rate_mmph=rain_rate_mmph.split('mm/h')[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_rate_mmph: "{e}"!')

  temperature_cels=None
  try:
    temperature_cels_ele=tree.xpath('/html/body/div/table[2]/tbody/tr[7]/td[2]')
    temperature_cels=temperature_cels_ele[0].text
    temperature_cels=temperature_cels.split('°')[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  rel_humidity=None
  try:
    humidity_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[9]/td[2]')
    humidity=humidity_ele[0].text
    humidity=humidity[:len(humidity)-len(" %")].strip()
    rel_humidity=float(humidity)/100

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  heat_index_cels=None
  try:
    heat_index_cels_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[8]/td[2]')
    heat_index_cels=heat_index_cels_ele[0].text
    heat_index_cels=heat_index_cels.split('°')[0]

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting heat_index_cels: "{e}"!')

  dew_point_cels=None
  try:
    dew_point_cels_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[10]/td[2]')
    dew_point_cels=dew_point_cels_ele[0].text
    dew_point_cels=dew_point_cels.split('°')[0]

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting dew_point_cels: "{e}"!')

  uv_index=None
  if log:
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, wind_speed_knots: {wind_speed_knots}, wind_direction_deg: {wind_direction_deg}, barometric_pressure_hPa: {barometric_pressure_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmph: {rain_rate_mmph},  temperature_cels: {temperature_cels}, rel_humidity: {rel_humidity}, uv_index: {uv_index}, heat_index_cels: {heat_index_cels}, wind_gust_knots: {wind_gust_knots}, dew_point_cels: {dew_point_cels}')

  uv_index=None # Unsupported by these weather stations
  if not(timestamp_string and (wind_speed_knots or wind_direction_deg or barometric_pressure_hPa or rain_today_mm or rain_rate_mmph or temperature_cels or rel_humidity or uv_index or heat_index_cels or wind_gust_knots or dew_point_cels)):
    logging.info(f'{get_identification_string(location_id, server_name)}, Not enough scraped data. Skip saving data...')
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, wind_speed_knots: {wind_speed_knots}, wind_direction_deg: {wind_direction_deg}, barometric_pressure_hPa: {barometric_pressure_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmph: {rain_rate_mmph},  temperature_cels: {temperature_cels}, rel_humidity: {rel_humidity}, uv_index: {uv_index}, heat_index_cels: {heat_index_cels}, wind_gust_knots: {wind_gust_knots}, dew_point_cels: {dew_point_cels}')
    return last_seen_timestamp

  meteo_data_dict={}
  meteo_data_dict["timestamp_string"]=timestamp_string
  meteo_data_dict["timestamp_string_date"]=timestamp_string_date
  meteo_data_dict["timestamp_string_time"]=timestamp_string_time
  meteo_data_dict["wind_speed_knots"]=wind_speed_knots
  meteo_data_dict["wind_direction_deg"]=wind_direction_deg
  meteo_data_dict["barometric_pressure_hPa"]=barometric_pressure_hPa
  meteo_data_dict["rain_today_mm"]=rain_today_mm
  meteo_data_dict["rain_rate_mmph"]=rain_rate_mmph
  meteo_data_dict["temperature_cels"]=temperature_cels
  meteo_data_dict["rel_humidity"]=rel_humidity
  meteo_data_dict["uv_index"]=uv_index
  meteo_data_dict["heat_index_cels"]=heat_index_cels
  meteo_data_dict["wind_gust_knots"]=wind_gust_knots
  meteo_data_dict["dew_point_cels"]=dew_point_cels

  save_v6(location_id, server_name, meteo_data_dict)
  return timestamp_string

#
#
#
def scan_cellarda_ws_alike(last_seen_timestamp, server, save=True, log=True):

  location_id=server["location_id"]
  server_name=server["name"]
  weather_station_url=server["url"]
  if isinstance(weather_station_url, dict):
    weather_station_url=weather_station_url.get("1")

  tree, page_text = get_tree(weather_station_url, location_id)
  if tree is None:
    return last_seen_timestamp

  timestamp_string=None
  timestamp_string_date=None
  timestamp_string_time=None
  month_converter={ "Gennaio": "01", "Febbraio": "02", "Marzo": "03", "Aprile": "04", "Maggio": "05", "Giugno": "06", \
     "Luglio": "07", "Agosto": "08", "Settembre": "09", "Ottobre": "10", "Novembre": "11", "Dicembre": "12"}
  try: 
    timestamp_string = tree.xpath("//font[contains(text(),'ULTIMO RILEVAMENTO')]")[0].text.split(" ")
    timestamp_hour=timestamp_string[4]
    timestamp_day=timestamp_string[7]
    timestamp_month=timestamp_string[8]
    timestamp_year=timestamp_string[9]

    timestamp_string=f'{timestamp_day}.{month_converter.get(timestamp_month)}.{timestamp_year} {timestamp_hour}'
    timestamp_obj=datetime.strptime(timestamp_string, "%d.%m.%Y %H:%M")

    timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
    if last_seen_timestamp and last_seen_timestamp==timestamp_string:
      return last_seen_timestamp

    timestamp_string_date=timestamp_obj.strftime("%d/%m/%Y")
    timestamp_string_time=timestamp_obj.strftime("%H:%M:%S")

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting timestamp: "{e}"!')

  if timestamp_string==last_seen_timestamp:
    # Weather station is not updating data
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, last_seen_timestamp: {last_seen_timestamp}, skip saving!')
    # TODO Raise an alert
    return last_seen_timestamp

  barometric_pressure_hPa=None
  try:
    barometric_pressure_hPa_ele = tree.xpath("//font[contains(text(),'hPa')]")
    barometric_pressure_hPa=barometric_pressure_hPa_ele[0].text
    barometric_pressure_hPa=barometric_pressure_hPa.split('hPa')[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting barometric_pressure_hPa: "{e}"!')

  rain_today_mm=None
  try:
    rain_today_mm=tree.xpath("//font")[43].text.split(" ")[0].strip()
    rain_today_mm=float(rain_today_mm)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  rain_rate_mmph=None
  try:
    rain_rate_mmph=tree.xpath("//tr/td")[21].text.split(" ")[0]
    rain_rate_mmph=float(rain_rate_mmph)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_rate_mmph: "{e}"!')

  rain_this_month=None
  try:
    rain_this_month=tree.xpath("//tr/td")[25].text.split(" ")[0]
    rain_this_month=float(rain_this_month)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_this_month: "{e}"!')

  rain_this_year=None
  try:
    rain_this_year=tree.xpath("//tr/td")[27].text.split(" ")[0]
    rain_this_year=float(rain_this_year)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_this_year: "{e}"!')

  rel_humidity=None
  try:
    humidity=tree.xpath("//tr/td")[37].text.split("%")[0].strip()
    rel_humidity=float(humidity)/100

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  temperature_cels=None
  try:
    temperature_cels_ele=tree.xpath('//b')
    temperature_cels=temperature_cels_ele[4].text.split("°")[0]
    temperature_cels=float(temperature_cels)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  heat_index_cels=None
  try:
    # Extreme problems, extreme solutions
    heat_index_cels=page_text.split("temperatura apparente")[1].split("&")[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting heat_index_cels: "{e}"!')

  dew_point_cels=None
  try:
    dew_point_cels=tree.xpath("//font")[56].text.split("°")[0]
    dew_point_cels=float(dew_point_cels)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting dew_point_cels: "{e}"!')

  #
  # From another site
  #
  wind_speed_knots=wind_gust_knots=wind_direction_deg=None
  weather_station_url=server["url"]
  if isinstance(weather_station_url, dict):
    weather_station_url=weather_station_url.get("2")
  else:
    weather_station_url=None
  if weather_station_url is not None:
    tree, _ = get_tree(weather_station_url, location_id)
    if tree is not None:

      wind_speed_knots=None
      try:
        not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[4]/td[2]/span[1]')
        if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
          wind_speed_kmh_elem=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[4]/td[2]/span[1]')
          wind_speed_kmh=wind_speed_kmh_elem[0].text.strip().split(" ")[0].strip()
          wind_speed_knots=float(wind_speed_kmh)/1.852

      except Exception as e:
        logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

      wind_gust_knots=None
      try:
        not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[4]/td[2]/span[1]')
        if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
          wind_gust_kmh_elem=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[4]/td[2]/span[2]')
          wind_gust_kmh=wind_gust_kmh_elem[0].text.strip().split(" ")[1].strip()
          if wind_gust_kmh:
            wind_gust_knots=float(wind_gust_kmh)/1.852

      except Exception as e:
        logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_gust_knots: "{e}"!')

      wind_direction_deg=None
      try:  
        wind_direction_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[4]/td[3]/strong')
        wind_direction=wind_direction_ele[0].text.strip()
        wind_direction_deg=convert_wind_direction_to_deg(wind_direction)
        if not wind_direction_deg:
          logging.info(f'{get_identification_string(location_id, server_name)}, Unknown wind_direction: "{wind_direction}"!')

      except Exception as e:
        logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  if not(timestamp_string and (barometric_pressure_hPa or rain_today_mm or rain_rate_mmph or rain_this_month or rain_this_year or rel_humidity or temperature_cels or heat_index_cels or dew_point_cels or wind_speed_knots or wind_gust_knots or wind_direction_deg)):
    logging.info(f'{get_identification_string(location_id, server_name)}, Not enough scraped data. Skip saving data...')
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, barometric_pressure_hPa: {barometric_pressure_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmph: {rain_rate_mmph }, rain_this_month: {rain_this_month}, rain_this_year: {rain_this_year},  rel_humidity: {rel_humidity}, temperature_cels: {temperature_cels}, heat_index_cels: {heat_index_cels}, dew_point_cels: {dew_point_cels}, wind_speed_knots: {wind_speed_knots}, wind_gust_knots: {wind_gust_knots}, wind_direction_deg: {wind_direction_deg}')
    return last_seen_timestamp

  meteo_data_dict={}
  meteo_data_dict["timestamp_string"]=timestamp_string
  meteo_data_dict["timestamp_string_date"]=timestamp_string_date
  meteo_data_dict["timestamp_string_time"]=timestamp_string_time
  meteo_data_dict["barometric_pressure_hPa"]=barometric_pressure_hPa
  meteo_data_dict["rain_today_mm"]=rain_today_mm
  meteo_data_dict["rain_rate_mmph"]=rain_rate_mmph
  meteo_data_dict["rain_this_month"]=rain_this_month
  meteo_data_dict["rain_this_year"]=rain_this_year
  meteo_data_dict["rel_humidity"]=rel_humidity
  meteo_data_dict["temperature_cels"]=temperature_cels
  meteo_data_dict["heat_index_cels"]=heat_index_cels
  meteo_data_dict["dew_point_cels"]=dew_point_cels
  meteo_data_dict["wind_speed_knots"]=wind_speed_knots
  meteo_data_dict["wind_gust_knots"]=wind_gust_knots
  meteo_data_dict["wind_direction_deg"]=wind_direction_deg

  save_v6(location_id, server_name, meteo_data_dict)
  return timestamp_string

#
#
#
def scan_cellarda_nord_ws_alike(last_seen_timestamp, server, save=True, log=True):

  location_id=server["location_id"]
  server_name=server["name"]
  weather_station_url=server["url"]

  tree, page_text = get_tree(weather_station_url, location_id)
  if tree is None:
    return last_seen_timestamp

  timestamp_string=None
  timestamp_string_date=None
  timestamp_string_time=None
  month_converter={ "Gennaio": "01", "Febbraio": "02", "Marzo": "03", "Aprile": "04", "Maggio": "05", "Giugno": "06", \
     "Luglio": "07", "Agosto": "08", "Settembre": "09", "Ottobre": "10", "Novembre": "11", "Dicembre": "12"}
  try: 
    timestamp_string = tree.xpath("//font[contains(text(),'ULTIMO RILEVAMENTO')]")[0].text.split(" ")
    timestamp_hour=timestamp_string[4]
    timestamp_day=timestamp_string[7]
    timestamp_month=timestamp_string[8]
    timestamp_year=timestamp_string[9]

    timestamp_string=f'{timestamp_day}.{month_converter.get(timestamp_month)}.{timestamp_year} {timestamp_hour}'
    timestamp_obj=datetime.strptime(timestamp_string, "%d.%m.%Y %H:%M")

    timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
    if last_seen_timestamp and last_seen_timestamp==timestamp_string:
      return last_seen_timestamp

    timestamp_string_date=timestamp_obj.strftime("%d/%m/%Y")
    timestamp_string_time=timestamp_obj.strftime("%H:%M:%S")

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting timestamp: "{e}"!')

  if timestamp_string==last_seen_timestamp:
    # Weather station is not updating data
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, last_seen_timestamp: {last_seen_timestamp}, skip saving!')
    # TODO Raise an alert
    return last_seen_timestamp

  barometric_pressure_hPa=None
  try:
    barometric_pressure_hPa_ele = tree.xpath("//font[contains(text(),'hPa')]")
    barometric_pressure_hPa=barometric_pressure_hPa_ele[0].text
    barometric_pressure_hPa=barometric_pressure_hPa.split('hPa')[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting barometric_pressure_hPa: "{e}"!')

  rain_today_mm=None
  try:
    rain_today_mm=tree.xpath("//font")[43].text.split(" ")[0].strip()
    rain_today_mm=float(rain_today_mm)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  rain_rate_mmph=None
  try:
    rain_rate_mmph=tree.xpath("//tr/td")[21].text.split(" ")[0]
    rain_rate_mmph=float(rain_rate_mmph)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_rate_mmph: "{e}"!')

  rain_this_month_mm=None
  try:
    rain_this_month_mm=tree.xpath("//tr/td")[25].text.split(" ")[0]
    rain_this_month_mm=float(rain_this_month_mm)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_this_month_mm: "{e}"!')

  rain_this_year_mm=None
  try:
    rain_this_year_mm=tree.xpath("//tr/td")[27].text.split(" ")[0]
    rain_this_year_mm=float(rain_this_year_mm)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_this_year_mm: "{e}"!')

  rel_humidity=None
  try:
    humidity=tree.xpath("//tr/td")[37].text.split("%")[0].strip()
    rel_humidity=float(humidity)/100

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  temperature_cels=None
  try:
    temperature_cels_ele=tree.xpath('//b')
    temperature_cels=temperature_cels_ele[5].text.split("°")[0]
    temperature_cels=float(temperature_cels)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  heat_index_cels=None
  try:
    # Extreme problems, extreme solutions
    heat_index_cels=page_text.split("temperatura apparente")[1].split("&")[0].strip()

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting heat_index_cels: "{e}"!')

  dew_point_cels=None
  try:
    dew_point_cels=tree.xpath("//font")[56].text.split("°")[0]
    dew_point_cels=float(dew_point_cels)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting dew_point_cels: "{e}"!')

  wind_speed_knots=None
  try:
    wind_speed_kmh=tree.xpath("//tr/td")[9].text.split(" ")[0].strip()
    wind_speed_knots=float(wind_speed_kmh)/1.852

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

  wind_gust_knots=None
  try:
    wind_gust_kmh=page_text.split('Massima forza </font><FONT SIZE=+0> (ultima ora)</td><td><font color="#009900">')[1].split(" ")[0]
    if wind_gust_kmh:
      wind_gust_knots=float(wind_gust_kmh)/1.852

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_gust_knots: "{e}"!')

  wind_direction_deg=None
  try:  
    wind_direction=tree.xpath("//tr/td")[11].text.split(" ")[0].strip()
    wind_direction_deg=convert_wind_direction_to_deg(wind_direction)
    if not wind_direction_deg:
      logging.info(f'{get_identification_string(location_id, server_name)}, Unknown wind_direction: "{wind_direction}"!')

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  if not(timestamp_string and (barometric_pressure_hPa or rain_today_mm or rain_rate_mmph or rain_this_month_mm or rain_this_year_mm or rel_humidity or temperature_cels or heat_index_cels or dew_point_cels or wind_speed_knots or wind_gust_knots or wind_direction_deg)):
    logging.info(f'{get_identification_string(location_id, server_name)}, Not enough scraped data. Skip saving data...')
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, barometric_pressure_hPa: {barometric_pressure_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmph: {rain_rate_mmph }, rain_this_month_mm: {rain_this_month_mm}, rain_this_year_mm: {rain_this_year_mm},  rel_humidity: {rel_humidity}, temperature_cels: {temperature_cels}, heat_index_cels: {heat_index_cels}, dew_point_cels: {dew_point_cels}, wind_speed_knots: {wind_speed_knots}, wind_gust_knots: {wind_gust_knots}, wind_direction_deg: {wind_direction_deg}')
    return last_seen_timestamp

  meteo_data_dict={}
  meteo_data_dict["timestamp_string"]=timestamp_string
  meteo_data_dict["timestamp_string_date"]=timestamp_string_date
  meteo_data_dict["timestamp_string_time"]=timestamp_string_time
  meteo_data_dict["barometric_pressure_hPa"]=barometric_pressure_hPa
  meteo_data_dict["rain_today_mm"]=rain_today_mm
  meteo_data_dict["rain_rate_mmph"]=rain_rate_mmph
  meteo_data_dict["rain_this_month_mm"]=rain_this_month_mm
  meteo_data_dict["rain_this_year_mm"]=rain_this_year_mm
  meteo_data_dict["rel_humidity"]=rel_humidity
  meteo_data_dict["temperature_cels"]=temperature_cels
  meteo_data_dict["heat_index_cels"]=heat_index_cels
  meteo_data_dict["dew_point_cels"]=dew_point_cels
  meteo_data_dict["wind_speed_knots"]=wind_speed_knots
  meteo_data_dict["wind_gust_knots"]=wind_gust_knots
  meteo_data_dict["wind_direction_deg"]=wind_direction_deg

  save_v6(location_id, server_name, meteo_data_dict)
  return timestamp_string

#
#
#
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
    "note": "Meteo station @ https://www.meteo-caorle.it/, Porto Santa Margherita, Spiaggia Est, Caorle, Venezia",
    "height_asl_m": 0
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
    "note": "Meteo station @ https://www.meteo-venezia.net/compagnia01.php, Isola di San Giorgio Maggiore, Venezia",
    "height_asl_m": 0
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
    "note": "Meteo station @ https://www.meteo-venezia.net/, Punta San Giuliano, Mestre-Venezia",
    "height_asl_m": 0
}, {
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
    "note": "Meteo station @ https://www.bibione-meteo.it/, Bibione, Venezia",
    "height_asl_m": 0
}, {
    "name": 'Hotel "Marco Polo", Caorle',
    "latitude": 45.5978224,
    "longitude": 12.8839359,
    "address_complete": "Via della Serenissima, 22, 30021 Caorle VE",
    "street_1": "Via della Serenissima, 22",
    "street_2": None,
    "zip": "30021",
    "town": "Caorle",
    "province": "VE",
    "country": "IT",
    "note": "Meteo station @ https://www.hotelmarcopolocaorle.it/meteo/hmpolocaorle.php",
    "height_asl_m": 0
}, {
    "name": 'Meteo Network stazione meteo di Feltre',
    "latitude": 46.016,
    "longitude": 11.895,
    "address_complete": None,
    "street_1": None,
    "street_2": None,
    "zip": "32032",
    "town": "Feltre",
    "province": "BL",
    "country": "IT",
    "note": "Meteo station @ http://my.meteonetwork.it/station/vnt336/, Model: MTX, Type: Semi-Urbana, Ubicazione: Campo aperto",
    "height_asl_m": 267
}, {
    "name": 'Osservatorio meteorologico di I.I.S. Agrario “Antonio della Lucia” di Feltre (BL)',
    "latitude": 46.036,
    "longitude": 11.937,
    "address_complete": "Via Vellai, 41, 32032 Vellai BL",
    "street_1": "Via Vellai,",
    "street_2": None,
    "zip": "32032",
    "town": "Feltre",
    "province": "BL",
    "country": "IT",
    "note": "Meteo station @ http://www.meteosystem.com/dati/feltre/dati.php, Model: Davis Vantage Pro 2",
    "height_asl_m": 330
}, {
    "name": 'LaCrosse WS2300 di Pellencin Giorgio, Cellarda Sud, Feltre (BL)',
    "latitude": 46.011,
    "longitude": 11.966,
    "address_complete": "Cellarda Sud, 32032 Feltre (BL)",
    "street_1": "Cellarda Sud",
    "street_2": None,
    "zip": "32032",
    "town": "Feltre",
    "province": "BL",
    "country": "IT",
    "note": "Stazione Meteo di Pellencin Giorgio, Cellarda Sud, @ http://www.celarda.altervista.org/index.htm, Model: LaCrosse WS2300",
    "height_asl_m": 225
}, {
    "name": 'LaCrosse WS2300 di Pellencin Giorgio, Cellarda Nord, Feltre (BL)',
    "latitude": 46.011,
    "longitude": 11.966,
    "address_complete": "Cellarda Nord, 32032 Feltre (BL)",
    "street_1": "Cellarda Nord",
    "street_2": None,
    "zip": "32032",
    "town": "Feltre",
    "province": "BL",
    "country": "IT",
    "note": "Stazione Meteo di Pellencin Giorgio, Cellarda Nord, @ http://www.meteocelarda.altervista.org/index.htm, Model: LaCrosse WS2300",
    "height_asl_m": 225
}]

# "scan_time_interval" in seconds
servers = [
  { "location_id":  1, "location": locations_json[4], "to_be_started": True, "name": "hotelmarcopolo_caorle", "url": "https://www.hotelmarcopolocaorle.it/meteo/hmpolocaorle.php", "scanner": scan_hotelmarcopolo_caorle_alike, "scan_time_interval": 55 }, # Wait for 50 secs
  { "location_id":  4, "location": locations_json[0], "to_be_started": True, "name": "bagnomargherita_caorle", "url": "https://www.meteo-caorle.it/", "scanner": scan_meteovenezia_alike, "scan_time_interval": 55 },
  { "location_id":  8, "location": locations_json[1], "to_be_started": True, "name": "sangiorgio_venezia", "url": "https://www.meteo-venezia.net/compagnia01.php", "scanner": scan_meteovenezia_alike, "scan_time_interval": 55 },
  { "location_id":  9, "location": locations_json[2], "to_be_started": True, "name": "puntasangiuliano_mestre", "url": "https://www.meteo-venezia.net/", "scanner": scan_meteovenezia_alike, "scan_time_interval": 55 },
  { "location_id": 10, "location": locations_json[3], "to_be_started": True, "name": "lagunaparkhotel_bibione", "url": "https://www.bibione-meteo.it/", "scanner": scan_meteovenezia_alike, "scan_time_interval":55 },
  { "location_id": 11, "location": locations_json[5], "to_be_started": True, "name": "meteonetwork_feltre", "url": "http://my.meteonetwork.it/station/vnt336/", "scanner": scan_meteonetwork_alike, "scan_time_interval": 60*30 }, # Wait for half an hour
  { "location_id": 12, "location": locations_json[6], "to_be_started": True, "name": "agrario_feltre", "url": "http://www.meteosystem.com/dati/feltre/dati.php", "scanner": scan_meteosystem_alike, "scan_time_interval": 55 },
  { "location_id": 15, "location": locations_json[7], "to_be_started": True, "name": "cellarda_sud_feltre", "url": {"1": "http://www.celarda.altervista.org/index.htm", "2": "http://my.meteonetwork.it/station/vnt374/" }, "scanner": scan_cellarda_ws_alike, "scan_time_interval": 60*5 },
  { "location_id": 16, "location": locations_json[8], "to_be_started": True, "name": "cellarda_nord_feltre", "url": "http://www.meteocelarda.altervista.org/index.htm", "scanner": scan_cellarda_nord_ws_alike, "scan_time_interval": 60*5 } # Wait five minutes
]

SCAN_TIME_INTERVAL_DEFAULT=50 # Sec

#
#
#
def main_logger(server, save=True, log=False):
  logging.info(f'Thread ident: {threading.get_ident()}, Client for server: {server["location_id"]}, {server["name"]}, url: {server["url"]} up and running.')
  scanner=server["scanner"]
  scan_time_interval=server.get("scan_time_interval")
  if not scan_time_interval:
    scan_time_interval=SCAN_TIME_INTERVAL_DEFAULT
  while True:
    last_seen_timestamp=server.get("last_seen_timestamp", None)
    scan_no=server.get("scan_no", 0)
    scan_no=scan_no+1
    logging.info(f'{get_identification_string(server["location_id"], server["name"])}, scan: {scan_no}...')
    last_seen_timestamp=scanner(last_seen_timestamp, server, save, log)
    server["last_seen_timestamp"]=last_seen_timestamp
    server["scan_no"]=scan_no
    time.sleep(scan_time_interval)

#
#
#
def add_server_location(server):
    location_json=server["location"]
    headers={'Content-Type': 'application/json; charset=utf-8'}
    response=requests.post('http://localhost:8080/api/location', headers=headers, json=location_json)
    logging.info(f'Location id: {server["location_id"]}, name: {server["name"]}, response: {response}')

#
#
#
def add_server_locations(servers):
  for server in servers:
    location_id=server["location_id"]
    if location_id==13 or location_id==14:
      add_server_location(server)

#
#
#
if __name__=="__main__":
  #add_server_locations(servers)
  format = "%(asctime)s %(thread)d %(threadName)s: %(message)s"
  logging.basicConfig(filename="app/log/meteo_data_repo3.log", format=format, level=logging.NOTSET, datefmt="%Y-%m-%d %H:%M:%S")

  logging.info('##')
  logging.info("## 'Meteo data repo' data collector clients launcher")
  logging.info('##')
  logging.info('Starting clients...')
  nclients=0
  for server in servers:
    to_be_started=server["to_be_started"]
    if to_be_started==False:
      logging.info(f'Server: {server["location_id"]}, {server["name"]}, url: {server["url"]} starting DISABLED.')
      continue

    logging.info(f'Starting client for server: {server["location_id"]}, {server["name"]}, url: {server["url"]}...')
    threading.Thread(target=main_logger, args=(server, )).start()
    nclients=nclients+1

  logging.info(f'Clients starting complete. Started: {nclients} clients. Launcher ends.')
