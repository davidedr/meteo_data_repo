from lxml import html
import requests
import unicodedata

def scan(last_seen_timestamp, log=False):
  page = requests.get('https://www.hotelmarcopolocaorle.it/meteo/hmpolocaorle.php')
  tree = html.fromstring(page.content)

  timestamp_list = tree.xpath('/html/body/span')
  if (log):
    print(type(timestamp_list))
    for timestamp_ele in timestamp_list:
      print(type(timestamp_ele))
      print(timestamp_ele.text)

  timestamp_ele=timestamp_list[0].text
  # if (last_seen_timestamp == timestamp_ele):
  #   return timestamp_ele

  timestamp_string=timestamp_ele[-len('Dati in real-time aggiornati alle: ')+4:]
  from datetime import datetime
  timestamp_obj=datetime.strptime(timestamp_string, "%a, %d %b %Y %H:%M:%S %z")
  if (log):
    print("timestamp_obj")
    print(timestamp_obj)

  timestamp_string=timestamp_obj.strftime("%d/%m/%Y %H:%M:%S")
  if (log):  
    print("timestamp_string")
    print(timestamp_string)

  timestamp_string_date=timestamp_obj.strftime("%d/%m/%Y")
  if (log):  
    print("timestamp_string_date")
    print(timestamp_string_date)

  timestamp_string_time=timestamp_obj.strftime("%H:%M:%S")
  if (log):  
    print("timestamp_string_time")
    print(timestamp_string_time)

  wind_speed_elems = tree.xpath('/html/body/table/tbody/tr[2]/td[2]/h1[2]/big/big/big/span/text()')
  wind_speed=wind_speed_elems[0]
  wind_speed=wind_speed.strip()
  if (log):
    print("wind_speed")
    print(wind_speed)

  wind_direction = tree.xpath('/html/body/table/tbody/tr[2]/td[2]/h4/big/big/span/big/big/text()')
  wind_direction=wind_direction[0]
  if (log):
    print("wind_direction")
    print(wind_direction)

  pressure_ele = tree.xpath('/html/body/table/tbody/tr[2]/td[3]/h1[2]/big/span')
  pressure=pressure_ele[0].text
  pressure=pressure.strip()
  if (log):
    print("pressure")
    print(pressure)

  rain_today_ele = tree.xpath('/html/body/table/tbody/tr[4]/td[2]/h1[2]/big/span')
  rain_today=rain_today_ele[0].text
  rain_today=rain_today[:1]
  rain_today=rain_today.strip()
  if (log):
    print("rain_today")
    print(rain_today)

  rain_rate_ele = tree.xpath('/html/body/table/tbody/tr[4]/td[2]/h2')
  rain_rate=rain_rate_ele[0].text
  print(rain_rate)
  rain_rate=rain_rate[len('IntensitÃƒ'):]
  print(rain_rate)
  rain_rate=rain_rate[:3]
  print(rain_rate)
  rain_rate=rain_rate.strip()
  print(rain_rate)
  if (log):
    print("rain_rate")
    print(rain_rate)

  temperature_ele = tree.xpath('/html/body/table/tbody/tr[2]/td[1]/h1[3]/big/big/big')
  temperature=temperature_ele[0].text
  temperature=temperature[:len(temperature)-len("Â°C")+1]
  temperature=temperature.strip()
  if (log):
    print("temperature")
    print(temperature)

  humidity_ele = tree.xpath('/html/body/table/tbody/tr[3]/td/h1[2]/big/span')
  humidity=humidity_ele[0].text
  humidity=humidity[:len(humidity)-len(" %")]
  humidity=humidity.strip()
  if (log):
    print("humidity")
    print(humidity)

  uv_index_ele = tree.xpath('/html/body/table/tbody/tr[4]/td[1]/h1[2]/big/span')
  uv_index=uv_index_ele[0].text
  uv_index=uv_index.strip()
  if (log):
    print("uv_index")
    print(uv_index)

  heat_index_cels_ele = tree.xpath('/html/body/table/tbody/tr[2]/td[1]/h3[4]/big/span')
  heat_index=heat_index_cels_ele[0].text
  heat_index=heat_index[len('Indice di calore: '):]
  heat_index=heat_index[:len(heat_index)-len("°C")-1]
  heat_index=heat_index.strip()
  if (log):
    print("heat_index")
    print(heat_index)

  weather=[timestamp_string, timestamp_string_date, timestamp_string_time, wind_speed, wind_direction, pressure, rain_today, rain_rate, temperature, humidity, uv_index, heat_index]
  file_name="C:/temp/weather.txt"
  from csv import writer
  with open(file_name, 'a+', newline='') as write_obj:
    # Create a writer object from csv module
    csv_writer = writer(write_obj, delimiter=";")
    # Add contents of list as last row in the csv file
    csv_writer.writerow(weather)

  return timestamp_ele

import time
last_seen_timestamp=''
last_seen_timestamp=scan(last_seen_timestamp)
scan_no=0
while True:
  time.sleep(50)
  scan_no=scan_no+1
  print("scan "+ str(scan_no)+"...")
  last_seen_timestamp=scan(last_seen_timestamp)
