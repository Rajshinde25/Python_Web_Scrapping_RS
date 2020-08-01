import requests
from bs4 import BeautifulSoup
import csv
from collections import OrderedDict 
import re
import pandas as pd
from matplotlib import pyplot as plt

#Function stores list of pages available on site in page_url[] list
def url_list():
    ur = "https://www.indiacollegeshub.com/engineering/colleges-india"
    s  = ".aspx"
    url = ur + s
    page_urls.append(url)
    for i in range(2,179):
        u = ur+"-page-"+str(i)+s  
        page_urls.append(u)

#fuction returns college url available on each page in clg_url[] list
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

    for h3 in soup1.find_all('h3'):
       collegesDict[h3.get_text()]=""

    for h in soup1.find_all('h3'):
        s = h.get_text()
        v = re.findall(",\s[A-z]{0,20}",s)
        if len(v)== 0:
            district = "N\A"
        else:
            district = v[0]
            district = district[2:]
        locationList.append(district)
    
    for div in soup1.find_all('div',class_="clg-cntent"):
        s1 = div.find('p').get_text()
        s = re.findall("-[\s\w{2,20}+]*,\sIndia",s1)
        state = s[0]
        state =state[2:]
        state = state[:-7]
        locationList2.append(state)

    i=0
    for k in list(collegesDict.keys()):
        collegesDict[k]=[locationList[i],locationList2[i]]
        i=i+1
#Function to collect college details 
def clg_det(site_url):
    s = requests.get(site_url)
    mainpage = s.content
    soup = BeautifulSoup(mainpage,'html.parser')

    table = soup.find('table',class_ = "table tb-icons")
    clgnm = soup.find(text="College Name").findNext('td').contents[0]
    address = table.find('span', id = "ContentPlaceHolder1_lbl_address" ).get_text()
    contact = table.find('span', id="ContentPlaceHolder1_lbl_phone").get_text()
    email = table.find('span',id="ContentPlaceHolder1_lbl_email").get_text()
    website = table.find('span',id="ContentPlaceHolder1_lbl_website").get_text()
    
    if contact != "N/A":
        tmpval=collegesDict[clgnm]
        tmpval.append(address)
        tmpval.append(contact)
        tmpval.append(email)
        tmpval.append(website)
        collegesDict[clgnm]=tmpval
 
        finalList=[clgnm,tmpval[2],tmpval[0],tmpval[1],tmpval[3],tmpval[4],tmpval[5]]
        writer.writerow(finalList)

def plot_graphs():
    df = pd.read_csv (r'output.csv',encoding='cp1252')

    k=df.groupby(by='State').agg('count')
    k["College Name"].plot(kind ='bar')

    plt.title('Total Colleges in repective States')
    plt.xlabel('States')
    plt.ylabel('Count')
    plt.ylim(0,300)
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.4)
    plt.show(block=True)

    unique = df.groupby('State')['District'].nunique()
    unique.plot.bar(x='DISTRICT', y='STATE',color = "purple")
    plt.title('Total District in repective States')
    plt.xlabel('States')
    plt.ylabel('Count')
    plt.ylim(0,100)
    plt.subplots_adjust(bottom = 0.4)
    plt.show(block=True)



#execution starts from here
#initalization 
page_urls=[]
clg_url = []
count = 0
collegesDict =OrderedDict([])
locationList=[]
locationList2 = []

file = open('output.csv' , 'w', newline="")
writer = csv.writer(file)
writer.writerow(['College Name','Address','District','State','Contact number','Email id','Website'])

#call fuction
url_list()

for i in range(len(page_urls)):
    get_clg_urls(page_urls[i])

for j in range(len(clg_url)):
   clg_det(clg_url[j])

plot_graphs()


