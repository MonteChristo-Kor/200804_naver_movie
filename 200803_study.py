import requests
from bs4 import BeautifulSoup
import csv

soup_objects = []
temp_list = []

for page in range(1, 102, 10) :

    base_url = 'https://search.naver.com/search.naver?&where=news&query=%EA%B4%91%EC%A3%BC%20%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5%20%EC%82%AC%EA%B4%80%ED%95%99%EA%B5%90&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=47&start='
    num = page
    end_url = '&refresh_start=0'

    URL = base_url + str(num) + end_url

    reponse = requests.get(URL)

    soup = BeautifulSoup(reponse.text, 'html.parser') 
    soup_objects.append(soup)

for soup in soup_objects :    
    news_section = soup.select('div[id=wrap] > div[id=container] > div[id=content] > div[id=main_pack] > div.news.mynews.section._prs_nws > ul > li') 
    
    for i in news_section : 
        a_tag = i.select_one('dl > dt > a')
        news_title = a_tag['title']
        news_link = a_tag['href'] 
        temp_list = {
            "news_title" : news_title, 
            "link" : news_link
        }

        with open("test_01.csv", 'a') as file :
            fieldnames = ['news_title', 'link']
            csvfile = csv.DictWriter(file, fieldnames=fieldnames)           
            csvfile.writerow(temp_list)