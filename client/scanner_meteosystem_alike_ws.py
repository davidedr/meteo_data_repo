from datetime import datetime
import logging

import utility

#
#
#
def scan_meteosystem_alike(last_seen_timestamp, server, save=True, log=True):

  location_id=server["location_id"]
  server_name=server["name"]
  weather_station_url=server["url"]

  tree, _ = utility.get_tree(weather_station_url, location_id)
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
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting the timestamp: "{e}"!')
    return last_seen_timestamp

  if timestamp_string==last_seen_timestamp:
    # Weather station is not updating data
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, last_seen_timestamp: {last_seen_timestamp}, skip saving!')
    # TODO Raise an alert
    return last_seen_timestamp

  wind_speed_knots_elem=None
  try:
    wind_speed_knots_elem = tree.xpath("/html/body/div/div[4]/table/tr/td[2]/table[1]/tr[2]/td/table/tr[17]/td[3]/div/strong")
    wind_speed_knots=wind_speed_knots_elem[0].text.strip()
    wind_speed_knots=wind_speed_knots.split(" ")[0].strip()
    wind_speed_knots=float(wind_speed_knots)/1.852

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

  wind_gust_knots=None
  try:
    wind_gust_kmh_ele=tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(17) > td.sfondotagmax > div > strong")
    wind_gust_kmh=wind_gust_kmh_ele[0].text.split(" ")[0].strip()
    wind_gust_knots=float(wind_gust_kmh)/1.852
      
  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_gust_knots: "{e}"!')

  wind_direction_deg=None
  try:  
    wind_direction_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(18) > td:nth-child(3) > div > strong")
    wind_direction=wind_direction_ele[0].text

    wind_direction_deg=utility.convert_wind_direction_to_deg(wind_direction)
    if not wind_direction_deg:
      logging.info(f'{utility.get_identification_string(location_id, server_name)}, Unknown wind_direction: "{wind_direction}"!')

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  barometric_pressure_hPa=None
  try:
    barometric_pressure_hPa_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(7) > td:nth-child(3) > div > strong')
    barometric_pressure_hPa=float(barometric_pressure_hPa_ele[0].text.split(' ')[0].strip())

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting barometric_pressure_hPa: "{e}"!')

  rain_today_mm=None
  try:
    rain_today_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(21) > td.sfondotagmin > div > strong")
    rain_today_mm=float(rain_today_mm_ele[0].text.split(' ')[0].strip())

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  rain_rate_mmph=None
  try:
    rain_rate_mmph_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(21) > td:nth-child(3) > div > strong")
    rain_rate_mmph=float(rain_rate_mmph_ele[0].text.split(' ')[0].strip())

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_rate_mmph: "{e}"!')

  temperature_cels=None
  try:
    temperature_cels_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(3) > td:nth-child(3) > div > strong")
    temperature_cels=temperature_cels_ele[0].text.split("°")[0].strip()

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  rel_humidity=None
  try:
    rel_humidity_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(4) > td:nth-child(3) > div > strong")
    rel_humidity=rel_humidity_ele[0].text.split("%")[0].strip()
    rel_humidity=float(rel_humidity)/100

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  heat_index_cels=None
  try:
    heat_index_cels_ele=tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(6) > td:nth-child(3) > div > strong")
    heat_index_cels=heat_index_cels_ele[0].text.split("°")[0].strip()

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting heat_index_cels: "{e}"!')

  dew_point_cels=None
  try:
    dew_point_cels_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(5) > td:nth-child(3) > div > strong')
    dew_point_cels=dew_point_cels_ele[0].text.split('°')[0].strip()

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting dew_point_cels: "{e}"!')

  wind_chill_cels=None
  try:
    wind_chill_cels_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(8) > td:nth-child(3) > div > strong')
    wind_chill_cels=wind_chill_cels_ele[0].text.split('°')[0].strip()

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_chill_cels: "{e}"!')

  ground_temperature_cels=None
  try:
    ground_temperature_cels_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(11) > td:nth-child(3) > div > strong')
    ground_temperature_cels=ground_temperature_cels_ele[0].text.split('°')[0].strip()

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting ground_temperature_cels: "{e}"!')

  solar_irradiance_wpsm=None # Watts per square meter
  try:
    solar_irradiance_wpsm_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(13) > td:nth-child(3) > div > strong')
    solar_irradiance_wpsm=solar_irradiance_wpsm_ele[0].text.split(' ')[0].strip()

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting solar_irradiance_wpsm: "{e}"!')

  rel_leaf_wetness=None
  try:
    leaf_wetness_index_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(14) > td:nth-child(3) > div > strong')
    leaf_wetness_index=leaf_wetness_index_ele[0].text.strip() # Leaf wetness index: 0 (completely dry) to 15 (saturated).
    rel_leaf_wetness=float(leaf_wetness_index)/15

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rel_leaf_wetness: "{e}"!')

  soil_moisture_cb=None # Centibars
  try:
    soil_moisture_cb_ele = tree.cssselect('body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(12) > td:nth-child(3) > div > strong')
    soil_moisture_cb=soil_moisture_cb_ele[0].text.split(' ')[0].strip()

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting soil_moisture_cb: "{e}"!')

  rain_this_month_mm=None
  try:
    rain_this_month_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(22) > td.sfondotagmin > div > strong")
    rain_this_month_mm=rain_this_month_mm_ele[0].text.split(' ')[0].strip()

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception rain_this_month_mm: "{e}"!')

  rain_this_year_mm=None
  try:
    rain_this_year_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(23) > td.sfondotagmin > div > strong")
    rain_this_year_mm=rain_this_year_mm_ele[0].text.split(' ')[0].strip()

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception rain_this_year_mm: "{e}"!')

  evapotranspiration_today_mm=None
  try:
    evapotranspiration_today_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(21) > td.sfondotagmax > div > strong")
    evapotranspiration_today_mm=evapotranspiration_today_mm_ele[0].text.split(' ')[0].strip()

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception evapotranspiration_today_mm: "{e}"!')

  evapotranspiration_this_month_mm=None
  try:
    evapotranspiration_this_month_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(22) > td.sfondotagmax > div > strong")
    evapotranspiration_this_month_mm=evapotranspiration_this_month_mm_ele[0].text.split(' ')[0].strip()

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception evapotranspiration_this_month_mm: "{e}"!')

  evapotranspiration_this_year_mm=None
  try:
    evapotranspiration_this_year_mm_ele = tree.cssselect("body > div.interno > div:nth-child(4) > table > tr > td:nth-child(2) > table:nth-child(5) > tr:nth-child(2) > td > table > tr:nth-child(23) > td.sfondotagmax > div > strong ")
    evapotranspiration_this_year_mm=evapotranspiration_this_year_mm_ele[0].text.split(' ')[0].strip()

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception evapotranspiration_this_year_mm: "{e}"!')

  uv_index=None 
  if (log):
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, wind_speed_knots: {wind_speed_knots}, wind_direction_deg: {wind_direction_deg}, barometric_pressure_hPa: {barometric_pressure_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmph: {rain_rate_mmph},  temperature_cels: {temperature_cels}, rel_humidity: {rel_humidity}, uv_index: {uv_index}, heat_index_cels: {heat_index_cels}, wind_gust_knots: {wind_gust_knots}, dew_point_cels: {dew_point_cels}, wind_chill_cels: {wind_chill_cels}, ground_temperature_cels: {ground_temperature_cels}, solar_irradiance_wpsm: {solar_irradiance_wpsm}, rel_leaf_wetness: {rel_leaf_wetness}, soil_moisture_cb: {soil_moisture_cb}, rain_this_month_mm: {rain_this_month_mm}, rain_this_year_mm: {rain_this_year_mm}, evapotranspiration_today_mm: {evapotranspiration_today_mm}, evapotranspiration_this_month_mm: {evapotranspiration_this_month_mm}, evapotranspiration_this_year_mm: {evapotranspiration_this_year_mm}')

  # UV-index is not supported by this wather station
  if not(timestamp_string and (wind_speed_knots or wind_direction_deg or barometric_pressure_hPa or rain_today_mm or rain_rate_mmph or temperature_cels or rel_humidity or uv_index or heat_index_cels or wind_gust_knots or dew_point_cels or wind_chill_cels or ground_temperature_cels or solar_irradiance_wpsm or rel_leaf_wetness or soil_moisture_cb or rain_this_month_mm or rain_this_year_mm or evapotranspiration_today_mm or evapotranspiration_this_month_mm or evapotranspiration_this_year_mm)):
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, Not enough scraped data. Skip saving data...')
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, wind_speed_knots: {wind_speed_knots}, wind_direction_deg: {wind_direction_deg}, barometric_pressure_hPa: {barometric_pressure_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmph: {rain_rate_mmph},  temperature_cels: {temperature_cels}, rel_humidity: {rel_humidity}, uv_index: {uv_index}, heat_index_cels: {heat_index_cels}, wind_gust_knots: {wind_gust_knots}, dew_point_cels: {dew_point_cels}, wind_chill_cels: {wind_chill_cels}, ground_temperature_cels: {ground_temperature_cels}, solar_irradiance_wpsm: {solar_irradiance_wpsm}, rel_leaf_wetness: {rel_leaf_wetness}, soil_moisture_cb: {soil_moisture_cb}, rain_this_month_mm: {rain_this_month_mm}, rain_this_year_mm: {rain_this_year_mm}, evapotranspiration_today_mm: {evapotranspiration_today_mm}, evapotranspiration_this_month_mm: {evapotranspiration_this_month_mm}, evapotranspiration_this_year_mm: {evapotranspiration_this_year_mm}')
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
    
  utility.save_v6(location_id, server_name, meteo_data_dict)
  return timestamp_string
