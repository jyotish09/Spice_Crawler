import requests
from bs4 import BeautifulSoup as BS
import re

session = requests.session()
page = session.post('http://www.indianspices.com/dailyprice/ListAutionDetails.php')

#Home Page details

homepage = BS(page.text,"html.parser").find('div',{'class':'pagination'})
# print(homepage)

# Finding total number of pages

pages = homepage.find_all('a', href = re.compile(r'.*\?page.*'))
numPages = len(pages)-1
print(numPages)
