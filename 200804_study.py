import csv
import requests
from bs4 import BeautifulSoup

# 주소의 패턴 확인
# 1. 영화별 주소 
#  - 강철비 : https://movie.naver.com/movie/bi/mi/point.nhn?code=188909 // /movie/bi/mi/basic.nhn?code=188909
#  - 부산행 : https://movie.naver.com/movie/bi/mi/point.nhn?code=185917
#  - 빅샤크3 : https://movie.naver.com/movie/bi/mi/basic.nhn?code=194799


# movie_address = 주소를 가져와서 basic -> point로 변경

main_add = "/movie/running/current.nhn" # 메인 페이지 주소 저장
move_add = ""                           # 각 영화의 리뷰 주소 저장, 매번 변환
review_add = "/movie/bi/mi/point.nhn?code=188909"

f_url = "http://movie.naver.com"
l_url = review_add

URL = f_url + l_url

response = requests.get(URL)

soup = BeautifulSoup(response.text, 'html.parser')

page_r = soup.select_one('div[id=wrap] > div[id=container] > div[id=content] > div.article > div.section_group.section_group_frst > div.obj_section.noline > div.ifr_module2 > div.paging')
# > a')

#page_path = page_r['href']


print(page_r)
