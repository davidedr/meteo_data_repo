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

  barometric_pressure_ssl_hPa=None
  try:
    barometric_pressure_ssl_ele = tree.xpath("//font[contains(text(),'hPa')]")
    barometric_pressure_ssl=barometric_pressure_ssl_ele[0].text.split('hPa')[0].strip()
    if barometric_pressure_ssl:
      barometric_pressure_ssl_hPa=float(barometric_pressure_ssl)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting barometric_pressure_ssl_hPa: "{e}"!')

  rain_today_mm=None
  try:
    rain_today=tree.xpath("//font")[43].text.split(" ")[0].strip()
    rain_today_mm=float(rain_today)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  rain_rate_mmh=None
  try:
    rain_rate=tree.xpath("//tr/td")[21].text.split(" ")[0]
    if rain_rate:
      rain_rate_mmh=float(rain_rate)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_rate_mmh: "{e}"!')

  rain_this_month_mm=None
  try:
    rain_this_month=tree.xpath("//tr/td")[25].text.split(" ")[0]
    if rain_this_month:
      rain_this_month_mm=float(rain_this_month)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_this_month_mm: "{e}"!')

  rain_this_year_mm=None
  try:
    rain_this_year=tree.xpath("//tr/td")[27].text.split(" ")[0]
    if rain_this_year:
      rain_this_year_mm=float(rain_this_year)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_this_year_mm: "{e}"!')

  storm_rain_mmm=None
  try:
    storm_rain=tree.xpath("//tr/td")[29].text.split(" ")[0].strip()
    if storm_rain:
      storm_rain_mmm=float(storm_rain)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting storm_rain_mm: "{e}"!')

  rel_humidity=None
  try:
    humidity=tree.xpath("//tr/td")[37].text.split("%")[0].strip()
    if humidity:
      rel_humidity=float(humidity)/100

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  humidex_cels=None
  try:
    humidex_ele=tree.xpath("//tr/td")[37].text.split("%")[1].strip().split(" ")[2].strip().split("°")[0].strip()
    if humidex_ele:
      humidex_cels=float(humidex_ele)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting humidex_cels: "{e}"!')

  current_weather=None
  try:
    current_weather=tree.xpath("//tr/td")[1].text.strip()

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting current_weather: "{e}"!')

  temperature_cels=None
  try:
    temperature_ele=tree.xpath('//b')
    temperature=temperature_ele[5].text.split("°")[0]
    if temperature:
      temperature_cels=float(temperature)

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
    dew_point=tree.xpath("//font")[56].text.split("°")[0]
    if dew_point:
      dew_point_cels=float(dew_point)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting dew_point_cels: "{e}"!')

  wind_temperature_cels=None
  try:
    wind_temperature=tree.xpath("//tr/td")[13].text.split("°")[0].strip()
    if wind_temperature:
      wind_temperature_cels=float(wind_temperature)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_temperature_cels: "{e}"!')

  average_wind_speed_knots=None
  try:
    average_wind_speed=tree.xpath("//tr/td")[9].text.strip().split(" ")[0]
    if average_wind_speed:
      average_wind_speed_knots=float(average_wind_speed)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting average_wind_speed_knots: "{e}"!')

  wet_bulb_temperature_cels=None
  try:
    wet_bulb_temperature=tree.xpath("//tr/td//font")[46].text.split(":")[1].split("°")[0].strip()
    if wet_bulb_temperature:
      wet_bulb_temperature_cels=float(wet_bulb_temperature)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wet_bulb_temperature_cels: "{e}"!')

  wind_speed_knots=None
  try:
    wind_speed_kmh=tree.xpath("//tr/td")[9].text.split(" ")[0].strip()
    if wind_speed_kmh:
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
  meteo_data_dict["barometric_pressure_ssl_hPa"]=barometric_pressure_ssl_hPa
  meteo_data_dict["rain_today_mm"]=rain_today_mm
  meteo_data_dict["rain_rate_mmh"]=rain_rate_mmh
  meteo_data_dict["rain_this_month_mm"]=rain_this_month_mm
  meteo_data_dict["rain_this_year_mm"]=rain_this_year_mm
  meteo_data_dict["rel_humidity"]=rel_humidity
  meteo_data_dict["temperature_cels"]=temperature_cels
  meteo_data_dict["heat_index_cels"]=heat_index_cels
  meteo_data_dict["dew_point_cels"]=dew_point_cels
  meteo_data_dict["wind_speed_knots"]=wind_speed_knots
  meteo_data_dict["wind_gust_knots"]=wind_gust_knots
  meteo_data_dict["wind_direction_deg"]=wind_direction_deg
  meteo_data_dict["humidex_cels"]=humidex_cels

  meteo_data_dict["current_weather"]=current_weather
  meteo_data_dict["wind_temperature_cels"]=wind_temperature_cels
  meteo_data_dict["wet_bulb_temperature_cels"]=wet_bulb_temperature_cels
  meteo_data_dict["average_wind_speed_knots"]=average_wind_speed_knots
  meteo_data_dict["storm_rain_mmm"]=storm_rain_mmm

  if log:
    utility.log_sample(location_id, server_name, meteo_data_dict)

  if not(timestamp_string and (barometric_pressure_ssl_hPa or rain_today_mm or rain_rate_mmh or rain_this_month_mm or rain_this_year_mm or rel_humidity or temperature_cels or perceived_temperature_cels or dew_point_cels or wind_speed_knots or wind_gust_knots or wind_direction_deg or humidex_cels or wind_temperature_cels or current_weather or wet_bulb_temperature_cels or average_wind_speed_knots or storm_rain_mmm)):
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, Not enough scraped data. Skip saving data...')
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, barometric_pressure_ssl_hPa: {barometric_pressure_ssl_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmh: {rain_rate_mmh }, rain_this_month_mm: {rain_this_month_mm}, rain_this_year: {rain_this_year},  rel_humidity: {rel_humidity}, temperature_cels: {temperature_cels}, perceived_temperature_cels: {perceived_temperature_cels}, dew_point_cels: {dew_point_cels}, wind_speed_knots: {wind_speed_knots}, wind_gust_knots: {wind_gust_knots}, wind_direction_deg: {wind_direction_deg}, humidex_cels: {humidex_cels}, wind_temperature_cels: {wind_temperature_cels}, current_weather: {current_weather}, wet_bulb_temperature_cels: {wet_bulb_temperature_cels}, average_wind_speed_knots: {average_wind_speed_knots}, storm_rain_mmm: {storm_rain_mmm}.')
    return last_seen_timestamp

  utility.save_v9(location_id, server_name, meteo_data_dict)
  return timestamp_string

if __name__=="__main__":
  utility.test_starter(16) # Location id
