from datetime import datetime
import logging
import utility

from utility import log_xpath_elem, convert_wind_direction_to_deg, get_identification_string, get_tree, save_v6

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