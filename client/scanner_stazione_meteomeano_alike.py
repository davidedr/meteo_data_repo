from datetime import datetime
import logging
import platform
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent

import utility
import proxy_pool

#
# Unfortunately, this server ui is similar not equal to location id 18 stazione_amatoriale_feltre
#
def scan_stazione_meteomeano_alike(last_seen_timestamp, server, save=True, log=True):

  location_id=server["location_id"]
  server_name=server["name"]
  weather_station_url=server["url"]

  if platform.system() == 'Windows':
      PHANTOMJS_PATH = './utility/phantomjs.exe'
  else:
      PHANTOMJS_PATH = './utility/phantomjs'
      
  try:

    user_agent = UserAgent().random 
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent']=user_agent

    service_args=None

    """
    proxy=proxy_pool.get_proxy(location_id, server_name)
    if proxy is not None:
      service_args = [f'--proxy={proxy}', '--proxy-type=https']
    """

    browser = webdriver.PhantomJS(PHANTOMJS_PATH, service_log_path='./app/log/ghostdriver.log', service_args=service_args)
    browser.get(weather_station_url)
    soup = BeautifulSoup(browser.page_source, "html.parser")

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting getting webpage: "{e}"!')
    return last_seen_timestamp
    
  if soup is None:
      logging.info(f'{utility.get_identification_string(location_id, server_name)}, soup is None: "{soup}"!')
      return last_seen_timestamp

  timestamp_string=None
  try:
    currentTimestampValue_ele=soup.find('span', id='currentTimestampValue')
    currentTimestampValue=currentTimestampValue_ele.text
    if "OfflineLast update:" in currentTimestampValue:
      logging.exception(f'{utility.get_identification_string(location_id, server_name)}, ws station is Offline! weather_station_url: {weather_station_url}, currentTimestampValue: {currentTimestampValue}!')
      return last_seen_timestamp

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

  current_weather=None
  try:
    # soup.select('img[src*="homepage/blocks/current/icons/light"]')[0]["src"] works as well
    current_weather_ele=soup.findAll('img', style="width:50px")
    current_weather_src=current_weather_ele[0]['src'].split("/")[5].split(".")[0]
    if current_weather_src:
      current_weather=current_weather_src

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting current_weather: "{e}"!')

  temperature_cels=None
  try:
    temperature_ele=soup.find('span', id='currentDetailsValueT')
    temperature=temperature_ele.text.split("°")[0].strip()
    if temperature:
      temperature_cels=float(temperature)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  perceived_temperature_cels=None
  try:
    perceived_temperature=soup.find('span', id='currentDetailsValueA').text.strip()
    if perceived_temperature:
      perceived_temperature_cels=float(perceived_temperature)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting perceived_temperature_cels: "{e}"!')

  dew_point_cels=None
  try:
    dew_point_ele=soup.find('span', id='currentDetailsValueD')
    dew_point=dew_point_ele.text.strip()
    if dew_point:
      dew_point_cels=float(dew_point)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting dew_point_cels: "{e}"!')

  heat_index_cels=None
  try:
    heat_index_ele=soup.find('span', id='currentDetailsValueHI')
    heat_index=heat_index_ele.text.strip()
    if heat_index and not heat_index=="--":
      heat_index_cels=float(heat_index)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting heat_index_cels: "{e}"!')

  humidex_cels=None
  try:
    humidex=soup.find('span', id='currentDetailsValueHX').text.strip()
    if humidex:
      humidex_cels=float(humidex)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting humidex_cels: "{e}"!')

  wind_chill_cels=None
  try:
    wind_chill_ele=soup.find('span', id='currentDetailsValueWCh')
    wind_chill=wind_chill_ele.text.strip()
    if wind_chill and not wind_chill=='--':
      wind_chill_cels=float(wind_chill)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_chill_cels: "{e}"!')

  wet_bulb_temperature_cels=None
  try:
    wet_bulb_temperature_ele=soup.find('span', id='currentDetailsValueWB')
    wet_bulb_temperature=wet_bulb_temperature_ele.text
    if wet_bulb_temperature:
      wet_bulb_temperature_cels=float(wet_bulb_temperature)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wet_bulb_temperature_cels: "{e}"!')

  rel_humidity=None 
  try:
    humidity_ele=soup.find('span', id='currentDetailsValueH')
    humidity=humidity_ele.text.strip()
    if humidity:
      rel_humidity=float(humidity)/100

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  absolute_humidity_gm3=None
  try:
    absolute_humidity_ele=soup.find('span', id='currentDetailsValueAH')
    absolute_humidity=absolute_humidity_ele.text.strip()
    if absolute_humidity:
      absolute_humidity_gm3=float(absolute_humidity)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting absolute_humidity_gm3: "{e}"!')

  saturated_vapor_pressure_hPa=None
  try:
    saturated_vapor_pressure_ele=soup.find('span', id='currentDetailsValueSVP')
    saturated_vapor_pressure=saturated_vapor_pressure_ele.text.strip()
    if saturated_vapor_pressure:
      saturated_vapor_pressure_hPa=float(saturated_vapor_pressure)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting saturated_vapor_pressure_hPa: "{e}"!')

  rain_rate_mmh=None
  try:
    rain_rate_ele=soup.find('span', id='currentDetailsValueRR')
    rain_rate=rain_rate_ele.text.strip()
    if rain_rate:
      rain_rate_mmh=float(rain_rate)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_rate_mmh: "{e}"!')

  rain_today_mm=None
  try:
    rain_today_ele=soup.find('span', id='currentDetailsValueR')
    rain_today=rain_today_ele.text.strip()
    if rain_today:
      rain_today_mm=float(rain_today)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  wind_speed_knots=None
  try:
    wind_speed_kmh_elems=soup.find('span', id='currentDetailsValueW')
    wind_speed_kmh=wind_speed_kmh_elems.text.strip()
    if wind_speed_kmh:
      wind_speed_knots=float(wind_speed_kmh)/1.852

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

  wind_gust_knots=None
  try:
    wind_gust_kmh_elem=soup.find('span', id='currentDetailsValueG')
    wind_gust_kmh=wind_gust_kmh_elem.text.strip()
    if wind_gust_kmh:
      wind_gust_knots=float(wind_gust_kmh)/1.852

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_gust_knots: "{e}"!')

  wind_direction_deg=None
  try:
    wind_direction_ele=soup.find('span', id='currentDetailsValueBDir')
    wind_direction=wind_direction_ele.text.strip()
    wind_direction_deg=utility.convert_wind_direction_to_deg(wind_direction)
    if wind_direction_deg is None:
      logging.info(f'{utility.get_identification_string(location_id, server_name)}, Unknown wind_direction: "{wind_direction}"!')

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  windrun_km=None
  try:
    windrun_ele=soup.find('span', id='currentDetailsValueWrToday')
    windrun=windrun_ele.text.strip()
    if windrun:
      windrun_km=float(windrun)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting windrun_km: "{e}"!')

  barometric_pressure_ssl_hPa=None
  try:
    barometric_pressure_ssl_ele=soup.find('span', id='currentDetailsValueP')
    barometric_pressure_ssl=barometric_pressure_ssl_ele.text.strip()
    if barometric_pressure_ssl:
      barometric_pressure_ssl_hPa=float(barometric_pressure_ssl)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting barometric_pressure_ssl_hPa: "{e}"!')

  barometric_pressure_wsl_hPa=None
  try:
    barometric_pressure_wsl_ele=soup.find('span', id='currentDetailsValuePst')
    barometric_pressure_wsl=barometric_pressure_wsl_ele.text.strip()
    if barometric_pressure_wsl:
      barometric_pressure_wsl_hPa=float(barometric_pressure_wsl)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting barometric_pressure_wsl_hPa: "{e}"!')

  solar_irradiance_wpsm=None
  try:
    solar_irradiance_ele=soup.find('span', id='currentDetailsValueS')
    solar_irradiance=solar_irradiance_ele.text.strip()
    if solar_irradiance:
      solar_irradiance_wpsm=float(solar_irradiance)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting solar_irradiance_wpsm: "{e}"!')

  uv_index=None
  try:
    uv_index_ele=soup.find('span', id='currentDetailsValueUV')
    uv_index_ele=uv_index_ele.text.strip()
    if uv_index_ele and not uv_index_ele=="--":
      uv_index=float(uv_index_ele)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting uv_index: "{e}"!')

  meteo_data_dict={}
  meteo_data_dict["timestamp_string"]=timestamp_string
  meteo_data_dict["timestamp_string_date"]=timestamp_string_date
  meteo_data_dict["timestamp_string_time"]=timestamp_string_time
  meteo_data_dict["current_weather"]=current_weather
  meteo_data_dict["temperature_cels"]=temperature_cels
  meteo_data_dict["perceived_temperature_cels"]=perceived_temperature_cels
  meteo_data_dict["dew_point_cels"]=dew_point_cels
  meteo_data_dict["heat_index_cels"]=heat_index_cels
  meteo_data_dict["humidex_cels"]=humidex_cels
  meteo_data_dict["wind_chill_cels"]=wind_chill_cels
  meteo_data_dict["wet_bulb_temperature_cels"]=wet_bulb_temperature_cels
  meteo_data_dict["rel_humidity"]=rel_humidity
  meteo_data_dict["absolute_humidity_gm3"]=absolute_humidity_gm3
  meteo_data_dict["saturated_vapor_pressure_hPa"]=saturated_vapor_pressure_hPa
  meteo_data_dict["rain_rate_mmh"]=rain_rate_mmh
  meteo_data_dict["rain_today_mm"]=rain_today_mm
  meteo_data_dict["wind_speed_knots"]=wind_speed_knots
  meteo_data_dict["wind_gust_knots"]=wind_gust_knots
  meteo_data_dict["wind_direction_deg"]=wind_direction_deg
  meteo_data_dict["windrun_km"]=windrun_km
  meteo_data_dict["barometric_pressure_ssl_hPa"]=barometric_pressure_ssl_hPa
  meteo_data_dict["barometric_pressure_wsl_hPa"]=barometric_pressure_wsl_hPa
  meteo_data_dict["solar_irradiance_wpsm"]=solar_irradiance_wpsm
  meteo_data_dict["uv_index"]=uv_index

  if log:
    utility.log_sample(location_id, server_name, meteo_data_dict)

  if not utility.check_minimum_data(location_id, server_name, meteo_data_dict):
    return last_seen_timestamp

  utility.save(location_id, server_name, meteo_data_dict)
  return timestamp_string

if __name__=="__main__":
  utility.test_starter(24) # Location id
