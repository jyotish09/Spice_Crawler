import requests, urllib, re, os
from bs4 import BeautifulSoup as BS

session = requests.session()
currentPageNum = 1
pageURL = 'http://www.indianspices.com/dailyprice/ListAutionDetails.php?page='+str(currentPageNum)
auctionReportURL = 'http://www.indianspices.com/dailyprice/'
page = session.post(pageURL)

# Home Page details
# Finding total number of pages
# print("\n  Finding total number of pages \n ")
homepage = BS(page.text,"html.parser").find('div',{'class':'pagination'})
# print(homepage)

pages = homepage.find_all('a', href = re.compile(r'.*\?page.*'))
numPages = len(pages)-1
print( " " + str(numPages) + " Number of pages \n")

auctionerNames = []
downloadPDFLinks = []
fileNames = []

# Checking Tables in current page

while(currentPageNum <= numPages):

    auctionerNames.append("\n ******* For Page "+str(currentPageNum))
    fileNames.append(" ******* \n ")
    currentPageURL = 'http://www.indianspices.com/dailyprice/ListAutionDetails.php?page='+str(currentPageNum)
    currentPage = session.post(currentPageURL)
    print("\n Checking Tables in current page , for now page = "+ str(currentPageNum) +" \n ")
    linksInCurrentPage = BS(currentPage.text,"html.parser").find_all('td',{'width':'58%'})


    for i in linksInCurrentPage:
        if(i.get_text().strip() != "Auctioner Name"):
            auctionerNames.append(i.get_text().strip())
            print(i.get_text().strip())
    # print(auctionerNames)

    # Checking PDF links in the table
    print("\n Checking PDF links in the table \n ")
    pdfLinksInCurrentPage = BS(currentPage.text,"html.parser").find_all('td',{'width':'14%'})
    for i in pdfLinksInCurrentPage:
        if(i.find("a",href=True)):
            downloadPDFLinks.append(auctionReportURL+(i.find("a")['href']).replace(" ", "%20"))
            fileNames.append((i.find("a")['href'][20:]).replace(" ", "_"))
            print((i.find("a")['href'][20:]).replace(" ", "_"))
    currentPageNum+=1

###### File Write Operations ######

print("Linking Auctioner Names with PDF Name in PDF_Names.txt "+str(len(fileNames))+" file ")

destination = 'DownloadedContents'
if not os.path.exists(destination):
    os.makedirs(destination)

# Writing The auctioner name along with their filename for easy reference

k = 0
text  = ''

pdfLinking = os.path.join(destination, "PDF_Names.txt")
linkingFiles = open(pdfLinking, "a+")

for i in fileNames:
    text = "\n "+auctionerNames[k]+" - "+fileNames[k]
    linkingFiles.write(text)
    k+=1
    text = ""

linkingFiles.close()
k = 0

# Writing the files to DownloadedPDFs folder
print(" Downloading the PDFs now : "+str(len(downloadPDFLinks))+" files ")
for item in downloadPDFLinks:
     r = requests.get(item)
     filename = item[59:].replace("%20", "_")
     print(filename)
     with open(destination+"/"+filename,'wb') as f:
         f.write(r.content)
     k+=1


print("Download Completed !!!!")
