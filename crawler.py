import requests
from bs4 import BeautifulSoup as BS
import re

session = requests.session()
page = session.post('http://www.indianspices.com/dailyprice/ListAutionDetails.php')

#Home Page details

page = BS(page.text,"html.parser").find('div',{'class':'pagination'})
print(page)
