import requests
from bs4 import BeautifulSoup as BS
import re

session = requests.session()
pageURL = 'http://www.indianspices.com/dailyprice/ListAutionDetails.php?page=1'
auctionReportURL = 'http://www.indianspices.com/dailyprice/'
page = session.post(pageURL)

#Home Page details
# Finding total number of pages
print("\n  Finding total number of pages \n ")
homepage = BS(page.text,"html.parser").find('div',{'class':'pagination'})
print(homepage)

pages = homepage.find_all('a', href = re.compile(r'.*\?page.*'))
numPages = len(pages)-1
# print(numPages)

#Checking Tables in current page , for now page = 1
print("\n Checking Tables in current page , for now page = 1 \n ")
linksInCurrentPage = BS(page.text,"html.parser").find_all('td',{'width':'58%'})

for i in linksInCurrentPage:
    print(i.get_text().strip())

#Checking PDF links in the table
print("\n Checking PDF links in the table \n ")
pdfLinksInCurrentPage = BS(page.text,"html.parser").find_all('td',{'width':'14%'})

for i in pdfLinksInCurrentPage:
    if(i.find("a",href=True)):
        print(auctionReportURL+(i.find("a")['href']).replace(" ", "%20"))
