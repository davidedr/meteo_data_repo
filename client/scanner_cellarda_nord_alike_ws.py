from datetime import datetime
import logging

import utility

#
#
#
def scan_cellarda_nord_ws_alike(last_seen_timestamp, server, save=True, log=True):

  location_id=server["location_id"]
  server_name=server["name"]
  weather_station_url=server["url"]

  tree, page_text = utility.get_tree(weather_station_url, location_id, server_name)
  if tree is None:
    return last_seen_timestamp

  timestamp_string=None
  timestamp_string_date=None
  timestamp_string_time=None
  month_converter={ "Gennaio": "01", "Febbraio": "02", "Marzo": "03", "Aprile": "04", "Maggio": "05", "Giugno": "06", \
     "Luglio": "07", "Agosto": "08", "Settembre": "09", "Ottobre": "10", "Novembre": "11", "Dicembre": "12"}
  try: 
    timestamp_string = tree.xpath("//font[contains(text(),'ULTIMO RILEVAMENTO')]")[0].text.split(" ")
    timestamp_hour=timestamp_string[4]
    timestamp_day=timestamp_string[7]
    timestamp_month=timestamp_string[8]
    timestamp_year=timestamp_string[9]

    timestamp_string=f'{timestamp_day}.{month_converter.get(timestamp_month)}.{timestamp_year} {timestamp_hour}'
    timestamp_obj=datetime.strptime(timestamp_string, "%d.%m.%Y %H:%M")

    timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
    if last_seen_timestamp and last_seen_timestamp==timestamp_string:
      return last_seen_timestamp

    timestamp_string_date=timestamp_obj.strftime("%d/%m/%Y")
    timestamp_string_time=timestamp_obj.strftime("%H:%M:%S")

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting timestamp: "{e}"!')

  if timestamp_string==last_seen_timestamp:
    # Weather station is not updating data
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, last_seen_timestamp: {last_seen_timestamp}, skip saving!')
    # TODO Raise an alert
    return last_seen_timestamp

  barometric_pressure_hPa=None
  try:
    barometric_pressure_hPa_ele = tree.xpath("//font[contains(text(),'hPa')]")
    barometric_pressure_hPa=barometric_pressure_hPa_ele[0].text
    barometric_pressure_hPa=barometric_pressure_hPa.split('hPa')[0].strip()

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting barometric_pressure_hPa: "{e}"!')

  rain_today_mm=None
  try:
    rain_today_mm=tree.xpath("//font")[43].text.split(" ")[0].strip()
    rain_today_mm=float(rain_today_mm)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  rain_rate_mmph=None
  try:
    rain_rate_mmph=tree.xpath("//tr/td")[21].text.split(" ")[0]
    rain_rate_mmph=float(rain_rate_mmph)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_rate_mmph: "{e}"!')

  rain_this_month_mm=None
  try:
    rain_this_month_mm=tree.xpath("//tr/td")[25].text.split(" ")[0]
    rain_this_month_mm=float(rain_this_month_mm)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_this_month_mm: "{e}"!')

  rain_this_year_mm=None
  try:
    rain_this_year_mm=tree.xpath("//tr/td")[27].text.split(" ")[0]
    rain_this_year_mm=float(rain_this_year_mm)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_this_year_mm: "{e}"!')

  rel_humidity=None
  try:
    humidity=tree.xpath("//tr/td")[37].text.split("%")[0].strip()
    rel_humidity=float(humidity)/100

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  temperature_cels=None
  try:
    temperature_cels_ele=tree.xpath('//b')
    temperature_cels=temperature_cels_ele[5].text.split("°")[0]
    temperature_cels=float(temperature_cels)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  heat_index_cels=None
  try:
    # Extreme problems, extreme solutions
    heat_index_cels=page_text.split("temperatura apparente")[1].split("&")[0].strip()

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting heat_index_cels: "{e}"!')

  dew_point_cels=None
  try:
    dew_point_cels=tree.xpath("//font")[56].text.split("°")[0]
    dew_point_cels=float(dew_point_cels)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting dew_point_cels: "{e}"!')

  wind_speed_knots=None
  try:
    wind_speed_kmh=tree.xpath("//tr/td")[9].text.split(" ")[0].strip()
    wind_speed_knots=float(wind_speed_kmh)/1.852

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

  wind_gust_knots=None
  try:
    wind_gust_kmh=page_text.split('Massima forza </font><FONT SIZE=+0> (ultima ora)</td><td><font color="#009900">')[1].split(" ")[0]
    if wind_gust_kmh:
      wind_gust_knots=float(wind_gust_kmh)/1.852

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_gust_knots: "{e}"!')

  wind_direction_deg=None
  try:  
    wind_direction=tree.xpath("//tr/td")[11].text.split(" ")[0].strip()
    wind_direction_deg=utility.convert_wind_direction_to_deg(wind_direction)
    if not wind_direction_deg:
      logging.info(f'{utility.get_identification_string(location_id, server_name)}, Unknown wind_direction: "{wind_direction}"!')

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  meteo_data_dict={}
  meteo_data_dict["timestamp_string"]=timestamp_string
  meteo_data_dict["timestamp_string_date"]=timestamp_string_date
  meteo_data_dict["timestamp_string_time"]=timestamp_string_time
  meteo_data_dict["barometric_pressure_hPa"]=barometric_pressure_hPa
  meteo_data_dict["rain_today_mm"]=rain_today_mm
  meteo_data_dict["rain_rate_mmph"]=rain_rate_mmph
  meteo_data_dict["rain_this_month_mm"]=rain_this_month_mm
  meteo_data_dict["rain_this_year_mm"]=rain_this_year_mm
  meteo_data_dict["rel_humidity"]=rel_humidity
  meteo_data_dict["temperature_cels"]=temperature_cels
  meteo_data_dict["heat_index_cels"]=heat_index_cels
  meteo_data_dict["dew_point_cels"]=dew_point_cels
  meteo_data_dict["wind_speed_knots"]=wind_speed_knots
  meteo_data_dict["wind_gust_knots"]=wind_gust_knots
  meteo_data_dict["wind_direction_deg"]=wind_direction_deg

  if log:
    utility.log_sample(location_id, server_name, meteo_data_dict)

  if not(timestamp_string and (barometric_pressure_hPa or rain_today_mm or rain_rate_mmph or rain_this_month_mm or rain_this_year_mm or rel_humidity or temperature_cels or heat_index_cels or dew_point_cels or wind_speed_knots or wind_gust_knots or wind_direction_deg)):
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, Not enough scraped data. Skip saving data...')
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, barometric_pressure_hPa: {barometric_pressure_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmph: {rain_rate_mmph }, rain_this_month_mm: {rain_this_month_mm}, rain_this_year_mm: {rain_this_year_mm},  rel_humidity: {rel_humidity}, temperature_cels: {temperature_cels}, heat_index_cels: {heat_index_cels}, dew_point_cels: {dew_point_cels}, wind_speed_knots: {wind_speed_knots}, wind_gust_knots: {wind_gust_knots}, wind_direction_deg: {wind_direction_deg}')
    return last_seen_timestamp

  utility.save_v6(location_id, server_name, meteo_data_dict)
  return timestamp_string