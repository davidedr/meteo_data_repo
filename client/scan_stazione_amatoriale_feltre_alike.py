from datetime import datetime
import logging
import platform
from bs4 import BeautifulSoup
from selenium import webdriver

import utility

#
#
#
def scan_stazione_amatoriale_feltre_alike(last_seen_timestamp, server, save=True, log=True):

  location_id=server["location_id"]
  server_name=server["name"]
  weather_station_url=server["url"]

  if platform.system() == 'Windows':
      PHANTOMJS_PATH = './utility/phantomjs.exe'
  else:
      PHANTOMJS_PATH = './utility/phantomjs'

  #import os
  #print(os.getcwd())

  try:
    browser = webdriver.PhantomJS(PHANTOMJS_PATH)
    browser.get(weather_station_url)
    soup = BeautifulSoup(browser.page_source, "html.parser")

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting getting webpage: "{e}"!')
    return last_seen_timestamp
    
  if soup is None:
      logging.info(f'{utility.get_identification_string(location_id, server_name)}, soup is None: "{soup}"!')
      return last_seen_timestamp

  #games = soup.find_all('span', {'id': 'currentPValue'})
  #print(games[0].text)
  #print(games.prettify())

  timestamp_string=None
  try:
    
    currentTimestampValue_ele=soup.find('span', id='currentTimestampValue')
    currentTimestampValue=currentTimestampValue_ele.text
    timestamp_obj_time=datetime.strptime(currentTimestampValue, "%H:%M:%S")

    timestamp_obj=datetime.now()
    timestamp_obj.replace(hour=timestamp_obj_time.hour, minute=timestamp_obj_time.minute, second=timestamp_obj_time.second)
    timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
    timestamp_string_date=timestamp_obj.strftime("%d/%m/%Y")
    timestamp_string_time=timestamp_obj.strftime("%H:%M:%S")

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting timestamp: "{e}"!')
    return last_seen_timestamp

  if timestamp_string==last_seen_timestamp:
    # Weather station is not updating data
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, last_seen_timestamp: {last_seen_timestamp}, skip saving!')
    # TODO Raise an alert
    return last_seen_timestamp

  temperature_cels=None
  try:
    temperature_ele=soup.find('div', id='currentConditionsBigDiv')
    temperature=temperature_ele[0].text.split("°")[0].strip()
    if temperature:
      temperature_cels=float(temperature)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  rel_humidity=None
  try:
    humidity_ele=soup.find('span', id='currentHValue')
    humidity=humidity_ele.text.strip()
    if humidity:
      rel_humidity=float(humidity)/100

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  barometric_pressure_hPa=None
  try:
    barometric_pressure_ele=soup.find('span', id='currentPValue')
    barometric_pressure=barometric_pressure_ele.text.strip()
    if barometric_pressure:
      barometric_pressure_hPa=float(barometric_pressure)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting barometric_pressure_hPa: "{e}"!')

  wind_speed_knots=None
  try:
    wind_speed_kmh_elems=soup.find('span', id='currentWValue')
    wind_speed_kmh=wind_speed_kmh_elems.text.strip()
    if wind_speed_kmh:
      wind_speed_knots=float(wind_speed_kmh)/1.852

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

  wind_direction_deg=None
  try:
    wind_direction_ele=soup.find('span', id='currentBValue')
    wind_direction=wind_direction_ele.text.strip()
    wind_direction_deg=utility.convert_wind_direction_to_deg(wind_direction)
    if not wind_direction_deg:
      logging.info(f'{utility.get_identification_string(location_id, server_name)}, Unknown wind_direction: "{wind_direction}"!')

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  wind_gust_knots=None
  try:
    wind_gust_kmh_elem=soup.find('span', id='currentGValue')
    wind_gust_kmh=wind_gust_kmh_elem.text.strip()
    if wind_gust_kmh:
      wind_gust_knots=float(wind_gust_kmh)/1.852

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

  rain_rate_mmph=None
  try:
    rain_rate_ele=soup.find('span', id='currentDetailsValueRR')
    rain_rate=rain_rate_ele.text.strip()
    if rain_rate:
      rain_rate_mmph=float(rain_rate)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_rate_mmph: "{e}"!')

  rain_today_mm=None
  try:
    rain_today_ele=soup.find('span', id='currentRRValue')
    rain_today=rain_today_ele.text.strip()
    if rain_today:
      rain_today_mm=float(rain_today)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  dew_point_cels=None
  try:
    dew_point_ele=soup.find('span', id='currentDValue')
    dew_point=dew_point_ele.text.strip()
    if dew_point:
      dew_point_cels=float(dew_point)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting uv_index: "{e}"!')

  wind_chill_cels=None
  try:
    wind_chill_ele=soup.find('span', id='currentDetailsValueWCh')
    wind_chill=wind_chill_ele.text.strip()
    if wind_chill and wind_chill is not "--":
      wind_chill_cels=float(wind_chill)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting uv_index: "{e}"!')

  uv_index=None
  try:
    uv_index_ele=soup.find('span', id='currentDetailsValueUV')
    uv_index_ele=uv_index_ele.text.strip()
    if uv_index_ele:
      uv_index=float(uv_index_ele)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting uv_index: "{e}"!')

  heat_index_cels=None
  try:
    heat_index_ele=soup.find('span', id='currentDetailsValueHI')
    heat_index=heat_index_ele.text.strip()
    if heat_index and heat_index is not "--":
      heat_index_cels=float(heat_index)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting heat_index_cels: "{e}"!')

  if log:
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, wind_speed_knots: {wind_speed_knots}, wind_gust_knots: {wind_gust_knots},wind_direction_deg: {wind_direction_deg}, barometric_pressure_hPa: {barometric_pressure_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmph: {rain_rate_mmph},  temperature_cels: {temperature_cels}, rel_humidity: {rel_humidity}, uv_index: {uv_index}, heat_index_cels: {heat_index_cels}, dew_point_cels: {dew_point_cels}, wind_chill_cels: {wind_chill_cels}')

  if not(timestamp_string and (wind_speed_knots or wind_direction_deg or barometric_pressure_hPa or rain_today_mm or rain_rate_mmph or temperature_cels or rel_humidity or uv_index or heat_index_cels)):
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, Not enough scraped data. Skip saving data...')
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, wind_speed: {wind_speed_knots}, wind_direction_deg: {wind_direction_deg}, barometric_pressure_hPa: {barometric_pressure_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmph: {rain_rate_mmph},  temperature_cels: {temperature_cels}, rel_humidity: {rel_humidity}, uv_index: {uv_index}, heat_index_cels: {heat_index_cels}')
    return last_seen_timestamp

  #
  meteo_data_dict={}
  meteo_data_dict["timestamp_string"]=timestamp_string
  meteo_data_dict["timestamp_string_date"]=timestamp_string_date
  meteo_data_dict["timestamp_string_time"]=timestamp_string_time
  meteo_data_dict["wind_speed_knots"]=wind_speed_knots
  meteo_data_dict["wind_gust_knots"]=wind_gust_knots
  meteo_data_dict["wind_direction_deg"]=wind_direction_deg
  meteo_data_dict["barometric_pressure_hPa"]=barometric_pressure_hPa
  meteo_data_dict["rain_today_mm"]=rain_today_mm
  meteo_data_dict["rain_rate_mmph"]=rain_rate_mmph
  meteo_data_dict["temperature_cels"]=temperature_cels
  meteo_data_dict["rel_humidity"]=rel_humidity
  meteo_data_dict["uv_index"]=uv_index
  meteo_data_dict["heat_index_cels"]=heat_index_cels
  meteo_data_dict["dew_point_cels"]=dew_point_cels
  meteo_data_dict["wind_chill_cels"]=wind_chill_cels
    
  utility.save_v6(location_id, server_name, meteo_data_dict)
  return timestamp_string

if __name__=="__main__":
  utility.test_starter(18) # Location id
