from datetime import datetime
import logging

import utility

#
# Scanner for MeteoVenezia weather stations alike stations
#
def scan_osservatorio_metereologico_festisei_alike(last_seen_timestamp, server, save=True, log=True):

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
    timestamp_list=tree.xpath('/html/body/div/div/div[2]/div/strong[1]')
    timestamp_date_string=timestamp_list[0].text
    
    timestamp_list=tree.xpath('/html/body/div/div/div[2]/div/strong[2]')
    timestamp_time_string=timestamp_list[0].text

    timestamp_datetime_string=timestamp_date_string+" "+timestamp_time_string
    timestamp_date_obj=datetime.strptime(timestamp_datetime_string, "%d/%m/%y %H:%M")
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

  wind_speed_knots=None
  try:
    wind_speed_kmh_elem=tree.xpath('/html/body/div/div/div[2]/table[1]/tr[12]/td[3]/div/strong')
    wind_speed_kmh=wind_speed_kmh_elem[0].text.strip().split(" ")[0].strip()
    if wind_speed_kmh:
      wind_speed_knots=float(wind_speed_kmh)/1.852

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

  wind_direction_deg=None
  try:
    wind_direction_ele=tree.xpath('/html/body/div/div/div[2]/table[1]/tr[13]/td[3]/div/strong ')
    wind_direction=wind_direction_ele[0].text.strip()
    wind_direction_deg=utility.convert_wind_direction_to_deg(wind_direction)
    if not wind_direction_deg:
      logging.info(f'{utility.get_identification_string(location_id, server_name)}, Unknown wind_direction: "{wind_direction}"!')

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  barometric_pressure_ssl_hPa=None
  try:
    barometric_pressure_ssl_ele=tree.xpath('/html/body/div/div/div[2]/table[1]/tr[8]/td[3]/div/strong')
    barometric_pressure_ssl=barometric_pressure_ssl_ele[0].text.strip().split(" ")[0].strip()
    if barometric_pressure_ssl:
      barometric_pressure_ssl_hPa=float(barometric_pressure_ssl)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting barometric_pressure_ssl_hPa: "{e}"!')

  rain_today_mm=None
  try:
    rain_today_ele = tree.xpath('/html/body/div/div/div[2]/table[1]/tr[15]/td[4]/div/div/strong')
    rain_today=rain_today_ele[0].text.strip().split(" ")[0].strip()
    if rain_today:
      rain_today_mm=float(rain_today)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  rain_rate_mmh=None
  try:
    rain_rate_ele=tree.xpath('/html/body/div/div/div[2]/table[1]/tr[15]/td[3]/div/div/strong')
    rain_rate=rain_rate_ele[0].text.strip().split(" ")[0].strip()
    if rain_rate:
      rain_rate_mmh=float(rain_rate)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_rate_mmh: "{e}"!')

  temperature_cels=None
  try:
    temperature_ele=tree.xpath('/html/body/div/div/div[2]/table[1]/tr[4]/td[3]/div/strong')
    temperature=temperature_ele[0].text.strip().split("°")[0].strip()
    if temperature:
      temperature_cels=float(temperature)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  rel_humidity=None
  try:
    humidity_ele=tree.xpath('/html/body/div/div/div[2]/table[1]/tr[5]/td[3]/div/strong')
    humidity=humidity_ele[0].text.strip().split("%")[0].strip()
    if humidity:
      rel_humidity=float(humidity)/100

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  heat_index_cels=None
  try:
    heat_index_ele=tree.xpath('/html/body/div/div/div[2]/table[1]/tr[7]/td[3]/div/strong')
    heat_index=heat_index_ele[0].text.strip().split("°")[0].strip()
    if heat_index:
      heat_index_cels=float(heat_index)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting heat_index_cels: "{e}"!')

  wind_gust_knots=None
  try:
    wind_gust_kmh_elem=tree.xpath('/html/body/div/div/div[2]/table[1]/tr[12]/td[6]/div/div/strong')
    wind_gust_kmh=wind_gust_kmh_elem[0].text.strip().split(" ")[0].strip()
    if wind_gust_kmh:
      wind_gust_knots=float(wind_gust_kmh)/1.852
  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_gust_knots: "{e}"!')

  dew_point_cels=None
  try:
    dew_point_ele=tree.xpath('/html/body/div/div/div[2]/table[1]/tr[6]/td[3]/div/strong')
    dew_point=dew_point_ele[0].text.strip().split("°")[0].strip()
    if dew_point:
      dew_point_cels=float(dew_point)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting dew_point_cels: "{e}"!')

  wind_chill_cels=None
  try:
    wind_chill_ele=tree.xpath('/html/body/div/div/div[2]/table[1]/tr[9]/td[3]/div/strong')
    wind_chill=wind_chill_ele[0].text.strip().split("°")[0].replace(",", ".")
    if wind_chill:
      wind_chill_cels=float(wind_chill)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_chill_cels: "{e}"!')

  ground_temperature_cels=None
  try:
    ground_temperature_ele=tree.xpath('/html/body/div/div/div[2]/table[1]/tr[19]/td[3]/div/strong')
    ground_temperature=ground_temperature_ele[0].text.strip().split("°")[0].strip()
    if ground_temperature:
      ground_temperature_cels=float(ground_temperature)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting ground_temperature_cels: "{e}"!')

  solar_irradiance_wpsm=None
  try:
    solar_irradiance_ele=tree.xpath('/html/body/div/div/div[2]/table[1]/tr[10]/td[3]/div/strong')
    solar_irradiance=solar_irradiance_ele[0].text.strip().split(" ")[0].strip()
    if solar_irradiance and solar_irradiance!="---":
      solar_irradiance_wpsm=float(solar_irradiance)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting solar_irradiance_wpsm: "{e}"!')

  rel_leaf_wetness=None
  try:
    leaf_wetness_index_ele=tree.xpath('/html/body/div/div/div[2]/table[1]/tr[21]/td[3]/div/strong')
    leaf_wetness_index=leaf_wetness_index_ele[0].text.strip() # Leaf wetness index: 0 (completely dry) to 15 (saturated).
    if leaf_wetness_index:
      rel_leaf_wetness=float(leaf_wetness_index)/15

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rel_leaf_wetness: "{e}"!')

  soil_moisture_cb=None # Centibars
  try:
    soil_moisture_ele=tree.xpath('/html/body/div/div/div[2]/table[1]/tr[20]/td[3]/div/strong')
    soil_moisture=soil_moisture_ele[0].text.split(' ')[0].strip()
    if soil_moisture:
      soil_moisture_cb=float(soil_moisture)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting soil_moisture_cb: "{e}"!')

  rain_this_month_mm=None
  try:
    rain_this_month_ele = tree.xpath('/html/body/div/div/div[2]/table[1]/tr[16]/td[4]/div/div/strong')
    rain_this_month=rain_this_month_ele[0].text.strip().split(" ")[0].strip()
    if rain_this_month:
      rain_this_month_mm=float(rain_this_month)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_this_month_mm: "{e}"!')

  rain_this_year_mm=None
  try:
    rain_this_year_ele = tree.xpath('/html/body/div/div/div[2]/table[1]/tr[17]/td[4]/div/div/strong')
    rain_this_year=rain_this_year_ele[0].text.strip().split(" ")[0].strip()
    if rain_this_year:
      rain_this_year_mm=float(rain_this_year)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_this_year_mm: "{e}"!')

  evapotranspiration_today_mm=None
  try:
    evapotranspiration_today_ele=tree.xpath('/html/body/div/div/div[2]/table[1]/tr[15]/td[6]/div/strong')
    evapotranspiration_today=evapotranspiration_today_ele[0].text.strip().split(" ")[0].strip()
    if evapotranspiration_today and evapotranspiration_today!="---":
      evapotranspiration_today_mm=float(evapotranspiration_today)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting evapotranspiration_today_mm: "{e}"!')

  evapotranspiration_this_month_mm=None
  try:
    evapotranspiration_this_month_ele=tree.xpath('/html/body/div/div/div[2]/table[1]/tr[16]/td[6]/div/strong')
    evapotranspiration_this_month=evapotranspiration_this_month_ele[0].text.strip().split(" ")[0].strip()
    if evapotranspiration_this_month and evapotranspiration_this_month!="---":
      evapotranspiration_this_month_mm=float(evapotranspiration_this_month)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting evapotranspiration_this_month_mm: "{e}"!')

  evapotranspiration_this_year_mm=None
  try:
    evapotranspiration_this_year_ele=tree.xpath('/html/body/div/div/div[2]/table[1]/tr[17]/td[6]/div/strong')
    evapotranspiration_this_year=evapotranspiration_this_year_ele[0].text.strip().split(" ")[0].strip()
    if evapotranspiration_this_year and evapotranspiration_this_year!="---":
      evapotranspiration_this_year_mm=float(evapotranspiration_this_year)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting evapotranspiration_this_year_mm: "{e}"!')

  perceived_temperature_cels=wind_chill_cels

  average_wind_speed_knots=None
  try:
    average_wind_speed_ele=tree.xpath("/html/body/div/div/div[2]/table[1]/tr[12]/td[4]/div/strong")
    average_wind_speed=average_wind_speed_ele[0].text.split(" ")[0].strip()
    if average_wind_speed:
      average_wind_speed_knots=float(average_wind_speed)/1.852

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting average_wind_speed_knots: "{e}"!')

  rain_in_last_storm_event_mm=None
  try:
    rain_in_last_storm_event_ele=tree.xpath("/html/body/div/div/div[2]/table[1]/tr[17]/td[3]/div/div/strong")
    rain_in_last_storm_event=rain_in_last_storm_event_ele[0].text.split(' ')[0].strip()
    if rain_in_last_storm_event:
      rain_in_last_storm_event_mm=float(rain_in_last_storm_event)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception rain_in_last_storm_event_mm: "{e}"!')

  meteo_data_dict={}
  meteo_data_dict["timestamp_string"]=timestamp_string
  meteo_data_dict["timestamp_string_date"]=timestamp_string_date
  meteo_data_dict["timestamp_string_time"]=timestamp_string_time
  meteo_data_dict["wind_speed_knots"]=wind_speed_knots
  meteo_data_dict["wind_direction_deg"]=wind_direction_deg
  meteo_data_dict["barometric_pressure_ssl_hPa"]=barometric_pressure_ssl_hPa
  meteo_data_dict["rain_today_mm"]=rain_today_mm
  meteo_data_dict["rain_rate_mmh"]=rain_rate_mmh
  meteo_data_dict["temperature_cels"]=temperature_cels
  meteo_data_dict["rel_humidity"]=rel_humidity
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
  meteo_data_dict["perceived_temperature_cels"]=perceived_temperature_cels
  meteo_data_dict["average_wind_speed_knots"]=average_wind_speed_knots
  meteo_data_dict["rain_in_last_storm_event_mm"]=rain_in_last_storm_event_mm

  if log:
    utility.log_sample(location_id, server_name, meteo_data_dict)

  if not(timestamp_string and (wind_speed_knots or wind_direction_deg or barometric_pressure_ssl_hPa or rain_today_mm or rain_rate_mmh or temperature_cels or rel_humidity or wind_gust_knots or perceived_temperature_cels)):
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, Not enough scraped data. Skip saving data...')
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, wind_speed_knots: {wind_speed_knots}, wind_direction_deg: {wind_direction_deg}, barometric_pressure_ssl_hPa: {barometric_pressure_ssl_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmh: {rain_rate_mmh}, temperature_cels: {temperature_cels}, rel_humidity: {rel_humidity}, wind_gust_knots: {wind_gust_knots}, perceived_temperature_cels: {perceived_temperature_cels}.')
    return last_seen_timestamp

  utility.save_v11(location_id, server_name, meteo_data_dict)
  return timestamp_string

if __name__=="__main__":
  utility.test_starter(21) # Location id
