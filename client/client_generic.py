import requests
import csv
from datetime import datetime
from lxml import html
import requests
from fake_useragent import UserAgent

#
#
#
def get_tree(weather_station_url, location_id):
  
  user_agent = UserAgent().random 
  headers = {'User-Agent': user_agent}

  try:
    page = requests.get(weather_station_url, headers=headers)
  except Exception as e:
    logging.exception(f'Server: {location_id} exception in requests.get, {e}, weather_station_url: "{weather_station_url}".')
    return None

  try:
    tree = html.fromstring(page.text)    
  except Exception as e:
    logging.exception(f'Server: {location_id} exception in html.fromstring, {e}!')
    return None

  return tree

#
#
#
def scan_meteosystem_alike(last_seen_timestamp, server, save=True, log=True):

  location_id=server["location_id"]
  name=server["name"]
  weather_station_url=server["url"]

  tree = get_tree(weather_station_url, location_id)
  if tree is None:
    return last_seen_timestamp

  try:
    date_list = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > div.valori3 > strong:nth-child(1)")
    date_string=date_list[0].text.strip()

    time_list = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > div.valori3 > strong:nth-child(2)")
    time_string=time_list[0].text.strip()

    datetime_string=date_string+" "+time_string
    from datetime import datetime
    timestamp_obj=datetime.strptime(datetime_string, "%d/%m/%y %H.%M")
    timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
    if (log):  
      print("timestamp_string: {timestamp_string}")

    timestamp_string_date=timestamp_obj.strftime("%d/%m/%Y")
    if (log):  
      print("timestamp_string_date: {timestamp_string_date}")

    timestamp_string_time=timestamp_obj.strftime("%H:%M:%S")
    timestamp_ele=timestamp_string_time
    if (log):  
      print("timestamp_string_time: {timestamp_string_time}")

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception getting the timestamp: "{e}"!')
    return last_seen_timestamp

  if timestamp_string==last_seen_timestamp:
    # Weather station is not updating data
    logging.info(f'Server: {location_id},  {name}, timestamp_string: {timestamp_string}, last_seen_timestamp: {last_seen_timestamp}, skip saving!')
    # TODO Raise an alert
    return last_seen_timestamp

  wind_speed_knots_elems=None
  try:
    wind_speed_knots_elems = tree.xpath("/html/body/div/div[4]/table/tr/td[2]/table[1]/tr[2]/td/table/tr[17]/td[3]/div/strong")
    wind_speed_knots=wind_speed_knots_elems[0].text.strip()
    wind_speed_knots=wind_speed_knots.split(" ")[0].strip()
    wind_speed_knots=float(wind_speed_knots)/1.852
    if (log):
      print("wind_speed_knots_elems : {wind_speed_knots_elems}")

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception getting wind_speed_knots: "{e}"!')

  wind_direction_deg=None
  try:  
    wind_direction_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(18) > td:nth-child(3) > div > strong")
    wind_direction=wind_direction_ele[0].text
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
    elif wind_direction=="SSW":
      wind_direction_deg=202.5
    elif wind_direction=="SW":
      wind_direction_deg=225
    elif wind_direction=="WSW":
      wind_direction_deg=247.5
    elif wind_direction=="W":
      wind_direction_deg=270
    elif wind_direction=="WNW":
      wind_direction_deg=292.5
    elif wind_direction=="NW":
      wind_direction_deg=315
    elif wind_direction=="NNW":
      wind_direction_deg=337.5
    else:
      print("Unknown wind_direction: '{wind_direction}'!")
      wind_direction_deg=None

    if (log):
      print("wind_direction_deg: {wind_direction_deg}")

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception getting wind_direction_deg: "{e}"!')

  barometric_pressure_hPa=None
  try:
    barometric_pressure_hPa_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(7) > td:nth-child(3) > div > strong')
    barometric_pressure_hPa=float(barometric_pressure_hPa_ele[0].text.split(' ')[0].strip())
    if (log):
      print("barometric_pressure_hPa: {barometric_pressure_hPa}")

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception getting barometric_pressure_hPa: "{e}"!')

  rain_today_mm=None
  try:
    rain_today_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(21) > td.sfondotagmin > div > strong")
    rain_today_mm=float(rain_today_mm_ele[0].text.split(' ')[0].strip())
    if (log):
      print("rain_today_mm: {rain_today_mm}")

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception getting rain_today_mm: "{e}"!')

  rain_rate_mmph=None
  try:
    rain_rate_mmph_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(21) > td:nth-child(3) > div > strong")
    rain_rate_mmph=float(rain_rate_mmph_ele[0].text.split(' ')[0].strip())
    if (log):
      print("rain_rate_mmph: {rain_rate_mmph}")

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception getting rain_rate_mmph: "{e}"!')

  temperature_cels=None
  try:
    temperature_cels_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(3) > td:nth-child(3) > div > strong")
    temperature_cels=temperature_cels_ele[0].text.split("°")[0].strip()
    if (log):
      print("temperature_cels: {temperature_cels}")

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception getting temperature_cels: "{e}"!')

  rel_humidity=None
  try:
    rel_humidity_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(4) > td:nth-child(3) > div > strong")
    rel_humidity=rel_humidity_ele[0].text.split("%")[0].strip()
    rel_humidity=float(rel_humidity)/100
    if (log):
      print("rel_humidity: {rel_humidity}")

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception getting rel_humidity: "{e}"!')

  heat_index_cels=None
  try:
    heat_index_cels_ele=tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(6) > td:nth-child(3) > div > strong")
    heat_index_cels=heat_index_cels_ele[0].text.split("°")[0].strip()
    if (log):
      print("heat_index_cels: {heat_index_cels}")

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception getting heat_index_cels: "{e}"!')

  wind_gust_knots=None
  try:
    wind_gust_kmh_ele=tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(17) > td.sfondotagmax > div > strong")
    wind_gust_kmh=wind_gust_kmh_ele[0].text.split(" ")[0].strip()
    wind_gust_knots=float(wind_gust_kmh)/1.852
    if (log):
      print("wind_gust_knots: {wind_gust_knots}")
      
  except Exception as e:
    logging.exception(f'Server: {location_id}, exception getting wind_gust_knots: "{e}"!')

  dew_point_cels=None
  try:
    dew_point_cels_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(5) > td:nth-child(3) > div > strong')
    dew_point_cels=dew_point_cels_ele[0].text.split('°')[0].strip()
    if (log):
      logging.info(f'Server: {location_id}, dew_point_cels: {dew_point_cels}')

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception getting dew_point_cels: "{e}"!')

  wind_chill_cels=None
  try:
    wind_chill_cels_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(8) > td:nth-child(3) > div > strong')
    wind_chill_cels=wind_chill_cels_ele[0].text.split('°')[0].strip()
    if (log):
      logging.info(f'Server: {location_id}, wind_chill_cels: {wind_chill_cels}')

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception getting wind_chill_cels: "{e}"!')

  ground_temperature_cels=None
  try:
    ground_temperature_cels_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(11) > td:nth-child(3) > div > strong')
    ground_temperature_cels=ground_temperature_cels_ele[0].text.split('°')[0].strip()
    if (log):
      logging.info(f'Server: {location_id}, ground_temperature_cels: {ground_temperature_cels}')

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception getting ground_temperature_cels: "{e}"!')

  solar_irradiance_wpsm=None # Watts per square meter
  try:
    solar_irradiance_wpsm_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(13) > td:nth-child(3) > div > strong')
    solar_irradiance_wpsm=solar_irradiance_wpsm_ele[0].text.split(' ')[0].strip()
    if (log):
      logging.info(f'Server: {location_id}, solar_irradiance_wpsm: {solar_irradiance_wpsm}')

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception getting solar_irradiance_wpsm: "{e}"!')

  rel_leaf_wetness=None
  try:
    leaf_wetness_index_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(14) > td:nth-child(3) > div > strong')
    leaf_wetness_index=leaf_wetness_index_ele[0].text.strip() # Leaf wetness index: 0 (completely dry) to 15 (saturated).
    rel_leaf_wetness=float(leaf_wetness_index)/15
    if (log):
      logging.info(f'Server: {location_id}, rel_leaf_wetness: {rel_leaf_wetness}')

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception getting rel_leaf_wetness: "{e}"!')

  soil_moisture_cb=None # Centibars
  try:
    soil_moisture_cb_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(12) > td:nth-child(3) > div > strong')
    soil_moisture_cb=soil_moisture_cb_ele[0].text.split(' ')[0].strip()
    if (log):
      logging.info(f'Server: {location_id}, soil_moisture_cb: {soil_moisture_cb}')

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception getting soil_moisture_cb: "{e}"!')

  rain_this_month_mm=None
  try:
    rain_this_month_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(22) > td.sfondotagmin > div > strong")
    rain_this_month_mm=rain_this_month_mm_ele[0].text.split(' ')[0].strip()
    if (log):
      print("rain_this_month_mm: {rain_this_month_mm}")

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception rain_this_month_mm: "{e}"!')

  rain_this_year_mm=None
  try:
    rain_this_year_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(23) > td.sfondotagmin > div > strong")
    rain_this_year_mm=rain_this_year_mm_ele[0].text.split(' ')[0].strip()
    if (log):
      print("rain_this_year_mm: {rain_this_year_mm}")

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception rain_this_year_mm: "{e}"!')

  evapotranspiration_today_mm=None
  try:
    evapotranspiration_today_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(21) > td.sfondotagmax > div > strong")
    evapotranspiration_today_mm=evapotranspiration_today_mm_ele[0].text.split(' ')[0].strip()
    if (log):
      print("evapotranspiration_today_mm: {evapotranspiration_today_mm}")

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception evapotranspiration_today_mm: "{e}"!')

  evapotranspiration_this_month_mm=None
  try:
    evapotranspiration_this_month_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(22) > td.sfondotagmax > div > strong")
    evapotranspiration_this_month_mm=evapotranspiration_this_month_mm_ele[0].text.split(' ')[0].strip()
    if (log):
      print("evapotranspiration_this_month_mm: {evapotranspiration_this_month_mm}")

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception evapotranspiration_this_month_mm: "{e}"!')

  evapotranspiration_this_year_mm=None
  try:
    evapotranspiration_this_year_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(23) > td.sfondotagmax > div > strong ")
    evapotranspiration_this_year_mm=evapotranspiration_this_year_mm_ele[0].text.split(' ')[0].strip()
    if (log):
      print("evapotranspiration_this_year_mm: {evapotranspiration_this_year_mm}")

  except Exception as e:
    logging.exception(f'Server: {location_id}, exception evapotranspiration_this_year_mm: "{e}"!')

  uv_index=None
  if not(timestamp_string and (wind_speed_knots or wind_direction_deg or barometric_pressure_hPa or rain_today_mm or rain_rate_mmph or temperature_cels or rel_humidity or uv_index or heat_index_cels or wind_gust_knots or dew_point_cels or wind_chill_cels or ground_temperature_cels or solar_irradiance_wpsm or rel_leaf_wetness or soil_moisture_cb or rain_this_month_mm or rain_this_year_mm or evapotranspiration_today_mm or evapotranspiration_this_month_mm or evapotranspiration_this_year_mm)):
    logging.info(f'Server: {location_id}, Not enough scraped data. Skip saving data...')
    logging.info(f'Server: {location_id}, timestamp_string: {timestamp_string}, wind_speed_knots: {wind_speed_knots}, wind_direction_deg: {wind_direction_deg}, barometric_pressure_hPa: {barometric_pressure_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmph: {rain_rate_mmph},  temperature_cels: {temperature_cels}, rel_humidity: {rel_humidity}, uv_index: {uv_index}, heat_index_cels: {heat_index_cels}, wind_gust_knots: {wind_gust_knots}, dew_point_cels: {dew_point_cels}, wind_chill_cels: {wind_chill_cels}, ground_temperature_cels: {ground_temperature_cels}, solar_irradiance_wpsm: {solar_irradiance_wpsm}, rel_leaf_wetness: {rel_leaf_wetness}, soil_moisture_cb: {soil_moisture_cb}, rain_this_month_mm: {rain_this_month_mm}, rain_this_year_mm: {rain_this_year_mm}, evapotranspiration_today_mm: {evapotranspiration_today_mm}, evapotranspiration_this_month_mm: {evapotranspiration_this_month_mm}, evapotranspiration_this_year_mm: {evapotranspiration_this_year_mm}')
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
  # uv_index: not handled by this weather station
  #meteo_data_dict["uv_index"]=uv_index
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
    
  save_v6(location_id, name, meteo_data_dict)
  return timestamp_string

