import requests
from bs4 import BeautifulSoup
import csv


#get college urls from each page
def get_clg_urls(l1):
    s = requests.get(l1)
    mainpage = s.content
    soup1 = BeautifulSoup(mainpage,'html.parser')

    for div_tag in soup1.find_all('div',class_="clg-lists"):
        for uls in div_tag.find_all('ul'):
            for l1 in uls.find_all('li'):
                for a_tag in l1.find_all('a',href =True):
                    if a_tag not in clg_url:
                        clg_url.append(a_tag['href'])
    return clg_url

#list of pages available on site containt college list
def url_list():
    ur = "https://www.indiacollegeshub.com/engineering/colleges-india"
    s  = ".aspx"
    url = ur + s
    page_urls.append(url)
    for i in range(2,209):
        u = ur+"-page-"+str(i)+s  
        page_urls.append(u)

#get college details and store it in CSV file
def clg_det(site_url,count):
    s = requests.get(site_url)
    mainpage = s.content
    soup = BeautifulSoup(mainpage,'html.parser')

    table = soup.find('table',class_ = "table tb-icons")
    clgnm = soup.find(text="College Name").findNext('td').contents[0]
    address = table.find('span', id = "ContentPlaceHolder1_lbl_address" ).get_text()
    contact = table.find('span', id="ContentPlaceHolder1_lbl_phone").get_text()
    email = table.find('span',id="ContentPlaceHolder1_lbl_email").get_text()
    website = table.find('span',id="ContentPlaceHolder1_lbl_website").get_text()

    if contact != "N/A" or (website != "N/A" and email != "N/A") and (count <=1000 ):
        detail_list = [clgnm,address,contact,email,website]
        writer.writerow(detail_list)
        count=count+1



page_urls=[]
clg_url = []
count=0
url_list()
for i in range(2):
    get_clg_urls(page_urls[i])

print(len(page_urls),len(clg_url))

file = open('final-1.csv' , 'w', newline="")
writer = csv.writer(file)
writer.writerow(['College Name','Address','Contact number','Email id','Website'])

for j in range(10):
    clg_det(clg_url[j],count)