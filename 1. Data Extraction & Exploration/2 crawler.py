from bs4 import BeautifulSoup
import requests
import time
import csv
import sys
import pandas as pd

category = 'technology'
df = pd.read_csv('links_technology.csv')

user_agent = r'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
cookie_raw= '##delete for privacy'
cookies={}
for line in cookie_raw.split(';'):
    name,value=line.strip().split('=',1)
    cookies[name]=value

fieldnames = ['category','title','author','date','read_time','shares','content']
with open("article0.csv","w",encoding='utf_8_sig',newline ='') as file:   
    writer = csv.DictWriter(file,fieldnames = fieldnames, extrasaction ='ignore')
    writer.writeheader()
    for i in range(len(df['Links'])):
        url = df['Links'][i]
        s = requests.session()
        s.headers.update(headers)
        html = s.get(url, cookies=cookies)
#         time.sleep(1)
        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, 'lxml')
        #title
        if soup.select('h1'):
            title = soup.select('h1')[0].get_text()
        elif soup.select('.graf--leading'):
            title = soup.select('.graf--leading')[0].get_text()
        else: continue
        #date
        if soup.select('time'):
            date = soup.select('time')[0].get_text()
        else: 
            date = 'NA'
        #read_time
        if soup.select('span.readingTime'):
            read_time = soup.select('span.readingTime')[0]['title']
        else: read_time = 'NA'
        #shares
        if soup.select('.js-actionMultirecommend'):
            shares = soup.select('.js-actionMultirecommend')[0].get_text()
            if 'K' in shares:
                shares = shares.strip('K')
                shares = int(float(shares)*1000)
        else: shares = 0
        #author
        if soup.select('.ds-link'):
            author = soup.select('.ds-link')[0].get_text()
        elif soup.select('.link darker'):
            author = soup.select('.link darker')[0].get_text()
        else: continue
        #content
        contents = soup.select('.graf--p')
        content = ''
        for p in contents:
            content = content + p.get_text()
        detail = {'category':category,'title':title,'author':author,'date':date,'read_time':read_time,'shares':shares,'content':content}
        writer.writerow(detail)
        sys.stdout.write("Articles scrapped: %d / %d \r" % (i,len(df['Links'])) )  
        sys.stdout.flush()
     
            
            