#
#
#
def save_v6(location_id, server_name, meteo_data_dict, save=True):

  if not save:
    logging.info(f'Server: {location_id}, {server_name}: Save disabled!')
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

  file_name=f"data/weather_{location_id}_{server_name}_v6.txt"
  import os
  from csv import writer
  try:
    with open(file_name, 'a+', newline='') as write_obj:
      csv_writer = writer(write_obj, delimiter=";")
      if os.stat(file_name).st_size == 0:
        csv_writer.writerow(csv_file_header)

      weather=[timestamp_string, timestamp_string_date, timestamp_string_time, wind_speed_knots, wind_direction_deg, barometric_pressure_hPa, rain_today_mm, rain_rate_mmph, temperature_cels, rel_humidity, uv_index, heat_index_cels, wind_gust_knots, dew_point_cels, wind_chill_cels, ground_temperature_cels, solar_irradiance_wpsm, rel_leaf_wetness, soil_moisture_cb, rain_this_month_mm, rain_this_year_mm, evapotranspiration_today_mm, evapotranspiration_this_month_mm, evapotranspiration_this_year_mm]
      csv_writer.writerow(weather)
  except Exception as e:
    logging.exception(f'Server: {location_id}, {server_name}: exception: {e} saving to csv file: {file_name}!')

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
    logging.exception(f'Server: {location_id}, {server_name}: exception: {e} POSTing to: {rest_server}!')

  logging.info(f'Server: {location_id}, {server_name}, {timestamp}, response {response}')

  return

