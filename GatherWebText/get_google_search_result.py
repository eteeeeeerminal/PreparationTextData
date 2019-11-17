# -*- coding: utf-8 -*-

# まずは取得するためのURLをいっぱい取る。
# Google検索で上位のサイトのURLを取得する。

import codecs
import json
import collections as cl
import datetime

from time import sleep
from Deropy.google import Google

if __name__=='__main__':

    print('start_getting_URLs')
    print(datetime.datetime.now())

    query_json = json.load(codecs.open("query.json", 'r', 'utf-8', 'ignore'))

    for query in query_json['second_classes']:

        search_result = cl.OrderedDict()

        # search_textでmain_classがあるやつとないやつ両方やりたい
        def search (search_text):
            google = Google()
            search_result[search_text] = google.Search(search_text, type='text', maximum=query_json['second_cl_page_num'])
            suggests = google.Suggest(search_text, jap=True, alph=True, num=True)
            sleep(300)

            n = 0
            for key in suggests.keys():
                for suggest in suggests[key]:
                    google = Google()
                    if suggest == search_text:
                        continue
                    search_result[suggest] = google.Search(suggest, type='text', maximum=query_json['third_cl_page_num'])
                    n += 1
                    print(n, len(search_result[suggest]))
                    if n == query_json['third_class_num']:
                        break
                    sleep(300)

                else:
                    continue

                break

        search(query_json['main_class'] + ' ' + query)
        search(query)

        fw = open(query + '.json', 'w')
        json.dump(search_result, fw, indent=4)

    print('complete_getting_URLs')
    print(datetime.datetime.now())
