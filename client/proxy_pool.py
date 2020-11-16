import requests
from lxml.html import fromstring
from itertools import cycle
import logging

import utility

#
# GLobals
#
PROXY_LIST_HOME='https://free-proxy-list.net/'
TEST_URL='https://httpbin.org/ip'
proxies_pool={}

#
#
#
def get_proxies_pool(location_id=None, server_name=None):

  try:
    response=requests.get(PROXY_LIST_HOME)

  except Exception as e:
    logging.info(f'{utility.get_identification_string(location_id, server_name)}: Failed to get proxy list: {e}!')
    return

  if response is None:
    logging.info(f'{utility.get_identification_string(location_id, server_name)}: response is None in response=requests.get(PROXY_LIST_HOME)!')
    return

  parser=fromstring(response.text)
  proxies=set()
  proxies_elems=parser.xpath('//tbody/tr')
  for i in proxies_elems:
    if i.xpath('.//td[7][contains(text(),"yes")]'):
      proxy=":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
      proxies.add(proxy)

  global proxies_pool
  proxies_pool["len"]=len(proxies)
  proxies_pool["pool"]=cycle(proxies)

  return proxies_pool

#
#
#
def test_proxy(proxy):
  try:
    response = requests.get(TEST_URL, proxies={ "http": proxy, "https": proxy })

  except Exception as e:
    return False

  return True

 #
 #
 #
def get_proxy(location_id=None, server_name=None):
  global proxies_pool
  if proxies_pool is None or proxies_pool.get("len") is None or proxies_pool.get("len")==0:
    get_proxies_pool()

  if proxies_pool is None or proxies_pool["len"]==0:
    logging.info(f'{utility.get_identification_string(location_id, server_name)}: Unable to get proxyes list!')
    return None

  for i in range(proxies_pool["len"]):
    proxy=next(proxies_pool["pool"])
    logging.info(f'{utility.get_identification_string(location_id, server_name)}: Testing {i}-th proxy {proxy}...')
    proxy_ok=test_proxy(proxy)
    if proxy_ok:
      logging.info(f'{utility.get_identification_string(location_id, server_name)}: {i}-th proxy {proxy} working!')
      return proxy

  logging.info(f'{utility.get_identification_string(location_id, server_name)}: No working proxy found!')
  return None

#
#
#
if __name__=="__main__":
  proxy=get_proxy()
  if proxy:
    print(proxy)
  else:
    print("No valid proxy found!")
