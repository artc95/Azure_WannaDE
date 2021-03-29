### DO BEFORE RUNNING CODE!!!
### in cmd, run "pip install beautifulsoup4" to install beautifulsoup4 (details https://www.tutorialspoint.com/beautiful_soup/beautiful_soup_installation.htm)
### change Chrome Webdriver path in "Extract" sections if different path

from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd

#--------EXTRACT FROM QASA, CREATE QASA.CSV--------#
browser = webdriver.Chrome("/Users/artc/Desktop/chromedriver.exe") # change chromedriver.exe path if different
browser.get("https://en.qasa.se/p2/en/find-home/sweden?searchAreas[]=Solna%20kommun%3B%3B398040")
time.sleep(10) # time to load

try: # ACCEPT COOKIES to access other buttons
    browser.find_element_by_xpath("//button[@class='sc-hKgILt hPMLcZ general-cookie-consent__AcceptButton-mls226-1 ejXQzy']").click()
except:
    print("Agreed to cookies.")

can_load_more = True # click on "LOAD MORE" BUTTON until all listings shown and cannot "Load more"
while can_load_more:
    try: # find and click "Load more", then give time to load
        browser.find_element_by_xpath("//button[@class='sc-hKgILt hPMLcZ pagination__StyledButton-sc-17c2n48-2 kFYVIO']").click()
        time.sleep(4)
    except: # cannot find "Load more" once all listings loaded, so end this loop
        print("All listings loaded.")
        time.sleep(4)
        can_load_more = False

names = []
urls = []
rooms = []
areas = []
monthly_prices_sek = []

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
        info_header = key_info_soup[n].find("div", attrs = {"class":"text__Text-sc-1ttkyfd-0 IFApQ"}).text.strip()
        key_info = info_header.split("•")
        if key_info[1][-5:] == "rooms": # because room info might contain "room" or "rooms"
            rooms_int = float(key_info[1].replace(" rooms", ""))
        else:
            rooms_int = float(key_info[1].replace(" room", ""))
        area = int(key_info[2].replace("m²", ""))
        rooms.append(rooms_int)
        areas.append(area)

        # extract listing prices
        price_soup = key_info_soup[n].find("div", attrs = {"class": "text__Text-sc-1ttkyfd-0 home-item__Rent-sc-1tbgb3o-9 fijJmN hPnVyJ"}).text.strip()
        price = int(price_soup[4:].replace(",", ""))
        monthly_prices_sek.append(price)

    except Exception as ex:
        print("Not a listing <div>. " + str(ex))
        
qasa_dict = {
    "name": names,
    "url": urls,
    "rooms": rooms,
    "area": areas,
    "monthly_price_sek": monthly_prices_sek
}

qasa_df = pd.DataFrame(qasa_dict, columns = ["name", "url", "rooms", "area", "monthly_price_sek"])

# qasa.csv might already exist, so check if ok to overwrite
overwrite_csv = input("If qasa.csv already exists, it will be overwritten. Press Enter to proceed, Ctrl + C to terminate.")
csv_file = qasa_df.to_csv("qasa.csv")

#--------EXTRACT FROM BLOCKET BOSTAD, CREATE BLOCKET.CSV--------#

browser = webdriver.Chrome("/Users/artc/Desktop/chromedriver.exe") # change chromedriver.exe path if different
browser.get("https://bostad.blocket.se/p2/sv/find-home/Stockholm%20Solna/l%C3%A4genhet?homeTypes[]=apartment&searchAreas[]=Stockholm%20Solna%3BStockholm%20Solna%3BStockholm%20Solna")
time.sleep(10) # time to load

try: # ACCEPT COOKIES to access listings
    browser.find_element_by_xpath("//button[@class='sc-hKgILt esLDzC blocket-cookie-consent___StyledButton-fscird-8 epUktU']").click()
except:
    print("Agreed to cookies.")

can_load_more = True # click on "LOAD MORE" BUTTON until all listings shown and cannot "Load more"
while can_load_more:
    try: # find and click "Load more", then give time to load
        browser.find_element_by_xpath("//button[@class='sc-hKgILt evzPbN pagination__StyledButton-sc-17c2n48-2 kFYVIO']").click()
        time.sleep(4)
    except: # cannot find "Load more" once all listings loaded, so end this loop
        print("All listings loaded.")
        time.sleep(4)
        can_load_more = False

names = []
urls = []
rooms = []
areas = []
monthly_prices_sek = []

content = browser.page_source
browser.quit()
soup = BeautifulSoup(content, "html.parser")
key_info_soup = soup.find_all("div", attrs = {"class": None, "id": None, "style":None}) # find all <div>s with no attributes

for n in range(len(key_info_soup)):
    try: # some <div>s with no attributes are not listings, so try-except
        # extract listing name
        name = key_info_soup[n].find("div", attrs = {"class":"text__Text-sc-1ttkyfd-0 iOhQqm"}).text.strip()
        names.append(name)

        # extract listing url
        url_soup = key_info_soup[n].find("a")
        urls.append("https://bostad.blocket.se/" + url_soup["href"]) # href in <a> is partial, so complete it with "https..."
        
        # extract listing rooms, area
        info_header = key_info_soup[n].find("div", attrs = {"class":"text__Text-sc-1ttkyfd-0 IFApQ"}).text.strip()
        key_info = info_header.split("•")
        rooms_int = float(key_info[1].replace(" rum", ""))
        area = int(key_info[2].replace("m²", ""))
        rooms.append(rooms_int)
        areas.append(area)

        # extract listing prices
        price_soup = key_info_soup[n].find("div", attrs = {"class": "text__Text-sc-1ttkyfd-0 home-item__Rent-sc-1tbgb3o-9 fijJmN hPnVyJ"}).text.strip()
        price = int(price_soup[:-7]+price_soup[-6:-3]) # concatenate digits only
        monthly_prices_sek.append(price)

    except Exception as ex:
        print("Not a listing <div>. " + str(ex))

blocket_dict = {
    "name": names,
    "url": urls,
    "rooms": rooms,
    "area": areas,
    "monthly_price_sek": monthly_prices_sek
}

blocket_df = pd.DataFrame(blocket_dict, columns = ["name", "url", "rooms", "area", "monthly_price_sek"])

# blocket.csv might already exist, so check if ok to overwrite
overwrite_csv = input("If blocket.csv already exists, it will be overwritten. Press Enter to proceed, Ctrl + C to terminate.")
csv_file = blocket_df.to_csv("blocket.csv")