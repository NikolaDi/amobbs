# coding=utf-8

import requests
import os
import re

base_path = os.getcwd()
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
           'Referer': 'http://www.amobbs.com/forum-9892-1.html',
           'Accept': 'image/webp,image/*,*/*;q=0.8',
           'Connection': 'keep-alive'}


class Spider:
    def __init__(self):
        self.session = requests.session()
        self.login()

    def login(self):
        response = self.session.get('http://www.amobbs.com/member.php?mod=logging&action=login&mobile=2',
                                    headers=headers)
        self.session.close()
        # print response.text
        content = response.text
        # print '登录url'+response.url.decode('gbk').encode('utf-8')
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
        # print '图片url:'+img_url
        # img_url = r'http://www.amobbs.com/index.php'
        # misc.php?mod=seccode&update=22727&idhash=SLcS6&mobile=2
        response = self.session.get(img_url, headers=headers)
        self.session.close()
        content = response.content
        with open(base_path+'/verify.jpg', 'wb') as f:
            f.write(content)
        username = raw_input("1/5 输入你的amobbs账户名:")
        password = raw_input("2/5 输入你的amobbs账户密码:")
        question = raw_input("3/5 输入安全提问编号:\n\t0-安全提问(未设置请忽略)\n\t1-母亲的名字\n\t2-爷爷的名字\n\t"
                             "3-父亲出生的城市\n\t4-您其中一位老师的名字\n\t5-您个人计算机的型号\n\t6-您最喜欢的餐馆名称\n\t"
                             "7-驾驶执照最后四位数\n\t请输入编号:")
        if question == '0':
            answer = None
        else:
            answer = raw_input("4/5 安全提问答案:")
        seccodeverify = raw_input("5/5 请输入程序运行目录下 verify.jpg 图片中的验证码:")
        # formhash:7a156042
        # referer:http://www.amobbs.com/forum.php?mod=guide&view=hot&mobile=2
        # fastloginfield:username
        # cookietime:2592000
        # username:
        # password:
        # questionid:5
        # answer:dell
        # seccodehash:SK14G //图片idhash
        # seccodeverify:crc9
        data = {
            'fromhash': formhash,
            'referer': 'http://www.amobbs.com/forum.php?mod=guide&view=hot&mobile=2',
            'fastloginfield': 'username',
            'cookietime': '2592000',
            'username': username,
            'password': password,
            'questionid': question,
            'answer': answer,
            'seccodehash': idhash,
            'seccodeverify': seccodeverify,
        }
        # http://www.amobbs.com/member.php?mod=logging&action=login&
        # loginsubmit=yes&loginhash=LuJaj&mobile=2&handlekey=loginform&inajax=1
        login_url = 'http://www.amobbs.com/member.php?mod=logging&action=login&' \
                    'loginsubmit=yes&loginhash={}&mobile=2&handlekey=loginform&inajax=1'.format(loginhash)
        # print login_url

        response = self.session.post(login_url, data, headers=headers)
        self.session.close()
        content = response.content
        if 'succeedhandle_loginform' in content:
            print '登录成功'
        else:
            print '登录失败'
            exit()

    def get(self, url):
        return self.session.get(url, headers=headers)

if __name__ == '__main__':
    spider = Spider()
