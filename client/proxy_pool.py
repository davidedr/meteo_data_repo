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
TEST_TIMEOUT=3 # s
proxies_pool={}

#
#
#
def init_proxy_pool():

  get_proxies_pool()

  global proxies_pool
  if proxies_pool is None or proxies_pool.get("len") is None or proxies_pool.get("len")==0:
    return 0
  return proxies_pool.get("len")

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
    response = requests.get(TEST_URL, proxies={ "http": proxy, "https": proxy }, timeout=TEST_TIMEOUT)

  except Exception as e:
    return False

  if response:
    return True

  return False

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

    tests_ok=proxies_pool.get("tests_ok")
    if tests_ok is None:
      tests_ok=0
    tests_nok=proxies_pool.get("tests_nok")
    if tests_nok is None:
      tests_nok=0

    proxy_ok=test_proxy(proxy)
    if proxy_ok:
      tests_ok=tests_ok+1
      proxies_pool["tests_ok"]=tests_ok
      logging.info(f'{utility.get_identification_string(location_id, server_name)}: {i}-th proxy {proxy} working. tests_ok: {tests_ok}, tests_nok: {tests_nok}, %: {float(tests_ok/(tests_ok+tests_nok)*100)}.')
      return proxy
    else:
      tests_nok=tests_nok+1
      proxies_pool["tests_nok"]=tests_nok
      logging.info(f'{utility.get_identification_string(location_id, server_name)}: {i}-th proxy {proxy} NOT working. tests_ok: {tests_ok}, tests_nok: {tests_nok}, %: {float(tests_ok/(tests_ok+tests_nok)*100)}.')

  logging.info(f'{utility.get_identification_string(location_id, server_name)}: No working proxy found!')
  return None

#
#
#
if __name__=="__main__":
  proxy=get_proxy()
  if proxy:
    print(proxy)
    import definitions
    location_id=1
    server=utility.find_server(location_id)
    tree, _=utility.get_tree(server["url"], server["location_id"], server["name"])
    print(tree)

  else:
    print("No valid proxy found!")
