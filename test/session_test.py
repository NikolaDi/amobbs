# coding=utf-8

import requests
import time

headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
           'Referer': 'http://www.amobbs.com/forum-9892-1.html'}

session = requests.session()

session.get('http://www.baidu.com', headers=headers)
#session.close()
session.get('http://www.baidu.com', headers=headers)
#session.close()