#
#
#
def scan_meteonetwork_alike(last_seen_timestamp, server, save=True, log=True):
  location_id=server["location_id"]
  name=server["name"]
  weather_station_url=server["url"]

  tree = get_tree(weather_station_url, location_id)
  if tree is None:
    return last_seen_timestamp

  try:
    timestamp_list = tree.xpath('/html/body/div[3]/div[1]/div/h3[1]')
    timestamp_ele=timestamp_list[0].text
    # if (last_seen_timestamp == timestamp_ele):
    #   return timestamp_ele

    time_string=timestamp_ele[len('Dati in diretta (aggiornati alle '):len('Dati in diretta (aggiornati alle ')+5]
    date_string=timestamp_ele[43:43+10]
    datetime_string=date_string+" "+time_string
    from datetime import datetime
    timestamp_obj=datetime.strptime(datetime_string, "%d/%m/%Y %H:%M")
    timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
    if (log):  
      print("timestamp_string: {timestamp_string}")

    timestamp_string_date=timestamp_obj.strftime("%d/%m/%Y")
    if (log):
      print("timestamp_string_date: {timestamp_string_date}")

    timestamp_string_time=timestamp_obj.strftime("%H:%M:%S")
    if (log):
      print("timestamp_string_time: {timestamp_string_time}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  wind_speed=None
  try:
    wind_speed_elems = tree.xpath('/html/body/table/tbody/tr[2]/td[2]/h1[2]/big/big/big/span/text()')
    wind_speed=wind_speed_elems[0]
    wind_speed=wind_speed.strip()
    wind_speed=float(wind_speed)/1.852
    if (log):
      print("wind_speed: {wind_speed}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  wind_direction=None
  try:  
    wind_direction = tree.xpath('/html/body/table/tbody/tr[2]/td[2]/h4/big/big/span/big/big/text()')
    wind_direction=wind_direction[0]
    if (log):
      print("wind_direction: {wind_direction}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  pressure=None
  try:
    pressure_ele = tree.xpath('/html/body/table/tbody/tr[2]/td[3]/h1[2]/big/span')
    pressure=pressure_ele[0].text
    pressure=pressure.strip()
    if (log):
      print("pressure: {pressure}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  rain_today=None
  try:
    rain_today_ele = tree.xpath('/html/body/table/tbody/tr[4]/td[2]/h1[2]/big/span')
    rain_today=rain_today_ele[0].text
    rain_today=rain_today[:1]
    rain_today=rain_today.strip()
    if (log):
      print("rain_today: {rain_today}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  rain_rate=None
  try:
    rain_rate_ele = tree.xpath('/html/body/table/tbody/tr[4]/td[2]/h2')
    rain_rate=rain_rate_ele[0].text
    rain_rate=rain_rate[len('IntensitÃƒ'):]
    rain_rate=rain_rate[:3]
    rain_rate=rain_rate.strip()
    if (log):
      print("rain_rate: {rain_rate}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  temperature=None
  try:
    temperature_ele = tree.xpath('/html/body/table/tbody/tr[2]/td[1]/h1[3]/big/big/big')
    temperature=temperature_ele[0].text
    temperature=temperature[:len(temperature)-len("Â°C")+1]
    temperature=temperature.strip()
    if (log):
      print("temperature: {temperature}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  rel_humidity=None
  try:
    rel_humidity_ele = tree.xpath('/html/body/table/tbody/tr[3]/td/h1[2]/big/span')
    rel_humidity=rel_humidity_ele[0].text
    rel_humidity=rel_humidity[:len(rel_humidity)-len(" %")].strip()
    if (log):
      print("rel_humidity: {rel_humidity}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  uv_index=None
  try:
    uv_index_ele = tree.xpath('/html/body/table/tbody/tr[4]/td[1]/h1[2]/big/span')
    uv_index=uv_index_ele[0].text
    uv_index=uv_index.strip()
    if (log):
      print("uv_index: {uv_index}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  heat_index=None
  try:
    heat_index_cels_ele = tree.xpath('/html/body/table/tbody/tr[2]/td[1]/h3[4]/big/span')
    heat_index=heat_index_cels_ele[0].text
    heat_index=heat_index[len('Indice di calore: '):]
    heat_index=heat_index[:len(heat_index)-len("°C")-1]
    heat_index=heat_index.strip()
    if (log):
      print("heat_index: {heat_index}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  if not(timestamp_string and (wind_speed or wind_direction or pressure or rain_today or rain_rate or temperature or rel_humidity or uv_index or heat_index)):
    logging.info(f'Server: {location_id}, Not enough scraped data. Skip saving data...')
    logging.info(f'Server: {location_id}, timestamp_string: {timestamp_string}, wind_speed: {wind_speed}, wind_direction: {wind_direction}, pressure: {pressure}, rain_today: {rain_today}, rain_rate: {rain_rate},  temperature: {temperature}, rel_humidity: {rel_humidity}, uv_index: {uv_index}, heat_index: {heat_index}')
    return last_seen_timestamp

  # Backup to CSV file
  if (save):  
    wind_gust=None
    dew_point_cels=None
    weather=[timestamp_string, timestamp_string_date, timestamp_string_time, wind_speed, wind_direction, pressure, rain_today, rain_rate, temperature, rel_humidity, uv_index, heat_index, wind_gust, dew_point_cels]
    file_name=f"data/weather_{name}_v3.txt"
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
      rel_humidity=float(rel_humidity)/100

    data_json = {
      "location_id": location_id,   
      "timestamp_ws": timestamp,
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
    logging.info(f'Server: {location_id}, {name}, {timestamp}, response {response}')
  
  return timestamp_ele

#
#
#
def scan_hotelmarcopolo_caorle_alike(last_seen_timestamp, server, save=True, log=True):

  location_id=server["location_id"]
  name=server["name"]
  weather_station_url=server["url"]

  tree = get_tree(weather_station_url, location_id)
  if tree is None:
    return last_seen_timestamp

  timestamp_string=None
  try:
    timestamp_list = tree.xpath('/html/body/span')
    if (log):
      print(type(timestamp_list))
      for timestamp_ele in timestamp_list:
        print(type(timestamp_ele))
        print(timestamp_ele.text)

    timestamp_ele=timestamp_list[0].text
    # if (last_seen_timestamp == timestamp_ele):
    #   return timestamp_ele

    timestamp_string=timestamp_ele[-len('Dati in real-time aggiornati alle: ')+4:].strip()
    from datetime import datetime
    timestamp_obj=datetime.strptime(timestamp_string, "%a, %d %b %Y %H:%M:%S %z")
    timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
    if (log):
      print("timestamp_string: {timestamp_string}")

    timestamp_string_date=timestamp_obj.strftime("%d/%m/%Y")
    if (log):
      print("timestamp_string_date: {timestamp_string_date}")

    timestamp_string_time=timestamp_obj.strftime("%H:%M:%S")
    if (log):
      print("timestamp_string_time: {timestamp_string_time}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')
    return last_seen_timestamp

  wind_speed=None
  try:
    wind_speed_elems = tree.xpath('/html/body/table/tbody/tr[2]/td[2]/h1[2]/big/big/big/span/text()')
    wind_speed=wind_speed_elems[0]
    wind_speed=wind_speed.strip()
    wind_speed=float(wind_speed)/1.852
    if (log):
      print("wind_speed: {wind_speed}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  wind_direction=None
  try:  
    wind_direction = tree.xpath('/html/body/table/tbody/tr[2]/td[2]/h4/big/big/span/big/big/text()')
    wind_direction=wind_direction[0]
    if (log):
      print("wind_direction: {wind_direction}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  pressure=None
  try:
    pressure_ele = tree.xpath('/html/body/table/tbody/tr[2]/td[3]/h1[2]/big/span')
    pressure=pressure_ele[0].text
    pressure=pressure.strip()
    if (log):
      print("pressure: {pressure}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  rain_today=None
  try:
    rain_today_ele = tree.xpath('/html/body/table/tbody/tr[4]/td[2]/h1[2]/big/span')
    rain_today=rain_today_ele[0].text
    rain_today=rain_today.split()[0].strip()
    if (log):
      print("rain_today: {rain_today}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  rain_rate=None
  try:
    rain_rate_ele = tree.xpath('/html/body/table/tbody/tr[4]/td[2]/h2')
    rain_rate=rain_rate_ele[0].text
    rain_rate=rain_rate.split(" ")[1].strip()
    if (log):
      print("rain_rate: {rain_rate}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  temperature=None
  try:
    temperature_ele = tree.xpath('/html/body/table/tbody/tr[2]/td[1]/h1[3]/big/big/big')
    temperature=temperature_ele[0].text
    temperature=temperature[:len(temperature)-len("Â°C")+1]
    temperature=temperature.strip()
    if (log):
      print("temperature: {temperature}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  humidity=None
  try:
    humidity_ele = tree.xpath('/html/body/table/tbody/tr[3]/td/h1[2]/big/span')
    humidity=humidity_ele[0].text
    humidity=humidity[:len(humidity)-len(" %")]
    humidity=humidity.strip()
    if (log):
      print("humidity: {humidity}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  uv_index=None
  try:
    uv_index_ele = tree.xpath('/html/body/table/tbody/tr[4]/td[1]/h1[2]/big/span')
    uv_index=uv_index_ele[0].text
    uv_index=uv_index.strip()
    if (log):
      print("uv_index: {uv_index}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  heat_index=None
  try:
    heat_index_cels_ele = tree.xpath('/html/body/table/tbody/tr[2]/td[1]/h3[4]/big/span')
    heat_index=heat_index_cels_ele[0].text
    heat_index=heat_index[len('Indice di calore: '):]
    heat_index=heat_index[:len(heat_index)-len("°C")-1]
    heat_index=heat_index.strip()
    if (log):
      print("heat_index: {heat_index}")

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  if not(timestamp_string and (wind_speed or wind_direction or pressure or rain_today or rain_rate or temperature or humidity or uv_index or heat_index)):
    logging.info(f'Server: {location_id}, Not enough scraped data. Skip saving data...')
    logging.info(f'Server: {location_id}, timestamp_string: {timestamp_string}, wind_speed: {wind_speed}, wind_direction: {wind_direction}, pressure: {pressure}, rain_today: {rain_today}, rain_rate: {rain_rate},  temperature: {temperature}, humidity: {humidity}, uv_index: {uv_index}, heat_index: {heat_index}')
    return last_seen_timestamp

  # Backup to CSV file
  if (save):  
    wind_gust=None
    dew_point_cels=None
    weather=[timestamp_string, timestamp_string_date, timestamp_string_time, wind_speed, wind_direction, pressure, rain_today, rain_rate, temperature, humidity, uv_index, heat_index, wind_gust, dew_point_cels]
    file_name=f"data/weather_{name}_v3.txt"
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
      "location_id": location_id,
      "timestamp_ws": timestamp,
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
    logging.info(f'Server: {location_id}, {name}, {timestamp}, response {response}')
  
  return timestamp_ele

#
# Scanner for MeteoVenezia weather stations alike stations
#
def scan_meteovenezia_alike(last_seen_timestamp, server, save=True, log=True):

  location_id=server["location_id"]
  name=server["name"]
  weather_station_url=server["url"]

  tree = get_tree(weather_station_url, location_id)
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
    logging.exception(f'Server: {location_id}, {err}')

  wind_speed=None
  try:
    wind_speed_elem = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[1]')
    wind_speed=wind_speed_elem[0].text
    wind_speed=float(wind_speed)
    if (log):
      logging.info(f'Server: {location_id}, wind_speed: {wind_speed}')

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  wind_gust=None
  try:
    wind_gust_elem = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[3]')
    wind_gust=wind_gust_elem[0].text.strip()
    wind_gust=float(wind_gust)
    if (log):
      logging.info(f'Server: {location_id}, wind_gust: {wind_gust}')

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  wind_direction=None
  try:
    wind_direction = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[2]')
    wind_direction=wind_direction[0].text
    wind_direction=wind_direction.split('°')[0].strip()
    if (log):
      logging.info(f'Server: {location_id}, wind_direction: {wind_direction}')

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  pressure=None
  try:
    pressure_elem = tree.xpath('/html/body/div/table[2]/tbody/tr[11]/td[2]')
    pressure=pressure_elem[0].text
    pressure=pressure.split('hPa')[0].strip()
    if (log):
      logging.info(f'Server: {location_id}, pressure: {pressure}')

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

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
    logging.exception(f'Server: {location_id}, {err}')

  rain_rate=None
  try:
    rain_rate_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[12]/td[2]')
    rain_rate=rain_rate_ele[0].text
    rain_rate=rain_rate.split('mm/h')[0].strip()
    if (log):
      logging.info(f'Server: {location_id}, rain_rate: {rain_rate}')

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  temperature=None
  try:
    temperature_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[7]/td[2]')
    temperature=temperature_ele[0].text
    temperature=temperature.split('°')[0].strip()
    if (log):
      logging.info(f'Server: {location_id}, temperature: {temperature}')

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  humidity=None
  try:
    humidity_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[9]/td[2]')
    humidity=humidity_ele[0].text
    humidity=humidity[:len(humidity)-len(" %")].strip()
    if (log):
      logging.info(f'Server: {location_id}, humidity: {humidity}')

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  heat_index=None
  try:
    heat_index_cels_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[8]/td[2]')
    heat_index=heat_index_cels_ele[0].text
    heat_index=heat_index.split('°')[0]
    if (log):
      logging.info(f'Server: {location_id}, heat_index: {heat_index}')

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  dew_point_cels=None
  try:
    dew_point_cels_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[10]/td[2]')
    dew_point_cels=dew_point_cels_ele[0].text
    dew_point_cels=dew_point_cels.split('°')[0]
    if (log):
      logging.info(f'Server: {location_id}, dew_point_cels: {dew_point_cels}')

  except Exception as err:
    logging.exception(f'Server: {location_id}, {err}')

  uv_index=None # Unsupported by these weather stations
  if not(timestamp_string and (wind_speed or wind_direction or pressure or rain_today or rain_rate or temperature or humidity or uv_index or heat_index or wind_gust or dew_point_cels)):
    logging.info(f'Server: {location_id}, Not enough scraped data. Skip saving data...')
    logging.info(f'Server: {location_id}, timestamp_string: {timestamp_string}, wind_speed: {wind_speed}, wind_direction: {wind_direction}, pressure: {pressure}, rain_today: {rain_today}, rain_rate: {rain_rate},  temperature: {temperature}, humidity: {humidity}, uv_index: {uv_index}, heat_index: {heat_index}, wind_gust: {wind_gust}, dew_point_cels: {dew_point_cels}')
    return last_seen_timestamp

  # Backup to CSV file
  if (save):
    weather=[timestamp_string, timestamp_string_date, timestamp_string_time, wind_speed, wind_direction, pressure, rain_today, rain_rate, temperature, humidity, uv_index, heat_index, wind_gust, dew_point_cels]
    file_name=f"data/weather_{name}_v3.txt"
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
      "timestamp_ws": timestamp,
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
    logging.info(f'Server: {location_id}, {name}, {timestamp}, response {response}')
  
  return timestamp_ele

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
    "note": "Meteo station @ https://www.bibione-meteo.it/, Bibione, Venezia",
    "height_asl_m": 0
},{
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
},{
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
},{
    "name": 'Osservatorio meteorologico di I.I.S. Agrario “Antonio della Lucia” di Feltre (BL) ',
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
}]

servers = [
  { "location_id": 1,  "location": locations_json[4], "to_be_started": True, "name": "hotelmarcopolo_caorle", "url": "https://www.hotelmarcopolocaorle.it/meteo/hmpolocaorle.php", "scanner": scan_hotelmarcopolo_caorle_alike },
  { "location_id": 4,  "location": locations_json[0], "to_be_started": True, "name": "bagnomargherita_caorle", "url": "https://www.meteo-caorle.it/", "scanner": scan_meteovenezia_alike },
  { "location_id": 8,  "location": locations_json[1], "to_be_started": True, "name": "sangiorgio_venezia", "url": "https://www.meteo-venezia.net/compagnia01.php", "scanner": scan_meteovenezia_alike },
  { "location_id": 9,  "location": locations_json[2], "to_be_started": True, "name": "puntasangiuliano_mestre", "url": "https://www.meteo-venezia.net/", "scanner": scan_meteovenezia_alike },
  { "location_id": 10, "location": locations_json[3], "to_be_started": True, "name": "lagunaparkhotel_bibione", "url": "https://www.bibione-meteo.it/", "scanner": scan_meteovenezia_alike },
  { "location_id": 11, "location": locations_json[5], "to_be_started": False, "name": "meteonetwork_feltre", "url": "http://my.meteonetwork.it/station/vnt336/", "scanner": scan_meteonetwork_alike },
  { "location_id": 12, "location": locations_json[6], "to_be_started": True, "name": "agrario_feltre", "url": "http://www.meteosystem.com/dati/feltre/dati.php", "scanner": scan_meteosystem_alike }
]

#
#
#
def main_logger(server, save=True, log=False):
  logging.info(f'Thread ident: {threading.get_ident()}, Client for server: {server["location_id"]}, {server["name"]}, url: {server["url"]} up and running.')
  scanner=server["scanner"]
  while True:
    last_seen_timestamp=server.get("last_seen_timestamp", None)
    scan_no=server.get("scan_no", 0)
    scan_no=scan_no+1
    logging.info(f'Server: {server["location_id"]}, {server["name"]}, scan: {scan_no}...')
    last_seen_timestamp=scanner(last_seen_timestamp, server, save, log)
    server["last_seen_timestamp"]=last_seen_timestamp
    server["scan_no"]=scan_no
    time.sleep(50)

#
#
#
def add_server_location(server):
    location_json=server["location"]
    headers={'Content-Type': 'application/json; charset=utf-8'}
    response=requests.post('http://localhost:8080/api/location', headers = headers, json = location_json)
    logging.info(f'Location id: {server["location_id"]}, name: {server["name"]}, response: {response}')

#
#
#
def add_server_locations(servers):
  for server in servers:
    add_server_location(server)

#
#
#
import logging
import threading
import time

if __name__=="__main__":
  #add_server_locations(servers)
  format = "%(asctime)s %(thread)d %(threadName)s: %(message)s"
  logging.basicConfig(filename="app/log/meteo_data_repo3.log", format=format, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")
  nclients=0
  for server in servers:
    to_be_started=server["to_be_started"]
    if to_be_started==False:
      logging.info(f'Server: {server["location_id"]}, {server["name"]}, url: {server["url"]} starting DISABLED.')
      continue

    logging.info(f'Starting client for server: {server["location_id"]}, {server["name"]}, url: {server["url"]}...')
    threading.Thread(target=main_logger, args=(server, )).start()
    nclients=nclients+1

  logging.info(f'Clients starting complete. Started: {nclients} clients.')
