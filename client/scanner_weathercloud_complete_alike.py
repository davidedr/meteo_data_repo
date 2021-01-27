from datetime import datetime
import logging
import platform
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
import time

import utility

#
# Scanner for Weathercloud weather stations alike stations
#
def scan_weathercloud_complete_alike(last_seen_timestamp, server, save=True, log=True):

  use_driver="Selenium"
  use_driver="Chrome"
  
  location_id=server["location_id"]
  server_name=server["name"]
  weather_station_url=server["url"]

  if isinstance(weather_station_url, dict):
    weather_station_url=weather_station_url.get("1")

  soup=None
  if use_driver=="Chrome":
    try:
      chrome_options=Options()
      chrome_options.add_argument("--headless")
      driver = webdriver.Chrome('./utility/chromedriver/chromedriver.exe', options=chrome_options)
      driver.get(weather_station_url)
      print(f'{utility.get_identification_string(location_id, server_name)}, url: 1, Driver sleeping 15s...')
      time.sleep(15)
      page_source=driver.page_source
      driver.quit()
      print(f'{utility.get_identification_string(location_id, server_name)}, url: 1, Driver quit.')
      soup = BeautifulSoup(page_source, "html.parser")

    except Exception as e:
      logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting getting webpage: "{e}"!')
      return last_seen_timestamp

  else:
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
      time.sleep(15)
      soup = BeautifulSoup(browser.page_source, "html.parser")

    except Exception as e:
      logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting getting webpage: "{e}"!')
      return last_seen_timestamp

  if soup is None:
      logging.info(f'{utility.get_identification_string(location_id, server_name)}, soup is None: "{soup}"!')
      return last_seen_timestamp

  timestamp_string=None
  timestamp_string_date=None
  timestamp_string_time=None
  try:
    timestamp_time=soup.find('span', id='header-localtime-container')
    timestamp_time_string=timestamp_time.text

    timestamp_date_string=datetime.today().strftime("%d/%m/%Y")
  
    timestamp_datetime_string=timestamp_date_string+" "+timestamp_time_string
    timestamp_date_obj=datetime.strptime(timestamp_datetime_string, "%d/%m/%Y %I:%M %p")
    timestamp_string=timestamp_date_obj.strftime("%d/%m/%Y %H:%M:%S")

    if timestamp_string==last_seen_timestamp:
      # Weather station is not updating data
      logging.info(f'{utility.get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, last_seen_timestamp: {last_seen_timestamp}, skip saving!')
      # TODO Raise an alert
      return last_seen_timestamp

    timestamp_string_date=timestamp_date_obj.strftime("%d/%m/%Y")
    timestamp_string_time=timestamp_date_obj.strftime("%H:%M:%S")

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting timestamp: "{e}"!')

  current_weather=None
  try:
    current_weather=soup.find('a', id='present-weather-string')["title"]

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting current_weather: "{e}"!')

  temperature_cels=None
  try:
    temperature_ele=soup.find('span', id='temp_cur')
    temperature=temperature_ele.text.strip()
    if temperature:
      temperature_cels=float(temperature)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  perceived_temperature_cels=None
  try:
    perceived_temperature_ele=soup.find('span', id='temp_feels')
    perceived_temperature=perceived_temperature_ele.text
    if perceived_temperature:
      perceived_temperature_cels=float(perceived_temperature)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting perceived_temperature_cels: "{e}"!')

  wind_direction_deg=None
  try:
    wind_direction_ele=soup.findAll('path', {"class": 'wind' })
    wind_direction=wind_direction_ele[0]["transform"].strip().split("(")[1].split(",")[0]
    wind_direction=float(wind_direction)
    if wind_direction>360:
      wind_direction=wind_direction-360
    if wind_direction<0:
      wind_direction=wind_direction+360
    if wind_direction:
      wind_direction_deg=wind_direction

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  wind_force_beaufort_desc=None
  try:
    wind_force_beaufort_desc_ele=soup.find('span', id='wdir_cur')
    wind_force_beaufort=wind_force_beaufort_desc_ele.text
    if wind_force_beaufort:
      wind_force_beaufort_desc=wind_force_beaufort
      
  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_force_beaufort_desc: "{e}"!')

  barometric_pressure_ssl_hPa=None
  try:
    barometric_pressure_ssl_ele=soup.find('span', id='bar_cur')
    barometric_pressure_ssl=barometric_pressure_ssl_ele.text.strip()
    if barometric_pressure_ssl:
      barometric_pressure_ssl_hPa=float(barometric_pressure_ssl)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting barometric_pressure_ssl_hPa: "{e}"!')

  cloud_height_m=None
  try:
    cloud_height_ele=soup.find('span', id='clouds')
    cloud_height=cloud_height_ele.text.strip()
    if cloud_height:
      cloud_height_m=float(cloud_height)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting cloud_height_m: "{e}"!')

  #
  #
  #
  weather_station_url=server["url"]
  if isinstance(weather_station_url, dict):
    weather_station_url=weather_station_url.get("2")

  soup=None
  if use_driver=="Chrome":
    try:
      chrome_options=Options()
      chrome_options.add_argument("--headless")
      driver = webdriver.Chrome('./utility/chromedriver/chromedriver.exe', options=chrome_options)
      driver.get(weather_station_url)
      print(f'{utility.get_identification_string(location_id, server_name)}, url: 2, Driver sleeping 15s...')
      time.sleep(30)
      page_source=driver.page_source
      driver.quit()
      print(f'{utility.get_identification_string(location_id, server_name)}, url: 2, Driver quit.')
      soup = BeautifulSoup(page_source, "html.parser")

    except Exception as e:
      logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting getting webpage: "{e}"!')
      return last_seen_timestamp

  else:
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
      time.sleep(30)
      soup = BeautifulSoup(browser.page_source, "html.parser")

    except Exception as e:
      logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting getting webpage: "{e}"!')
      return last_seen_timestamp

  if soup is None:
      logging.info(f'{utility.get_identification_string(location_id, server_name)}, soup is None: "{soup}"!')
      return last_seen_timestamp

  wind_speed_knots=None
  try:
    wind_speed_mps_ele=soup.findAll('span', {"class": 'pull-right' })[1]
    wind_speed_mps=wind_speed_mps_ele.text.split(" ")[0].strip()
    if wind_speed_mps:
      wind_speed_knots=float(wind_speed_mps)*1.94384

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

  wind_direction_deg_2=None
  try:  
    wind_direction_ele_2=soup.findAll('span', {"class": 'pull-right' })[1]
    wind_direction_2=wind_direction_ele_2.text.split(" ")[2].strip()
    wind_direction_deg_2=utility.convert_wind_direction_to_deg(wind_direction_2)
    if not wind_direction_deg_2:
      logging.info(f'{utility.get_identification_string(location_id, server_name)}, Unknown wind_direction: "{wind_direction_deg_2}"!')

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')
  
  if wind_direction_deg_2:
    wind_direction_deg=wind_direction_deg_2

  rel_humidity=None
  try:
    humidity=soup.findAll('span', {"class": 'pull-right' })[3].text.split(" ")[0].strip()
    if humidity:
      rel_humidity=float(humidity)/100

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  temperature_cels_2=None
  try:
    temperature_ele_2=soup.findAll('span', {"class": 'pull-right' })[2]
    temperature_2=temperature_ele_2.text.split(" ")[0].strip()
    if temperature_2:
      temperature_cels_2=float(temperature_2)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting temperature_cels_2: "{e}"!')

  if temperature_cels_2:
    temperature_cels=temperature_cels_2

  barometric_pressure_ssl_hPa_2=None
  try:
    barometric_pressure_ssl_ele_2=soup.findAll('span', {"class": 'pull-right' })[4]
    barometric_pressure_ssl_2=barometric_pressure_ssl_ele_2.text.split(" ")[0].strip()
    if barometric_pressure_ssl_2:
      barometric_pressure_ssl_hPa_2=float(barometric_pressure_ssl_2)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting barometric_pressure_ssl_hPa_2: "{e}"!')

  if barometric_pressure_ssl_hPa_2:
    barometric_pressure_ssl_hPa=barometric_pressure_ssl_hPa_2

  rain_today_mm=None
  try:
    rain_today=soup.findAll('span', {"class": 'pull-right' })[5].text.split(" ")[0].strip()
    rain_today_mm=float(rain_today)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  rain_rate_mmh=None
  try:
    rain_rate=soup.findAll('span', {"class": 'pull-right' })[6].text.split(" ")[0].strip()
    if rain_rate:
      rain_rate_mmh=float(rain_rate)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_rate_mmh: "{e}"!')

  uv_index=None
  try:
    uv_index_ele=soup.findAll('span', {"class": 'pull-right' })[7]
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
  meteo_data_dict["perceived_temperature_cels"]=perceived_temperature_cels
  meteo_data_dict["wind_direction_deg"]=wind_direction_deg
  meteo_data_dict["wind_force_beaufort_desc"]=wind_force_beaufort_desc
  meteo_data_dict["cloud_height_m"]=cloud_height_m
  meteo_data_dict["wind_speed_knots"]=wind_speed_knots
  meteo_data_dict["rel_humidity"]=rel_humidity
  meteo_data_dict["temperature_cels"]=temperature_cels
  meteo_data_dict["barometric_pressure_ssl_hPa"]=barometric_pressure_ssl_hPa
  meteo_data_dict["rain_today_mm"]=rain_today_mm
  meteo_data_dict["rain_rate_mmh"]=rain_rate_mmh
  meteo_data_dict["uv_index"]=uv_index
  
  if log:
    utility.log_sample(location_id, server_name, meteo_data_dict)

  if not utility.check_minimum_data(location_id, server_name, meteo_data_dict):
    return last_seen_timestamp

  utility.save(location_id, server_name, meteo_data_dict)
  return timestamp_string

if __name__=="__main__":
  utility.test_starter(26) # Location id
