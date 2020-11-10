from datetime import datetime
import logging
import utility

from utility import log_xpath_elem, convert_wind_direction_to_deg, get_identification_string, get_tree, save_v6

#
#
#
def scan_cellarda_ws_alike(last_seen_timestamp, server, save=True, log=True):

  location_id=server["location_id"]
  server_name=server["name"]
  weather_station_url=server["url"]
  if isinstance(weather_station_url, dict):
    weather_station_url=weather_station_url.get("1")

  tree, page_text = get_tree(weather_station_url, location_id)
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
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting timestamp: "{e}"!')

  if timestamp_string==last_seen_timestamp:
    # Weather station is not updating data
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, last_seen_timestamp: {last_seen_timestamp}, skip saving!')
    # TODO Raise an alert
    return last_seen_timestamp

  barometric_pressure_hPa=None
  try:
    barometric_pressure_ele = tree.xpath("//font[contains(text(),'hPa')]")
    barometric_pressure=barometric_pressure_ele[0].text
    barometric_pressure=barometric_pressure.split('hPa')[0].strip()
    if barometric_pressure:
      barometric_pressure_hPa=float(barometric_pressure_hPa)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting barometric_pressure_hPa: "{e}"!')

  rain_today_mm=None
  try:
    rain_today=tree.xpath("//font")[43].text.split(" ")[0].strip()
    if rain_today:
      rain_today_mm=float(rain_today)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  rain_rate_mmph=None
  try:
    rain_rate=tree.xpath("//tr/td")[21].text.split(" ")[0]
    if rain_rate:
      rain_rate_mmph=float(rain_rate)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_rate_mmph: "{e}"!')

  rain_this_month_mm=None
  try:
    rain_this_month=tree.xpath("//tr/td")[25].text.split(" ")[0]
    if rain_this_month_mm:
      rain_this_month_mm=float(rain_this_month)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_this_month: "{e}"!')

  rain_this_year_mm=None
  try:
    rain_this_year=tree.xpath("//tr/td")[27].text.split(" ")[0]
    if rain_this_year:
      rain_this_year_mm=float(rain_this_year)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rain_this_year: "{e}"!')

  rel_humidity=None
  try:
    humidity=tree.xpath("//tr/td")[37].text.split("%")[0].strip()
    if humidity:
      rel_humidity=float(humidity)/100

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  temperature_cels=None
  try:
    temperature_ele=tree.xpath('//b')
    temperature=temperature_ele[4].text.split("°")[0]
    if temperature:
      temperature_cels=float(temperature)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  heat_index_cels=None
  try:
    # Extreme problems, extreme solutions
    heat_index_ele=page_text.split("temperatura apparente")[1].split("&")[0].strip()
    if heat_index_ele:
      heat_index_cels=float(heat_index_ele)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting heat_index_cels: "{e}"!')

  dew_point_cels=None
  try:
    dew_point_ele=tree.xpath("//font")[56].text.split("°")[0]
    if dew_point_ele:
      dew_point_cels=float(dew_point_ele)

  except Exception as e:
    logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting dew_point_cels: "{e}"!')

  #
  # From another site
  #
  wind_speed_knots=wind_gust_knots=wind_direction_deg=None
  weather_station_url=server["url"]
  if isinstance(weather_station_url, dict):
    weather_station_url=weather_station_url.get("2")
  else:
    weather_station_url=None
  if weather_station_url is not None:
    tree, _ = get_tree(weather_station_url, location_id)
    if tree is not None:

      wind_speed_knots=None
      try:
        not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[4]/td[2]/span[1]')
        if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
          wind_speed_kmh_elem=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[4]/td[2]/span[1]')
          wind_speed_kmh=wind_speed_kmh_elem[0].text.strip().split(" ")[0].strip()
          if wind_speed_kmh:
            wind_speed_knots=float(wind_speed_kmh)/1.852

      except Exception as e:
        logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

      wind_gust_knots=None
      try:
        not_valid_warning_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[4]/td[2]/span[1]')
        if len(not_valid_warning_ele)==0 or (not_valid_warning_ele[0].attrib.get("class") != 'notvalid cluetips'):
          wind_gust_kmh_elem=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[4]/td[2]/span[2]')
          wind_gust_kmh=wind_gust_kmh_elem[0].text.strip().split(" ")[1].strip()
          if wind_gust_kmh:
            wind_gust_knots=float(wind_gust_kmh)/1.852

      except Exception as e:
        logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_gust_knots: "{e}"!')

      wind_direction_deg=None
      try:  
        wind_direction_ele=tree.xpath('/html/body/div[3]/div[1]/div/div[5]/table/tbody/tr[4]/td[3]/strong')
        wind_direction=wind_direction_ele[0].text.strip()
        wind_direction_deg=convert_wind_direction_to_deg(wind_direction)
        if not wind_direction_deg:
          logging.info(f'{get_identification_string(location_id, server_name)}, Unknown wind_direction: "{wind_direction}"!')

      except Exception as e:
        logging.exception(f'{get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  if not(timestamp_string and (barometric_pressure_hPa or rain_today_mm or rain_rate_mmph or rain_this_month or rain_this_year_mm or rel_humidity or temperature_cels or heat_index_cels or dew_point_cels or wind_speed_knots or wind_gust_knots or wind_direction_deg)):
    logging.info(f'{get_identification_string(location_id, server_name)}, Not enough scraped data. Skip saving data...')
    logging.info(f'{get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, barometric_pressure_hPa: {barometric_pressure_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmph: {rain_rate_mmph }, rain_this_month_mm: {rain_this_month_mm}, rain_this_year: {rain_this_year},  rel_humidity: {rel_humidity}, temperature_cels: {temperature_cels}, heat_index_cels: {heat_index_cels}, dew_point_cels: {dew_point_cels}, wind_speed_knots: {wind_speed_knots}, wind_gust_knots: {wind_gust_knots}, wind_direction_deg: {wind_direction_deg}')
    return last_seen_timestamp

  meteo_data_dict={}
  meteo_data_dict["timestamp_string"]=timestamp_string
  meteo_data_dict["timestamp_string_date"]=timestamp_string_date
  meteo_data_dict["timestamp_string_time"]=timestamp_string_time
  meteo_data_dict["barometric_pressure_hPa"]=barometric_pressure_hPa
  meteo_data_dict["rain_today_mm"]=rain_today_mm
  meteo_data_dict["rain_rate_mmph"]=rain_rate_mmph
  meteo_data_dict["rain_this_month_mm"]=rain_this_month
  meteo_data_dict["rain_this_year_mm"]=rain_this_year_mm
  meteo_data_dict["rel_humidity"]=rel_humidity
  meteo_data_dict["temperature_cels"]=temperature_cels
  meteo_data_dict["heat_index_cels"]=heat_index_cels
  meteo_data_dict["dew_point_cels"]=dew_point_cels
  meteo_data_dict["wind_speed_knots"]=wind_speed_knots
  meteo_data_dict["wind_gust_knots"]=wind_gust_knots
  meteo_data_dict["wind_direction_deg"]=wind_direction_deg

  save_v6(location_id, server_name, meteo_data_dict)
  return timestamp_string
