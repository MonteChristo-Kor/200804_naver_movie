import requests
import csv
import os
import datetime
import itertools

from bs4 import BeautifulSoup

idx_num = 1

def main() :
    temp_list = []
    temp_dict = {}

    test_str, search_word, page_num = input_string()

    base_url = 'https://search.naver.com/search.naver?&where=news&query='
    mid_url = '&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=31&start='
    start_num = 1
    end_url = '&refresh_start=0'

    for num in range(start_num, (page_num*10)+1) :
        URL = base_url + search_word + mid_url + str(num) + end_url

        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')

        temp_data = naver_searching_list(soup)
        temp_list.append(temp_data[0])
        temp_dict = dict(temp_dict, **temp_data[1])

    for i in range(1, page_num) :
        temp_list[0] += temp_list[1]
        del temp_list[1]

    temp_list = list(itertools.chain.from_iterable(temp_list))
    print(temp_list)

    save_sel = toCSV(temp_list, test_str)


def input_string() : 
    try :
        test_str = str(input("검색어를 입력하세요 : "))
        page_num = int(input("몇 페이지까지 크롤링 하시겠습니까? "))
    
        test_string = test_str.replace(" ", "+")
        encoded_1 = str(test_string.encode('utf-8')) # 검색어를 utf-8로 변환
        encoded_2 = encoded_1.replace(r"\x", "%") # utf-8로 변환 시 \x로 변환되는 것을 %로 변환
        encoded_3 = encoded_2.replace(r"+", "%20") # 스페이스바의 입력 문자인 '+'를 '%20'으로 변환
        encoded_4 = encoded_3[2:-1]
    except : 
        input_string()
    
    return test_str, encoded_4, page_num


def naver_searching_list(soup) :
    temp_dict = {}
    temp_list = []
    global idx_num

    naver_list = soup.select('div[id=wrap] > div[id=container] > div[id=content] > div[id=main_pack] > div.news.mynews.section._prs_nws > ul > li') 
    
    for news in naver_list :
        a_tag = news.select_one('dl > dt > a')
        news_title = a_tag['title']
        news_link = a_tag['href'] 
        temp_list.append([idx_num, news_title, news_link])
        idx_num += 1
        temp_dict[str(idx_num)] = {'News Title' : news_title, 'News Link' : news_link}

    return temp_list, temp_dict


def toCSV(temp_list, test_str) :
    path = "C:\Crawling"
    file_name = datetime.datetime.today().strftime('%Y%m%d') +"_" + test_str + ".csv"

    try : 
        save_sel = int(input("csv 파일로 저장하시겠습니까? (Yes : 1, No : 0) : "))
    
        if save_sel == 1 : 
            with open(os.path.join(path, file_name), 'w', encoding='euc-kr', newline='') as file :
                csvfile = csv.writer(file)
                for row in temp_list :
                    csvfile.writerow(row)                
                print("네이버 검색 크롤링을 마치겠습니다.")
                return 0        

        elif save_sel == 0 :
            print("감사합니다.")

    except :
        toCSV(temp_list, test_str)
        
    
go_to_csv = main()
go_to_csv
