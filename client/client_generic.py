from datetime import datetime

import logging
import threading
import time

from definitions import locations_json, servers, SCAN_TIME_INTERVAL_DEFAULT
from utility import get_identification_string, add_server_location_if_doesnot_exist
import proxy_pool

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
def add_server_locations(servers):
  for server in servers:
    add_server_location_if_doesnot_exist(server)

#
#
#
if __name__=="__main__":
  format = "%(asctime)s %(thread)d %(threadName)s: %(message)s"
  logging.basicConfig(filename="app/log/meteo_data_repo3.log", format=format, level=logging.NOTSET, datefmt="%Y-%m-%d %H:%M:%S")

  add_server_locations(servers)
  
  logging.info('##')
  logging.info("## 'Meteo data repo' data collector clients launcher")
  logging.info('##')
  logging.info('Starting proxy pool...')
  nproxy_found=proxy_pool.init_proxy_pool()
  logging.info(f'Found: {nproxy_found} proxy servers.')
  logging.info('Starting clients...')
  nclients=0
  for server in servers:
    to_be_started=server["to_be_started"]
    # if server["location_id"]!=26:
    #   to_be_started=False

    if not to_be_started:
      logging.info(f'Server: {server["location_id"]}, {server["name"]}, url: {server["url"]} starting DISABLED.')
      continue

    logging.info(f'Starting client for server: {server["location_id"]}, {server["name"]}, url: {server["url"]}...')
    threading.Thread(target=main_logger, args=(server, )).start()
    nclients=nclients+1

  logging.info(f'Clients starting complete. Started: {nclients} clients. Launcher ends.')
