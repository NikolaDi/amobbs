# coding=utf-8

import requests
import re
import os
import pickle
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

base_path = os.getcwd()
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
           'Referer': 'http://www.amobbs.com/forum-9892-1.html',
           'Accept': 'image/webp,image/*,*/*;q=0.8',
           'Connection': 'keep-alive'}

session = requests.session()
# session = requests

# <div>
# <a href="forum.php?mobile=2">首页</a> | <a href="member.php?mod=logging&amp;action=login&amp;mobile=2" title="登录">登录</a> | <a href="javascript:;" style="color:#D7D7D7;" title="注册">注册</a>
# </div>

# <div>
# <a href="home.php?mod=space&amp;uid=183508&amp;do=profile&amp;mycenter=1&amp;mobile=2">meirenai</a> , <a href="member.php?mod=logging&amp;action=logout&amp;formhash=9eb4632c&amp;mobile=2" title="退出" class="dialog">退出</a>
# </div>

if os.path.exists(base_path+'/cookies.txt'):
    with open(base_path+'/cookies.txt', 'r') as f:
        session.cookies = pickle.load(f)
        # session.cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
response = session.get('http://www.amobbs.com/', headers=headers)
session.close()
content = response.content
re_login = re.findall(r'class="dialog">(.*?)</a>', content)
if re_login and '退出' == re_login[0]:
    print '登录成功'
else:
    response = session.get('http://www.amobbs.com/member.php?mod=logging&action=login&mobile=2', headers=headers)
    session.close()
    # print response.text
    content = response.text
    # <form id="loginform" method="post" action="member.php?mod=logging&amp;action=login&amp;
    # loginsubmit=yes&amp;loginhash=LFhwW&amp;mobile=2" onsubmit="pwmd5('password3_LFhwW');">
    re_loginhash = re.findall(r'loginhash=(.*?)&', content)
    # print re_loginhash
    # <input type="hidden" name="formhash" id="formhash" value="4e69f3e9">
    re_formhash = re.findall(r'id="formhash" value=\'(.*?)\'', content)
    # print re_formhash
    # <img src="misc.php?mod=seccode&amp;update=03287&amp;idhash=SG0Ej&amp;mobile=2" class="seccodeimg"/>
    re_update = re.findall(r';update=(.*?)&', content)
    # print re_img
    re_idhash = re.findall(r';idhash=(.*?)&', content)
    # print re_idhash
    update = re_update[0]
    formhash = re_formhash[0]
    loginhash = re_loginhash[0]
    idhash = re_idhash[0]
    img_url = r'http://www.amobbs.com/misc.php?mod=seccode&update={}&idhash={}&mobile=2'.format(update, idhash)
    print img_url
    # img_url = r'http://www.amobbs.com/index.php'
    # misc.php?mod=seccode&update=22727&idhash=SLcS6&mobile=2
    response = session.get(img_url, headers=headers)
    session.close()
    content = response.content
    with open(base_path+'/verify.jpg', 'wb') as f:
        f.write(content)

    seccodeverify = raw_input("请输入验证码:")
    # formhash:7a156042
    # referer:http://www.amobbs.com/forum.php?mod=guide&view=hot&mobile=2
    # fastloginfield:username
    # cookietime:2592000
    # username:meirenai
    # password:Luffy532.
    # questionid:5
    # answer:dell
    # seccodehash:SK14G //图片idhash
    # seccodeverify:crc9
    data = {
        'fromhash': formhash,
        'referer': 'http://www.amobbs.com/forum.php?mod=guide&view=hot&mobile=2',
        'fastloginfield': 'username',
        'cookietime': '2592000',
        'username': 'meirenai',
        'password': 'Luffy532.',
        'questionid': '5',
        'answer': 'dell',
        'seccodehash': idhash,
        'seccodeverify': seccodeverify,
    }
    # http://www.amobbs.com/member.php?mod=logging&action=login&
    # loginsubmit=yes&loginhash=LuJaj&mobile=2&handlekey=loginform&inajax=1
    login_url = 'http://www.amobbs.com/member.php?mod=logging&action=login&' \
                'loginsubmit=yes&loginhash={}&mobile=2&handlekey=loginform&inajax=1'.format(loginhash)
    # print login_url

    response = session.post(login_url, data, headers=headers)
    session.close()
    # print response.content
    content = response.content
    if 'succeedhandle_loginform' in content:
        print '登录成功'
        with open(base_path+'/cookies.txt', 'w') as f:
            pickle.dump(session.cookies, f)
            # pickle.dump(requests.utils.dict_from_cookiejar(session.cookies), f)
    else:
        print '登录失败'
        exit()
