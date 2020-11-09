import csv
from datetime import datetime
from lxml import html
import requests

import logging
import threading
import time

from utility import log_xpath_elem, convert_wind_direction_to_deg, get_identification_string, get_tree, save_v6
from scanner_meteosystem_alike_ws import scan_meteosystem_alike
from scanner_meteovenezia_alike_ws import scan_meteovenezia_alike
from scanner_hotelmarcopolo_caorle_alike_ws import scan_hotelmarcopolo_caorle_alike
from scanner_meteonetwork_alike_ws import scan_meteonetwork_alike
from scanner_cellarda_ws_alike_ws import scan_cellarda_ws_alike
from scanner_cellarda_nord_ws_alike_ws import scan_cellarda_nord_ws_alike

#
#
#
locations_json = [{
    "name": 'Bagno Margherita Caorle',
    "latitude": 45.588340,
    "longitude": 12.861544,
    "address_complete": "Viale Lepanto, 13A, 30021 Porto Santa Margherita VE",
    "street_1": "Viale Lepanto, 13A",
    "street_2": "Porto Santa Margherita",
    "zip": "30021",
    "town": "Caorle",
    "province": "VE",
    "country": "IT",
    "note": "Meteo station @ https://www.meteo-caorle.it/, Porto Santa Margherita, Spiaggia Est, Caorle, Venezia",
    "height_asl_m": 0
}, {
    "name": 'San Giorgio, Venezia',
    "latitude": 45.429939,
    "longitude": 12.342716,
    "address_complete": "30100 Venezia, Città Metropolitana di Venezia",
    "street_1": "",
    "street_2": "",
    "zip": "30100",
    "town": "Venezia",
    "province": "Città Metropolitana di Venezia",
    "country": "IT",
    "note": "Meteo station @ https://www.meteo-venezia.net/compagnia01.php, Isola di San Giorgio Maggiore, Venezia",
    "height_asl_m": 0
}, {
    "name": 'Punta San Giuliano, Mestre-Venezia',
    "latitude": 45.629892,
    "longitude": 12.997956,
    "address_complete": "Via S. Giuliano, 23, 30174 Venezia VE",
    "street_1": "Via S. Giuliano, 23",
    "street_2": "",
    "zip": "30174",
    "town": "Mestre",
    "province": "VE",
    "country": "IT",
    "note": "Meteo station @ https://www.meteo-venezia.net/, Punta San Giuliano, Mestre-Venezia",
    "height_asl_m": 0
}, {
    "name": 'Laguna Park Hotel, Bibione, Venezia',
    "latitude": 45.466542,
    "longitude": 12.282729,
    "address_complete": "Via Passeggiata al Mare, 20, 30028 Bibione VE",
    "street_1": "Via Passeggiata al Mare, 20",
    "street_2": "",
    "zip": "30028",
    "town": "Bibione",
    "province": "VE",
    "country": "IT",
    "note": "Meteo station @ https://www.bibione-meteo.it/, Bibione, Venezia",
    "height_asl_m": 0
}, {
    "name": 'Hotel "Marco Polo", Caorle',
    "latitude": 45.5978224,
    "longitude": 12.8839359,
    "address_complete": "Via della Serenissima, 22, 30021 Caorle VE",
    "street_1": "Via della Serenissima, 22",
    "street_2": None,
    "zip": "30021",
    "town": "Caorle",
    "province": "VE",
    "country": "IT",
    "note": "Meteo station @ https://www.hotelmarcopolocaorle.it/meteo/hmpolocaorle.php",
    "height_asl_m": 0
}, {
    "name": 'Meteo Network stazione meteo di Feltre',
    "latitude": 46.016,
    "longitude": 11.895,
    "address_complete": None,
    "street_1": None,
    "street_2": None,
    "zip": "32032",
    "town": "Feltre",
    "province": "BL",
    "country": "IT",
    "note": "Meteo station @ http://my.meteonetwork.it/station/vnt336/, Model: MTX, Type: Semi-Urbana, Ubicazione: Campo aperto",
    "height_asl_m": 267
}, {
    "name": 'Osservatorio meteorologico di I.I.S. Agrario “Antonio della Lucia” di Feltre (BL)',
    "latitude": 46.036,
    "longitude": 11.937,
    "address_complete": "Via Vellai, 41, 32032 Vellai BL",
    "street_1": "Via Vellai,",
    "street_2": None,
    "zip": "32032",
    "town": "Feltre",
    "province": "BL",
    "country": "IT",
    "note": "Meteo station @ http://www.meteosystem.com/dati/feltre/dati.php, Model: Davis Vantage Pro 2",
    "height_asl_m": 330
}, {
    "name": 'LaCrosse WS2300 di Pellencin Giorgio, Cellarda Sud, Feltre (BL)',
    "latitude": 46.011,
    "longitude": 11.966,
    "address_complete": "Cellarda Sud, 32032 Feltre (BL)",
    "street_1": "Cellarda Sud",
    "street_2": None,
    "zip": "32032",
    "town": "Feltre",
    "province": "BL",
    "country": "IT",
    "note": "Stazione Meteo di Pellencin Giorgio, Cellarda Sud, @ http://www.celarda.altervista.org/index.htm, Model: LaCrosse WS2300",
    "height_asl_m": 225
}, {
    "name": 'LaCrosse WS2300 di Pellencin Giorgio, Cellarda Nord, Feltre (BL)',
    "latitude": 46.011,
    "longitude": 11.966,
    "address_complete": "Cellarda Nord, 32032 Feltre (BL)",
    "street_1": "Cellarda Nord",
    "street_2": None,
    "zip": "32032",
    "town": "Feltre",
    "province": "BL",
    "country": "IT",
    "note": "Stazione Meteo di Pellencin Giorgio, Cellarda Nord, @ http://www.meteocelarda.altervista.org/index.htm, Model: LaCrosse WS2300",
    "height_asl_m": 225
}]

