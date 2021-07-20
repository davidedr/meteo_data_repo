from datetime import datetime
import logging

import utility

#
# Scanner for MeteoVenezia weather stations alike stations
#
def scan_osservatorio_metereologico_monte_avena_alike(last_seen_timestamp, server, save=True, log=True):

  location_id=server["location_id"]
  server_name=server["name"]
  weather_station_url=server["url"]

  if isinstance(weather_station_url, dict):
    weather_station_url=weather_station_url.get("1")

  tree, _ =utility.get_tree(weather_station_url, location_id, server_name)
  if tree is None:
    return last_seen_timestamp

  timestamp_string=None
  timestamp_string_date=None
  timestamp_string_time=None
  try:
    timestamp_list=tree.xpath('/html/body/div/div/table/tr/td/p/b/font/span')
    timestamp_datetime_string=timestamp_list[0].text.strip().split(" ")
    
    timestamp_date_string=timestamp_datetime_string[0].strip()
    timestamp_time_string=timestamp_datetime_string[2].strip()

    timestamp_datetime_string=timestamp_date_string+" "+timestamp_time_string
    timestamp_date_obj=datetime.strptime(timestamp_datetime_string, "%d/%m/%Y %H:%M")
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

  temperature_cels=None
  try:
    temperature_ele=tree.xpath('//*[@id="ajaxtemp"]/font')
    temperature=temperature_ele[0].text.strip().split("°")[0].strip()
    if temperature:
      temperature_cels=float(temperature)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  dew_point_cels=None
  try:
    dew_point_ele=tree.xpath('//*[@id="ajaxdew0"]')
    dew_point=dew_point_ele[0].text.strip().split("°")[0].strip()
    if dew_point:
      dew_point_cels=float(dew_point)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting dew_point_cels: "{e}"!')

  perceived_temperature_cels=None
  try:
    perceived_temperature_ele=tree.xpath('//*[@id="ajaxapparenttemp"]')
    perceived_temperature=perceived_temperature_ele[0].text.strip().split("°")[0].replace(",", ".")
    if perceived_temperature:
      perceived_temperature_cels=float(perceived_temperature)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_chill_cels: "{e}"!')

  wet_bulb_temperature_cels=None
  try:
    wet_bulb_temperature=tree.xpath('//*[@id="ajaxwetbulb"]')[0].text.split("°")[0].strip()
    if wet_bulb_temperature:
      wet_bulb_temperature_cels=float(wet_bulb_temperature)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wet_bulb_temperature_cels: "{e}"!')

  rain_rate_mmh=None
  try:
    rain_rate_ele=tree.xpath('//*[@id="ajaxrainratehr0"]')
    rain_rate=rain_rate_ele[0].text.strip()
    if rain_rate:
      rain_rate_mmh=float(rain_rate)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_rate_mmh: "{e}"!')

  rel_humidity=None
  try:
    humidity_ele=tree.xpath('//*[@id="ajaxhumidity"]/font')
    humidity=humidity_ele[0].text.strip().split("%")[0].strip()
    if humidity:
      rel_humidity=float(humidity)/100

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  wind_speed_knots=None
  try:
    wind_speed_kmh_elem=tree.xpath('//*[@id="ajaxwind0"]')
    wind_speed_kmh=wind_speed_kmh_elem[0].text.strip().split(" ")[0].strip()
    if wind_speed_kmh and wind_speed_kmh!="N.D.":
      wind_speed_knots=float(wind_speed_kmh)/1.852

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

  wind_direction_deg=None
  try:
    wind_direction_ele=tree.xpath('//*[@id="ajaxwinddir"]')
    wind_direction=wind_direction_ele[0].text.strip()
    wind_direction_deg=utility.convert_wind_direction_to_deg(wind_direction)
    if wind_direction_deg is None:
      logging.info(f'{utility.get_identification_string(location_id, server_name)}, Unknown wind_direction: "{wind_direction}"!')

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  wind_temperature_cels=None
  try:
    wind_temperature=tree.xpath('//*[@id="ajaxapparenttemp"]')[0].text.split("°")[0].strip()
    if wind_temperature:
      wind_temperature_cels=float(wind_temperature)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wet_bulb_temperature_cels: "{e}"!')

  barometric_pressure_ssl_hPa=None
  try:
    barometric_pressure_ssl_ele=tree.xpath('//*[@id="ajaxbaro"]')
    barometric_pressure_ssl=barometric_pressure_ssl_ele[0].text.strip().split(" ")[0].strip()
    if barometric_pressure_ssl:
      barometric_pressure_ssl_hPa=float(barometric_pressure_ssl)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting barometric_pressure_ssl_hPa: "{e}"!')

  rain_today_mm=None
  try:
    rain_today_ele=tree.xpath('//*[@id="ajaxrain0"]')
    rain_today=rain_today_ele[0].text.strip()
    if rain_today:
      rain_today_mm=float(rain_today)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  #
  #
  weather_station_url=server["url"]
  if isinstance(weather_station_url, dict):
    weather_station_url=weather_station_url.get("2")
  else:
    weather_station_url=None

  if weather_station_url is not None:
    tree, _ = utility.get_tree(weather_station_url, location_id, server_name)
    if tree is not None:

      average_wind_speed_knots=None
      try:
        average_wind_speed_ele=tree.xpath("/html/body/div/table/tr[1]/td[2]/table/tr[1]/td[3]")
        average_wind_speed=average_wind_speed_ele[0].text.split(" ")[0].strip()
        if average_wind_speed:
          average_wind_speed_knots=float(average_wind_speed)/1.852

      except Exception as e:
        logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting average_wind_speed_knots: "{e}"!')

  meteo_data_dict={}
  meteo_data_dict["timestamp_string"]=timestamp_string
  meteo_data_dict["timestamp_string_date"]=timestamp_string_date
  meteo_data_dict["timestamp_string_time"]=timestamp_string_time
  meteo_data_dict["temperature_cels"]=temperature_cels
  meteo_data_dict["dew_point_cels"]=dew_point_cels
  meteo_data_dict["perceived_temperature_cels"]=perceived_temperature_cels
  meteo_data_dict["wet_bulb_temperature_cels"]=wet_bulb_temperature_cels
  meteo_data_dict["rain_rate_mmh"]=rain_rate_mmh
  meteo_data_dict["rel_humidity"]=rel_humidity
  meteo_data_dict["wind_speed_knots"]=wind_speed_knots
  meteo_data_dict["wind_direction_deg"]=wind_direction_deg
  meteo_data_dict["wind_temperature_cels"]=wind_temperature_cels
  meteo_data_dict["barometric_pressure_ssl_hPa"]=barometric_pressure_ssl_hPa
  meteo_data_dict["rain_today_mm"]=rain_today_mm
  meteo_data_dict["average_wind_speed_knots"]=average_wind_speed_knots
  
  if log:
    utility.log_sample(location_id, server_name, meteo_data_dict)

  if not utility.check_minimum_data(location_id, server_name, meteo_data_dict):
    return last_seen_timestamp

  utility.save(location_id, server_name, meteo_data_dict)
  return timestamp_string

if __name__=="__main__":
  utility.test_starter(22) # Location id