response = session.get('http://www.amobbs.com/forum.php?mod=guide&view=hot&mobile=2', headers=headers)
session.close()
content = response.content
# <a href="home.php?mod=space&amp;uid=183508&amp;do=profile&amp;mycenter=1&amp;mobile=2">meirenai</a>
re_username = re.findall(r'<a href="home\.php.*?mobile=2">(.*?)</a>', content)
login_username = re_username[0]
print login_username
# http://www.amobbs.com/home.php?mod=space&uid=261204&from=space&type=thread&do=thread&view=me&mobile=2
response = session.get('http://www.amobbs.com/forum.php?mod=viewthread&tid=5631417&extra=&page=1&mobile=2', headers=headers)
text = response.text
# print text
re_title = re.findall(r'<h2>([\w\W]*?)<a href=', text)
title = re_title[0].strip()
print title
re_name = re.findall(r'<a href="home\.php\?mod=space&amp;uid=(.*?)&amp;mobile=2" class="blue">(.*?)</a>', text)
print re_name
re_time = re.findall(r'<li class="grey rela">[\w\W]*?([0-9|\-| |:]*?)</li>', text)
print re_time
re_message = re.findall(r'<div class="message">([\w\W]*?)</div>', text)
len(re_message)
for i in re_message:
    for c in i:
        pass
with open(base_path+'/message.txt', 'w') as f:
    for i in re_message:
        f.write(i.strip().replace('&nbsp;', ' ').replace('<br />', '\n'))
        f.write('\n---------------------------------------\n')
print len(re_message)
soup = BeautifulSoup(text, 'html.parser')
test = soup.prettify()
# print test
soup = BeautifulSoup(test, 'html.parser')
test = soup.find_all('div', class_='message')
with open(base_path+'/soup.txt', 'w') as f:
    f.write(title+'\n'+'http://www.baidu.com\n')
    cnt = 0
    for i in test:
        f.write(re_name[cnt][1]+'   '+re_name[cnt][0]+'   '+re_time[cnt]+'\n')
        cnt += 1
        demo = i.text.strip()
        s = re.sub(r'\n+', '\n', demo)
        f.write(s)
        f.write('\n-----------------------------------------------------\n')

# 帖子内的图片链接
# <img id="aimg_239855"
# src="forum.php?mod=image&amp;aid=239855&amp;size=140x140&amp;key=3285b4ed131bf5e8&amp;type=fixnone"
# alt="QQ图片20141127161216.jpg" title="QQ图片20141127161216.jpg"
# zsrc="forum.php?mod=image&amp;aid=239855&amp;size=140x140&amp;key=3285b4ed131bf5e8&amp;type=fixnone"
# style="display: inline; visibility: visible;">

# moji图片
# <img src="static/image/smiley/default/lol.gif" smilieid="12" border="0" alt="">
# <img src="static/image/smiley/grapeman/01.gif" smilieid="41" border="0" alt=""
# zsrc="static/image/smiley/grapeman/01.gif" style="display: inline; visibility: visible;">

# 帖子内的下载链接
# <a
# href="forum.php?mod=attachment&amp;aid=MjM5ODU5fGM2N2YzZDUwfDE0NTY5MTk4MjZ8MTgzNTA4fDU2MDYwODk%3D&amp;mobile=2"
# id="aid239859" target="_blank">BmosV1.1.zip</a>





# <a
# href="forum.php?mod=attachment&amp;aid=Mjg2NTY1fDg5ZjY2N2NhfDE0NTY5MjIzNzV8MTgzNTA4fDU2MzE0MTc%3D&amp;mobile=2"

# 255808|ccace87f|1456923348|183508|5610807
# 249218|f31da17e|1456923348|183508|5610807
