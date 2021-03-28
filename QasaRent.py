### DO BEFORE RUNNING CODE!!!
### in cmd, run "pip install beautifulsoup4" to install beautifulsoup4 (details https://www.tutorialspoint.com/beautiful_soup/beautiful_soup_installation.htm)
import requests
from bs4 import BeautifulSoup

r = requests.get("https://en.qasa.se/p2/en/find-home/sweden?searchAreas[]=Solna%20kommun%3B%3B398040")
r_soup = BeautifulSoup(r.text, "html.parser")
print(r_soup)