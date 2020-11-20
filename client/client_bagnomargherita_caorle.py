import requests
import csv
from datetime import datetime
from lxml import html
import requests
import unicodedata
import logging

import utility

#
#
#
def scan(last_seen_timestamp, server, save=True, log=True):

  location_id=server["location_id"]
  server_name=server["name"]
  weather_station_url=server["url"]

  tree, _ =utility.get_tree(weather_station_url, location_id, server_name)
  if tree is None:
    return last_seen_timestamp

  timestamp_string=None
  timestamp_string_date=None
  timestamp_string_time=None
  try:
    timestamp_list = tree.xpath('/html/body/div[2]/table[2]/tbody/tr[1]/td[1]')
    timestamp_ele=timestamp_list[0].text
    timestamp_ele_1=timestamp_ele[1:11]
    timestamp_ele_2=timestamp_ele[14:20]

    timestamp_string=timestamp_ele_1+" "+timestamp_ele_2
    timestamp_obj=datetime.strptime(timestamp_string, "%d.%m.%Y %H:%M")

    timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
    timestamp_string_date=timestamp_obj.strftime("%d/%m/%Y")
    timestamp_string_time=timestamp_obj.strftime("%H:%M:%S")

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting timestamp: "{e}"!')

  if last_seen_timestamp and last_seen_timestamp==timestamp_string:
    return last_seen_timestamp

  wind_speed_knots=None
  try:
    wind_speed_elem = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[1]')
    wind_speed=wind_speed_elem[0].text
    if wind_speed:
      wind_speed_knots=float(wind_speed)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

  wind_gust_knots=None
  try:
    wind_gust_elem = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[3]')
    wind_gust=wind_gust_elem[0].text.strip()
    if wind_gust:
      wind_gust_knots=float(wind_gust)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_gust_knots: "{e}"!')

  wind_direction_deg=None
  try:
    wind_direction = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[2]')
    wind_direction=wind_direction[0].text.split('°')[0].strip()
    if wind_direction:
      wind_direction_deg=float(wind_direction)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  barometric_pressure_ssl_hPa=None
  try:
    barometric_pressure_ssl_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[11]/td[2]')
    barometric_pressure_ssl=barometric_pressure_ssl_ele[0].text.split('hPa')[0].strip()
    if barometric_pressure_ssl:
      barometric_pressure_ssl_hPa=float(barometric_pressure_ssl)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting barometric_pressure_ssl_hPa: "{e}"!')

  rain_today_mm=None
  try:
    rain_today_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[12]/td[3]')
    rain_today=rain_today_ele[0].text
    rain_today=rain_today.split(';')[0]
    rain_today=rain_today[5:]
    rain_today=rain_today[:-3].strip()
    if rain_today:
      rain_today_mm=float(rain_today)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  rain_rate_mmh=None
  try:
    rain_rate_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[12]/td[2]')
    rain_rate=rain_rate_ele[0].text
    rain_rate=rain_rate.split('mm/h')[0].strip()
    if rain_rate:
      rain_rate_mmh=float(rain_rate)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_rate_mmh: "{e}"!')

  temperature_cels=None
  try:
    temperature_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[7]/td[2]')
    temperature=temperature_ele[0].text.split('°')[0].strip()
    if temperature:
      temperature_cels=float(temperature)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  rel_humidity=None
  try:
    humidity_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[9]/td[2]')
    humidity=humidity_ele[0].text.split(" ")[0].strip()
    if humidity:
      rel_humidity=float(humidity)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  heat_index_cels=None
  try:
    heat_index_cels_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[8]/td[2]')
    heat_index=heat_index_cels_ele[0].text.split('°')[0]
    if heat_index:
      heat_index_cels=float(heat_index_cels)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting heat_index_cels: "{e}"!')

  dew_point_cels=None  
  try:
    dew_point_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[10]/td[2]')
    dew_point=dew_point_ele[0].text.split('°')[0]
    if dew_point:
      dew_point_cels=float(dew_point_cels)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting dew_point_cels: "{e}"!')

  meteo_data_dict = {
    "location_id": location_id,
    "timestamp": timestamp_string,
    "timestamp_date": timestamp_string_date,
    "timestamp_time": timestamp_string_time,
    "wind_speed_knots": float(wind_speed_knots),
    "wind_direction_deg": wind_direction_deg,
    "barometric_pressure_ssl_hPa": float(barometric_pressure_ssl_hPa),
    "rain_today_mm": float(rain_today_mm),
    "rain_rate_mmh": float(rain_rate_mmh),
    "temperature_cels": temperature_cels,
    "rel_humidity": rel_humidity,
    "heat_index_cels	": heat_index_cels,
    "wind_gust_knots": wind_gust_knots,
    "dew_point_cels": dew_point_cels
  }

  if log:
    utility.log_sample(location_id, server_name, meteo_data_dict)

  utility.save_v11(location_id, server_name, meteo_data_dict)
  return timestamp_string

if __name__=="__main__":
  utility.test_starter(4) # Location id
