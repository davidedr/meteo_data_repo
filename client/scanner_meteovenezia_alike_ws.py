from datetime import datetime
import logging
import utility

from utility import log_xpath_elem, convert_wind_direction_to_deg, get_identification_string, get_tree, save_v6

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
    timestamp_ele_1=timestamp_ele[0].strip()
    timestamp_ele_2=timestamp_ele[1].strip()

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
    wind_speed_elem = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[1]')
    wind_speed=wind_speed_elem[0].text
    if wind_speed:
      wind_speed_knots=float(wind_speed)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

  wind_gust_knots=None
  try:
    wind_gust_elem = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[3]')
    wind_gust=wind_gust_elem[0].text.strip()
    if wind_gust:
      wind_gust_knots=float(wind_gust)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_gust_knots: "{e}"!')

  wind_direction_deg=None
  try:
    wind_direction_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[3]/td[2]')
    wind_direction=wind_direction_ele[0].text
    wind_direction=wind_direction.split('°')[0].strip()
    if wind_direction:
      wind_direction_deg=float(wind_direction)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  barometric_pressure_hPa=None
  try:
    barometric_pressure_hPa_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[11]/td[2]')
    barometric_pressure=barometric_pressure_ele[0].text
    barometric_pressure=barometric_pressure.split('hPa')[0].strip()
    if barometric_pressure:
      barometric_pressure_hPa=float(barometric_pressure)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting barometric_pressure_hPa: "{e}"!')

  rain_today_mm=None
  try:
    rain_today_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[12]/td[3]')
    rain_today=rain_today_ele[0].text
    rain_today=rain_today.split(';')[0]
    rain_today=rain_today[5:]
    rain_today=rain_today[:-3].strip()
    if rain_today:
      rain_today_mm=float(rain_today_mm)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  rain_rate_mmph=None
  try:
    rain_rate_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[12]/td[2]')
    rain_rate=rain_rate_ele[0].text
    rain_rate=rain_rate.split('mm/h')[0].strip()
    if rain_rate:
      rain_rate_mmph=float(rain_rate)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_rate_mmph: "{e}"!')

  temperature_cels=None
  try:
    temperature_ele=tree.xpath('/html/body/div/table[2]/tbody/tr[7]/td[2]')
    temperature=temperature_ele[0].text
    temperature=temperature.split('°')[0].strip()
    if temperature:
      temperature_cels=float(temperature)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  rel_humidity=None
  try:
    humidity_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[9]/td[2]')
    humidity=humidity_ele[0].text
    humidity=humidity[:len(humidity)-len(" %")].strip()
    if humidity:
      rel_humidity=float(humidity)/100

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  heat_index_cels=None
  try:
    heat_index_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[8]/td[2]')
    heat_index=heat_index_ele[0].text
    heat_index=heat_index.split('°')[0]
    if heat_index:
      heat_index_cels=float(heat_index_cels)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting heat_index_cels: "{e}"!')

  dew_point_cels=None
  try:
    dew_point_ele = tree.xpath('/html/body/div/table[2]/tbody/tr[10]/td[2]')
    dew_point=dew_point_ele[0].text
    dew_point=dew_point.split('°')[0]
    if dew_point:
      dew_point_cels=float(dew_point)

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
