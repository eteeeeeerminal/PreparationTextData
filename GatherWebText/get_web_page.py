# -*- coding: utf-8 -*-
# get_google_search_result.py で保存した URL の html をダウンロードする

import os
import codecs
import json
import urllib.request
import datetime
from time import sleep
import selenium
from selenium import webdriver

import traceback

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


if __name__ == '__main__':

    print('start_getting_HTMLs')
    print(datetime.datetime.now())

    # "second_classes" に検索したい単語のリストがある。
    query_json = json.load(codecs.open("query.json", 'r', 'utf-8', 'ignore'))
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver  = webdriver.Chrome(options=options)

    def get_web(web_num, _url, _save_dir, timeout_counter = 0):
        try :
            driver.get(_url)
            html = driver.page_source

        except selenium.common.exceptions.UnexpectedAlertPresentException:
            alert = driver.switch_to_alert()
            alert.accept()

        except selenium.common.exceptions.TimeoutException:
            if timeout_counter > 5:
                print(_url)
                print('raise error & skip save')
                return "Timeout"
            else:
                sleep(5)
                get_web(web_num, _url, _save_dir, timeout_counter=timeout_counter+1)
                return "Timeout"

        except:
            traceback.print_exc()
            print(_url)
            print('raise error & skip save')
            return "Error"

        with open(_save_dir +'/'+ str(i) +'.html', mode='w', encoding='utf-8') as f:
            f.write('<!--' + _url + '-->\n')
            f.write(html)
            print('\t\t save : ' + _url)

    for query in query_json['second_classes']:
        print('save : ' + query)
        urls_json = json.load(codecs.open(query + ".json", 'r', 'utf-8', 'ignore'))
        os.makedirs(query, exist_ok=True)
        for sub_query in urls_json:
            print('\t save : ' + sub_query)
            save_dir = query + '/' + sub_query
            os.makedirs(save_dir, exist_ok=True)
            i = 0
            timeout_counter = 0
            for url in urls_json[sub_query]:
                sleep(1)
                get_web(i, url, save_dir)
                i += 1

                    
    print('complete_getting_HTMLs')
    print(datetime.datetime.now())