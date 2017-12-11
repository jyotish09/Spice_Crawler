import requests, urllib, re, os
from bs4 import BeautifulSoup as BS

session = requests.session()
pageURL = 'http://www.indianspices.com/dailyprice/ListAutionDetails.php?page=14'
auctionReportURL = 'http://www.indianspices.com/dailyprice/'
page = session.post(pageURL)

# Home Page details
# Finding total number of pages
# print("\n  Finding total number of pages \n ")
homepage = BS(page.text,"html.parser").find('div',{'class':'pagination'})
# print(homepage)

pages = homepage.find_all('a', href = re.compile(r'.*\?page.*'))
numPages = len(pages)-1
# print( " " + str(numPages) + " Number of pages \n")

# Checking Tables in current page , for now page = 1
print("\n Checking Tables in current page , for now page = 1 \n ")
linksInCurrentPage = BS(page.text,"html.parser").find_all('td',{'width':'58%'})

auctionerNames = []

for i in linksInCurrentPage:
    if(i.get_text().strip() != "Auctioner Name"):
        auctionerNames.append(i.get_text().strip())
print(auctionerNames)

# Checking PDF links in the table
print("\n Checking PDF links in the table \n ")
pdfLinksInCurrentPage = BS(page.text,"html.parser").find_all('td',{'width':'14%'})
downloadPDFLinks = []
fileName = []
for i in pdfLinksInCurrentPage:
    if(i.find("a",href=True)):
        downloadPDFLinks.append(auctionReportURL+(i.find("a")['href']).replace(" ", "%20"))
        fileName.append((i.find("a")['href'][20:]).replace(" ", "_"))

destination = 'DownloadedPDFs'
if not os.path.exists(destination):
    os.makedirs(destination)

# Writing The auctioner name along with their filename for easy reference

k = 0
text  = ''

for i in fileName:
    text += "\n "+auctionerNames[k]+" - "+fileName[k]
    k+=1

pdfLinking = os.path.join(destination, "PDF_Names.txt")

linkingFiles = open(pdfLinking, "w")

toFile = text

linkingFiles.write(toFile)

linkingFiles.close()

k = 0

for item in downloadPDFLinks:
     r = requests.get(item)
     filename = fileName[k]
     print(filename)
     with open(destination+"/"+filename,'wb') as f:
         f.write(r.content)
     k+=1
