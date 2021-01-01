from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import json
from bs4 import BeautifulSoup
import time
from urllib.parse import quote, quote_plus
from urllib.request import urlopen
from .serializers import NaverSerializer
from .models import Naver
import flask

# app = flask.Flask(__name__)

@api_view(['POST'])
def index(request):

    # my_res = flask.Response('차단된다')
    client_id = 'B8wV6Y7kOQbv16yNZ8po' 
    client_secret = 'UDvZzy0onJ'
    headers = {'X-Naver-Client-Id':client_id, 'X-Naver-Client-Secret':client_secret}


    url_base="https://openapi.naver.com/v1/search/local.json?query="
    # keyword = quote(input("지역 및 먹고 싶은 음식을 입력해주세요! : "))
    # if weathers[0]['fields']['weather_summary'] == '흐림':
    #     keyword = '국밥'
    # elif weathers[0]['fields']['weather_summary'] == '구름많음':
    #     keyword = '전골'    
    keyword = request.data.get('keyword')
    print(keyword)

    url_middle="$&start="
    keyword_number='1'
    url_middle2 = "$&display="
    restaurant_display = '5'

    url = url_base + keyword + url_middle + keyword_number + url_middle2 + restaurant_display

    result = requests.get(url,headers = headers).json()  

    for lst in result['items']:
        lst['models'] = "restaurants.naver"

    print(result['items'])
    data = result['items']

    # with open('restaurants.json', 'w', encoding="utf-8") as make_file:
    #     json.dump(data, make_file, ensure_ascii=False, indent="\t")

    return Response(data)


@api_view(['GET', 'POST'])
def weather_info(request):
    global weathers
    if request.method == 'POST':
        # search = input('검색어를 입력해주세요. : ')
        search = request.data.get('search')

        url = f'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query={quote_plus(search)}%EB%82%A0%EC%94%A8&tqi=U95mQdprvOssseIM4VKssssss%2Bl-367438'
        # url = f'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EA%B0%95%EC%9B%90%EB%8F%84+%EB%82%A0%EC%94%A8&oquery=%EA%B0%95%EC%9B%90%EB%8F%84+%EB%82%A0%EC%94%A8&tqi=U9gK6lprvmsssCMZusdssssstzh-359477'
        html = urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        check_location_name = soup.find('span', {'class' : 'btn_select'}) 
        if 'None' in str(check_location_name): 
            print("지역 이름을 다시 입력해주세요.") 
        else: 
            # 지역 정보 
            for i in soup.select('span[class=btn_select]'): 
                location = i.text 

            data1 = soup.find('div', {'class': 'detail_box'})
            data2 = data1.findAll('dd')

            # 미세먼지(dust), 초미세먼지(little_dust)
            dust = data2[0].find('span', {'class': 'num'}).text
            little_dust = data2[1].find('span', {'class': 'num'}).text

            # 현재 온도 
            now_temp = soup.find('span', {'class': 'todaytemp'}).text + soup.find('span', {'class' : 'tempmark'}).text[2:] 

            # 날씨
            weather_detail = soup.find('p', {'class' : 'cast_txt'}).text 
            comma_index = weather_detail.index(',')
            # weather_summary = 좋음, 구름많음, 흐림 등 요약 정보만 뽑아 저장한 변수
            weather_summary = weather_detail[0:comma_index]

            temp_dict = {
                'location': location,
                'weather_summary': weather_summary,
                'now_temp': now_temp,
                'dust': dust,
                'little_dust': little_dust
            }

        weathers = []
        weather = {}
        weather["model"] = "articles.weather_api"
        weather["fields"] = {}
        for key, value in temp_dict.items():
            if key in ['location', 'weather_summary', 'now_temp', 'dust', 'little_dust']:
                weather["fields"][key] = value
        weathers.append(weather)

        ######################################
        # client_id = 'B8wV6Y7kOQbv16yNZ8po' 
        # client_secret = 'UDvZzy0onJ'
        # headers = {'X-Naver-Client-Id':client_id, 'X-Naver-Client-Secret':client_secret}


        # url_base="https://openapi.naver.com/v1/search/local.json?query="
        # # keyword = quote(input("지역 및 먹고 싶은 음식을 입력해주세요! : "))
        # if weathers[0]['fields']['weather_summary'] == '흐림':
        #     keyword = '국밥'
        # elif weathers[0]['fields']['weather_summary'] == '구름많음':
        #     keyword = '전골'    
        # print(keyword)

        # url_middle="$&start="
        # keyword_number='1'
        # url_middle2 = "$&display="
        # restaurant_display = '5'

        # url = url_base + keyword + url_middle + keyword_number + url_middle2 + restaurant_display

        # result = requests.get(url,headers = headers).json()  

        # for lst in result['items']:
        #     lst['models'] = "restaurants.naver"

        # print(result['items'])
        # data = result['items']

        with open('weathers.json', 'w', encoding="utf-8") as make_file:
            json.dump(weathers, make_file, ensure_ascii=False, indent="\t") 
        return Response(weathers)

    else:
        context = {
            'location': weathers[0]['fields']['location'],
            'weather_summary': weathers[0]['fields']['weather_summary'],
            'now_temp': weathers[0]['fields']['now_temp'],
            'dust': weathers[0]['fields']['dust'],
            'little_dust': weathers[0]['fields']['little_dust'],
        }
        return Response(context)    