# "scan_time_interval" in seconds
servers = [
  { "location_id":  1, "location": locations_json[4], "to_be_started": True, "name": "hotelmarcopolo_caorle", "url": "https://www.hotelmarcopolocaorle.it/meteo/hmpolocaorle.php", "scanner": scan_hotelmarcopolo_caorle_alike, "scan_time_interval": 55 }, # Wait for 50 secs
  { "location_id":  4, "location": locations_json[0], "to_be_started": True, "name": "bagnomargherita_caorle", "url": "https://www.meteo-caorle.it/", "scanner": scan_meteovenezia_alike, "scan_time_interval": 55 },
  { "location_id":  8, "location": locations_json[1], "to_be_started": True, "name": "sangiorgio_venezia", "url": "https://www.meteo-venezia.net/compagnia01.php", "scanner": scan_meteovenezia_alike, "scan_time_interval": 55 },
  { "location_id":  9, "location": locations_json[2], "to_be_started": True, "name": "puntasangiuliano_mestre", "url": "https://www.meteo-venezia.net/", "scanner": scan_meteovenezia_alike, "scan_time_interval": 55 },
  { "location_id": 10, "location": locations_json[3], "to_be_started": True, "name": "lagunaparkhotel_bibione", "url": "https://www.bibione-meteo.it/", "scanner": scan_meteovenezia_alike, "scan_time_interval":55 },
  { "location_id": 11, "location": locations_json[5], "to_be_started": True, "name": "meteonetwork_feltre", "url": "http://my.meteonetwork.it/station/vnt336/", "scanner": scan_meteonetwork_alike, "scan_time_interval": 60*30 }, # Wait for half an hour
  { "location_id": 12, "location": locations_json[6], "to_be_started": True, "name": "agrario_feltre", "url": "http://www.meteosystem.com/dati/feltre/dati.php", "scanner": scan_meteosystem_alike, "scan_time_interval": 55 },
  { "location_id": 15, "location": locations_json[7], "to_be_started": True, "name": "cellarda_sud_feltre", "url": {"1": "http://www.celarda.altervista.org/index.htm", "2": "http://my.meteonetwork.it/station/vnt374/" }, "scanner": scan_cellarda_ws_alike, "scan_time_interval": 60*5 },
  { "location_id": 16, "location": locations_json[8], "to_be_started": True, "name": "cellarda_nord_feltre", "url": "http://www.meteocelarda.altervista.org/index.htm", "scanner": scan_cellarda_nord_ws_alike, "scan_time_interval": 60*5 } # Wait five minutes
]

SCAN_TIME_INTERVAL_DEFAULT=50 # Sec

#
#
#
def main_logger(server, save=True, log=False):
  logging.info(f'Thread ident: {threading.get_ident()}, Client for server: {server["location_id"]}, {server["name"]}, url: {server["url"]} up and running.')
  scanner=server["scanner"]
  scan_time_interval=server.get("scan_time_interval")
  if not scan_time_interval:
    scan_time_interval=SCAN_TIME_INTERVAL_DEFAULT
  while True:
    last_seen_timestamp=server.get("last_seen_timestamp", None)
    scan_no=server.get("scan_no", 0)
    scan_no=scan_no+1
    logging.info(f'{get_identification_string(server["location_id"], server["name"])}, scan: {scan_no}...')
    last_seen_timestamp=scanner(last_seen_timestamp, server, save, log)
    server["last_seen_timestamp"]=last_seen_timestamp
    server["scan_no"]=scan_no
    time.sleep(scan_time_interval)

#
#
#
def add_server_location(server):
    location_json=server["location"]
    headers={'Content-Type': 'application/json; charset=utf-8'}
    response=requests.post('http://localhost:8080/api/location', headers=headers, json=location_json)
    logging.info(f'Location id: {server["location_id"]}, name: {server["name"]}, response: {response}')

#
#
#
def add_server_locations(servers):
  for server in servers:
    location_id=server["location_id"]
    if location_id==13 or location_id==14:
      add_server_location(server)

#
#
#
if __name__=="__main__":
  #add_server_locations(servers)
  format = "%(asctime)s %(thread)d %(threadName)s: %(message)s"
  logging.basicConfig(filename="app/log/meteo_data_repo3.log", format=format, level=logging.NOTSET, datefmt="%Y-%m-%d %H:%M:%S")

  logging.info('##')
  logging.info("## 'Meteo data repo' data collector clients launcher")
  logging.info('##')
  logging.info('Starting clients...')
  nclients=0
  for server in servers:
    to_be_started=server["to_be_started"]
    if to_be_started==False:
      logging.info(f'Server: {server["location_id"]}, {server["name"]}, url: {server["url"]} starting DISABLED.')
      continue

    logging.info(f'Starting client for server: {server["location_id"]}, {server["name"]}, url: {server["url"]}...')
    threading.Thread(target=main_logger, args=(server, )).start()
    nclients=nclients+1

  logging.info(f'Clients starting complete. Started: {nclients} clients. Launcher ends.')
