# -*- coding: utf-8 -*- 

from urllib2 import urlopen
from bs4 import BeautifulSoup
from time import sleep
import requests
import string
import datetime
import re

URL = 'http://news.naver.com/main/hotissue/dailyList.nhn?'

CATEGORY = { '100' : '정치',
             '101' : '경제',
             '102' : '사회',
             '103' : '생활/문화',
             '104' : '세계',
             '105' : 'it/과학' }

OID = 999
MAX_AID = 100000
S_YEAR = 2006
S_MONTH = 1
S_DAY = 1
ENDATE = { 'year':2017,
            'month':12,
            'day':28
           }

def clawler_loop():
    
    for _year in range(S_YEAR, ENDATE['year']):
        for _month in range(S_MONTH, ENDATE['month']):
            print(str(_year) + str(_month).zfill(2) + " START")
            for _day in range(S_DAY, ENDATE['day']):
                for _list in CATEGORY:
                    index_date = URL + 'sid1='+  _list +'&date='+ str(_year) + str(_month).zfill(2) + str(_day).zfill(2)
                    date_time = str(_year) + str(_month).zfill(2)
                    naver_sid_write(index_date, 'crawler.txt','a')
            sleep(0.01)


def naver_sid_write(_url, _file_name, _option):
    _response = requests.get(_url)
    _plain_text = _response.text
    
    _soup = BeautifulSoup(_plain_text, 'lxml')

    _lists = _soup.find('div', class_='list_body ranking_body')
    replace_str = str(_lists).replace('</a>', '\n')
    _split_list = replace_str.split('\n')

    _file = open(_file_name, _option)

    for _list in _split_list:
        if _list.find('href') != -1:
            _start = _list.find('sid1=')
            _category =_list[_start+5:_start+8]
            f_write_str = CATEGORY[_category] + " " + _list[114:] +  "\n"
            _file.write(f_write_str) 

    _file.close()
        

def main():
    clawler_loop()
    
   



if __name__ == "__main__":
    main()