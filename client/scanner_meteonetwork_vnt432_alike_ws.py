from datetime import datetime
import logging

import utility

#
#
#
def scan_meteonetwork_vnt432_alike(last_seen_timestamp, server, save=True, log=True):

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
    timestamp_list=tree.xpath('/html/body/div[3]/div[1]/div/h3[1]')
    timestamp_ele=timestamp_list[0].text

    if timestamp_ele.find("Dati in diretta (aggiornati alle ")>=0:
      time_string=timestamp_ele.split('Dati in diretta (aggiornati alle ')[1].strip().split(" ")
      time_string[2]=time_string[2].strip().split(")")[0]
    elif timestamp_ele.find("Ultimo dato disponibile delle ")>=0:
      time_string=timestamp_ele.split('Ultimo dato disponibile delle ')[1].strip().split(" ")
    else:
      logging.info(f'{utility.get_identification_string(location_id, server_name)}, unable to parse timestamp_ele: {timestamp_ele}!')
      # TODO Raise an alert
      return last_seen_timestamp

    date_string=time_string[2].strip()
    time_string=time_string[0].strip()

    datetime_string=date_string+" "+time_string
    timestamp_obj=datetime.strptime(datetime_string, "%d/%m/%Y %H:%M")
    timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
    timestamp_string_date=timestamp_obj.strftime("%d/%m/%Y")
    timestamp_string_time=timestamp_obj.strftime("%H:%M:%S")

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting timestamp: "{e}"!')

  if timestamp_string==last_seen_timestamp:
    # Weather station is not updating data
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, last_seen_timestamp: {last_seen_timestamp}, skip saving!')
    # TODO Raise an alert
    return last_seen_timestamp

  temperature_cels=None
  try:
    not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[4]/table/tbody/tr[1]/td[2]/span')
    if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
      temperature_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[4]/table/tbody/tr[1]/td[2]/span/text()')
      temperature=temperature_ele[0].strip().split("°")[0].strip().replace(" ","")
      if temperature:
        temperature_cels=float(temperature)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  rel_humidity=None
  try:
    not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[4]/table/tbody/tr[2]/td[2]/span')
    if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
      rel_humidity_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[4]/table/tbody/tr[2]/td[2]/span/text()')
      rel_humidity=rel_humidity_ele[0].strip().split("%")[0].strip()
      rel_humidity=float(rel_humidity)/100

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  barometric_pressure_ssl_hPa=None
  try:
    not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[4]/table/tbody/tr[3]/td[2]/span')
    if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
      barometric_pressure_ssl_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[4]/table/tbody/tr[3]/td[2]/span/text()')
      barometric_pressure_ssl=barometric_pressure_ssl_ele[0].strip().split(" ")[0].strip()
      if barometric_pressure_ssl:
        barometric_pressure_ssl_hPa=float(barometric_pressure_ssl)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting barometric_pressure_ssl_hPa: "{e}"!')

  wind_speed_knots=None
  try:
    not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[4]/table/tbody/tr[4]/td[2]/span[1]')
    if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
      wind_speed_kmh_elem=tree.xpath('/html/body/div[3]/div[1]/div/div[4]/table/tbody/tr[4]/td[2]/span[1]/text()')
      wind_speed_kmh=wind_speed_kmh_elem[0].strip().split(" ")[0].strip()
      if wind_speed_kmh:
        wind_speed_knots=float(wind_speed_kmh)/1.852

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

  wind_gust_knots=None
  try:
    not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[4]/table/tbody/tr[4]/td[2]/span[2]')
    if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
      wind_gust_kmh_elem=tree.xpath('/html/body/div[3]/div[1]/div/div[4]/table/tbody/tr[4]/td[2]/span[2]')
      wind_gust_kmh=wind_gust_kmh_elem[0].text.strip().split("Raffica")[1].strip().split("km/h")[0].strip()
      if wind_gust_kmh:
        wind_gust_knots=float(wind_gust_kmh)/1.852

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_gust_knots: "{e}"!')

  wind_direction_deg=None
  try:
    wind_direction_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[4]/table/tbody/tr[4]/td[3]/strong')
    wind_direction=wind_direction_ele[0].text.strip()
    wind_direction_deg=utility.convert_wind_direction_to_deg(wind_direction)
    if wind_direction_deg is None:
      logging.info(f'{utility.get_identification_string(location_id, server_name)}, Unknown wind_direction: "{wind_direction}"!')

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  rain_today_mm=None
  try:
    not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[4]/table/tbody/tr[5]/td[2]/span')
    if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
      rain_today_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[4]/table/tbody/tr[5]/td[2]/span/text()')
      rain_today=str(rain_today_ele[0]).strip().split(" ")[0].strip()
      if rain_today:
        rain_today_mm=float(rain_today)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  dew_point_cels=None
  try:
    dew_point_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[4]/table/tbody/tr[6]/td[2]/text()')
    dew_point=dew_point_ele[0].strip().split("°")[0].strip().replace(" ","")
    if dew_point:
      dew_point_cels=float(dew_point)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting dew_point_cels: "{e}"!')

  heat_index_cels=None
  try:
    # Heat index is computed
    heat_index_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[4]/table/tbody/tr[7]/td[2]/text()')
    heat_index=heat_index_ele[0].split("°")[0].strip()
    if heat_index:
      heat_index_cels=float(heat_index)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting heat_index: "{e}"!')

  solar_irradiance_wpsm=None # Watts per square meter
  try:
    not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[4]/table/tbody/tr[8]/td[2]/span')
    if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
      solar_irradiance_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[4]/table/tbody/tr[8]/td[2]/span/text()')
      solar_irradiance=solar_irradiance_ele[0].strip().split(" ")[0].strip()
      if solar_irradiance:
        solar_irradiance_wpsm=float(solar_irradiance)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting solar_irradiance_wpsm: "{e}"!')

  meteo_data_dict={}
  meteo_data_dict["timestamp_string"]=timestamp_string
  meteo_data_dict["timestamp_string_date"]=timestamp_string_date
  meteo_data_dict["timestamp_string_time"]=timestamp_string_time
  meteo_data_dict["temperature_cels"]=temperature_cels
  meteo_data_dict["rel_humidity"]=rel_humidity
  meteo_data_dict["barometric_pressure_ssl_hPa"]=barometric_pressure_ssl_hPa
  meteo_data_dict["wind_speed_knots"]=wind_speed_knots
  meteo_data_dict["wind_gust_knots"]=wind_gust_knots
  meteo_data_dict["wind_direction_deg"]=wind_direction_deg
  meteo_data_dict["rain_today_mm"]=rain_today_mm
  meteo_data_dict["dew_point_cels"]=dew_point_cels
  meteo_data_dict["heat_index_cels"]=heat_index_cels
  meteo_data_dict["solar_irradiance_wpsm"]=solar_irradiance_wpsm

  if log:
    utility.log_sample(location_id, server_name, meteo_data_dict)

  if not utility.check_minimum_data(location_id, server_name, meteo_data_dict):
    return last_seen_timestamp
    
  utility.save(location_id, server_name, meteo_data_dict)
  return timestamp_string

if __name__=="__main__":
  utility.test_starter(17) # Location id
