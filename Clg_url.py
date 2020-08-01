import requests
from bs4 import BeautifulSoup

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


def url_list():
    ur = "https://www.indiacollegeshub.com/engineering/colleges-india"
    s  = ".aspx"
    url = ur + s
    page_urls.append(url)
    for i in range(2,209):
        u = ur+"-page-"+str(i)+s  
        page_urls.append(u)


page_urls=[]
clg_url = []
url_list()
for i in range(len(page_urls)):
    get_clg_urls(page_urls[i])
print(len(page_urls),len(clg_url))