### DO BEFORE RUNNING CODE!!!
### in cmd, run "pip install beautifulsoup4" to install beautifulsoup4 (details https://www.tutorialspoint.com/beautiful_soup/beautiful_soup_installation.htm)

from selenium import webdriver
import time
from bs4 import BeautifulSoup

browser = webdriver.Chrome("/Users/artc/Desktop/chromedriver.exe")
browser.get("https://en.qasa.se/p2/en/find-home/sweden?searchAreas[]=Solna%20kommun%3B%3B398040")
time.sleep(15)

"""initial_content = browser.page_source # not all listings shown yet
initial_soup = BeautifulSoup(content, "html.parser")"""


names = []
urls = []
rooms = []
areas = []
prices = []

content = browser.page_source
browser.quit()
soup = BeautifulSoup(content, "html.parser")
key_info_soup = soup.find_all("div", attrs = {"class": None, "id": None, "style":None}) # find all <div>s with no attributes

for n in range(len(key_info_soup)):
    try: # some <div>s with no attributes are not listings, so try-except
        # extract listing name
        name = key_info_soup[n].find("div", attrs = {"class":"text__Text-sc-1ttkyfd-0 hBZlMU"}).text.strip()
        names.append(name)

        # extract listing url
        url_soup = key_info_soup[n].find("a")
        urls.append("https://en.qasa.se" + url_soup["href"]) # href in <a> is partial, so complete it with "https..."
        
        # extract listing rooms, area
        info_header_soup = key_info_soup[n].find("div", attrs = {"class":"text__Text-sc-1ttkyfd-0 IFApQ"})
        info_header = info_header_soup.text.strip()
        key_info = info_header.split("•")
        rooms.append(key_info[1])
        areas.append(key_info[2])
    
    except:
        print("Not a listing <div>.")
        
print(names)
print(urls)
