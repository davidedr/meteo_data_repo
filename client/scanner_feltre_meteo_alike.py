from datetime import datetime
import logging

import utility

#
# Scanner for MeteoVenezia weather stations alike stations
#
def scan_feltre_meteo_alike(last_seen_timestamp, server, save=True, log=True):

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
    timestamp_list=tree.xpath('/html/body/div/div/div[14]/div/div[1]/p[2]/text()[1]')
    timestamp_string=timestamp_list[0].split("Pagina aggiornata il : ")[1]
    timestamp_obj=datetime.strptime(timestamp_string, "%d/%m/%Y %H:%M:%S")

    timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
    if timestamp_string==last_seen_timestamp:
      # Weather station is not updating data
      logging.info(f'{utility.get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, last_seen_timestamp: {last_seen_timestamp}, skip saving!')
      # TODO Raise an alert
      return last_seen_timestamp

    timestamp_string_date=timestamp_obj.strftime("%d/%m/%Y")
    timestamp_string_time=timestamp_obj.strftime("%H:%M:%S")

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting timestamp: "{e}"!')

  wind_speed_knots=None
  try:
    wind_speed_kmh_elem = tree.xpath('/html/body/div/div/div[14]/div/div[1]/table/tr[15]/td[2]')
    wind_speed_kmh=wind_speed_kmh_elem[0].text.strip().split(" ")[0].strip().replace(",", ".").strip()
    if wind_speed_kmh:
      wind_speed_knots=float(wind_speed_kmh)/1.852

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_speed_knots: "{e}"!')

  wind_direction_deg=None
  try:
    wind_direction_ele = tree.xpath('/html/body/div/div/div[14]/div/div[1]/table/tr[16]/td[4]')
    wind_direction=wind_direction_ele[0].text.strip()[:-1]
    if wind_direction:
      wind_direction_deg=float(wind_direction)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_direction_deg: "{e}"!')

  barometric_pressure_hPa=None
  try:
    barometric_pressure_ele = tree.xpath('/html/body/div/div/div[14]/div/div[1]/table/tr[20]/td[2]')
    barometric_pressure=barometric_pressure_ele[0].text.strip().split(" ")[0].replace(",", ".")
    if barometric_pressure:
      barometric_pressure_hPa=float(barometric_pressure)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting barometric_pressure_hPa: "{e}"!')

  rain_today_mm=None
  try:
    rain_today_ele = tree.xpath('/html/body/div/div/div[14]/div/div[1]/table/tr[10]/td[4]')
    rain_today=rain_today_ele[0].text.strip().split(" ")[0].replace(",", ".")
    if rain_today:
      rain_today_mm=float(rain_today)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_today_mm: "{e}"!')

  rain_rate_mmph=None
  try:
    rain_rate_ele = tree.xpath('/html/body/div/div/div[14]/div/div[1]/table/tr[10]/td[2]')
    rain_rate=rain_rate_ele[0].text.strip().split(" ")[0].replace(",", ".")
    if rain_rate:
      rain_rate_mmph=float(rain_rate)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rain_rate_mmph: "{e}"!')

  temperature_cels=None
  try:
    temperature_ele=tree.xpath('/html/body/div/div/div[14]/div/div[1]/table/tr[2]/td[2]')
    temperature=temperature_ele[0].text.strip().split(" ")[0].replace(",", ".")
    if temperature:
      temperature_cels=float(temperature)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting temperature_cels: "{e}"!')

  rel_humidity=None
  try:
    humidity_ele = tree.xpath('/html/body/div/div/div[14]/div/div[1]/table/tr[4]/td[4]')
    humidity=humidity_ele[0].text.strip().split("%")[0].strip()
    if humidity:
      rel_humidity=float(humidity)/100

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting rel_humidity: "{e}"!')

  uv_index=None
  try:
    uv_index_ele=tree.xpath('/html/body/div/div/div[14]/div/div[1]/table/tr[6]/td[4]')
    uv_index_string=uv_index_ele[0].text
    if uv_index_string:
      uv_index=float(uv_index_string)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting uv_index_cels: "{e}"!')

  wind_gust_knots=None
  try:
    wind_gust_kmh_elem = tree.xpath('/html/body/div/div/div[14]/div/div[1]/table/tr[16]/td[2]')
    wind_gust_kmh=wind_gust_kmh_elem[0].text.strip().split(" ")[0].strip().replace(",", ".")
    if wind_gust_kmh:
      wind_gust_knots=float(wind_gust_kmh)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_gust_knots: "{e}"!')

  wind_chill_cels=None
  try:
    wind_chill_ele = tree.xpath('/html/body/div/div/div[14]/div/div[1]/table/tr[5]/td[2]')
    wind_chill=wind_chill_ele[0].text.strip().split(" ")[0].replace(",", ".")
    if wind_chill:
      wind_chill_cels=float(wind_chill)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting wind_chill_cels: "{e}"!')

  solar_irradiance_wpsm=None
  try:
    solar_irradiance_ele=tree.xpath('/html/body/div/div/div[14]/div/div[1]/table/tr[6]/td[2]/text()')
    solar_irradiance=solar_irradiance_ele[0].strip().split(" ")[0].strip()
    if solar_irradiance:
      solar_irradiance_wpsm=float(solar_irradiance)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting solar_irradiance_wpsm: "{e}"!')

  rain_this_month_mm=None
  try:
    rain_this_month_ele = tree.xpath('/html/body/div/div/div[14]/div/div[1]/table/tr[11]/td[4]')
    rain_this_month=rain_this_month_ele[0].text.strip().split(" ")[0].replace(",", ".")
    if rain_this_month:
      rain_this_month_mm=float(rain_this_month)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting heat_index_cels: "{e}"!')

  rain_this_year_mm=None
  try:
    rain_this_year_ele = tree.xpath('/html/body/div/div/div[14]/div/div[1]/table/tr[12]/td[4]')
    rain_this_year=rain_this_year_ele[0].text.strip().split(" ")[0].replace(",", ".")
    if rain_this_year:
      rain_this_year_mm=float(rain_this_year)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting heat_index_cels: "{e}"!')

  evapotranspiration_today_mm=None
  try:
    evapotranspiration_today_ele = tree.xpath('/html/body/div/div/div[14]/div/div[1]/table/tr[5]/td[4]')
    evapotranspiration_today=evapotranspiration_today_ele[0].text.strip().split(" ")[0].strip().replace(",", ".")
    if evapotranspiration_today:
      evapotranspiration_today_mm=float(evapotranspiration_today)

  except Exception as e:
    logging.exception(f'{utility.get_identification_string(location_id, server_name)}, exception getting dew_point_cels: "{e}"!')

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
  meteo_data_dict["wind_gust_knots"]=wind_gust_knots
  meteo_data_dict["wind_chill_cels"]=wind_chill_cels
  meteo_data_dict["solar_irradiance_wpsm"]=solar_irradiance_wpsm
  meteo_data_dict["rain_this_month_mm"]=rain_this_month_mm
  meteo_data_dict["rain_this_year_mm"]=rain_this_year_mm
  meteo_data_dict["evapotranspiration_today_mm"]=evapotranspiration_today_mm


  if log:
    utility.log_sample(location_id, server_name, meteo_data_dict)

  if not(timestamp_string and (wind_speed_knots or wind_direction_deg or barometric_pressure_hPa or rain_today_mm or rain_rate_mmph or temperature_cels or rel_humidity or wind_gust_knots)):
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, Not enough scraped data. Skip saving data...')
    logging.info(f'{utility.get_identification_string(location_id, server_name)}, timestamp_string: {timestamp_string}, wind_speed_knots: {wind_speed_knots}, wind_direction_deg: {wind_direction_deg}, barometric_pressure_hPa: {barometric_pressure_hPa}, rain_today_mm: {rain_today_mm}, rain_rate_mmph: {rain_rate_mmph}, temperature_cels: {temperature_cels}, rel_humidity: {rel_humidity}, wind_gust_knots: {wind_gust_knots}')
    return last_seen_timestamp

  utility.save_v6(location_id, server_name, meteo_data_dict)
  return timestamp_string

if __name__=="__main__":
  utility.test_starter(19) # Location id