from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
import utility
import time
from selenium.webdriver.chrome.options import Options

weather_station_url="https://app.weathercloud.net/map#6903598366"


chrome_options=Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome('./utility/chromedriver/chromedriver.exe',
  options=chrome_options)
driver.get(weather_station_url)
time.sleep(15)
page_source=driver.page_source
driver.quit()
soup = BeautifulSoup(page_source, "html.parser")
print(soup.findAll('span', {"class": 'pull-right' })[1].text)