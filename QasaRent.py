### DO BEFORE RUNNING CODE!!!
### in cmd, run "pip install beautifulsoup4" to install beautifulsoup4 (details https://www.tutorialspoint.com/beautiful_soup/beautiful_soup_installation.htm)

from selenium import webdriver
import time
from bs4 import BeautifulSoup

browser = webdriver.Chrome("/Users/artc/Desktop/chromedriver.exe")
browser.get("https://en.qasa.se/p2/en/find-home/sweden?searchAreas[]=Solna%20kommun%3B%3B398040")
time.sleep(20)
content = browser.page_source
browser.quit()
soup = BeautifulSoup(content, "html.parser")
home_items = soup.find_all("div", attrs = {"class":"text__Text-sc-1ttkyfd-0 IFApQ"})
for n in range(len(home_items)):
    area = home_items[n].text.strip()
    key_info = area.split("•")
    print(key_info[2])
