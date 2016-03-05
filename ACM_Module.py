# ACM_Module.py
import re
import requests
from bs4 import BeautifulSoup

def print_list(list):
    for item in list:
        print(item)

class ACM_Module(object):
    def __init__(self):
        object.__init__(self)
        self.session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        }
        self.session.headers.update(headers)

    def login(self, username, password):
        url = 'http://acm.hdu.edu.cn/userloginex.php?action=login'
        r = self.session.get(url)
        cookie = r.cookies
        #print(cookie[0][1])

        data = {
            'username': username,
            'userpass': password,
            'login': 'Sign In',
        }
        headers = {
            'host': 'acm.hdu.edu.cn',
            'origin': 'http://acm.hdu.edu.cn',
            'referer': 'http://acm.hdu.edu.cn/'
            #'cookie': cookie
        }
        r = self.session.post(url, data=data, headers=headers)
        print(self.session.cookies.items())
        #print(r.text)
        #print(r.content)
        userstatus_url = 'http://acm.hdu.edu.cn/userstatus.php?user=' + username
        r = self.session.get(userstatus_url)
        #print(r.text)
        #print(r.cookies)

    def submit(self, problemID, code, language=0):
        """
        提交
        :param problemID: 题号
        :param language: 提交语言
        0 - G++
        1 - GCC
        2 - C++
        3 - C
        4 - Pascal
        5 - Java
        6 - C#
        :param code: 需要提交的代码
        """
        url = 'http://acm.hdu.edu.cn/submit.php?action=submit'
        data = {
            'check': '0',
            'problemid': str(problemID),
            'language': str(language),
            'usercode': code
        }
        headers = {
            'Connect-Type': 'application/x-www-form-urlencoded'
        }
        se = self.session
        print(se.cookies.items())
        #print(se.headers.items())
        r = self.session.post(url, data=data, headers=headers)
        print(r.cookies.items())
        #print(r.text)

    def getsolved(self, username):
        """
        获得一个用户已经解决的问题的所有题号
        :return: 返回一个含有解决问题题号的list
        :param username: 用户id
        """
        url = 'http://acm.hdu.edu.cn/userstatus.php?user=%s' % username
        solved = []
        r = self.session.get(url)

        f = open('temp.html', 'wb')
        f.write(r.text.encode('utf-8'))
        f.close()
        # 解析出含有所有已完成题目号的字符串solvedstr
        soup = BeautifulSoup(r.text, 'html.parser')
        result = soup.find('p', align='left')
        solvedstr = result.text.split(';')
        #print_list(solved1)
        # 从solvedstr中解析出一个list，含有所有完成题目号码
        for item in solvedstr:
            if item:
                item = re.search(r'\d{4}', item)
                #print(item.group(0))
                solved.append(item.group(0))
        print(solved)
        return solved

    def getdiscuss(self, problemID):
        """
        获取discuss中的题解
        :param problemID: 题目编号
        :return: 返回一个list，包含了discuss中的解析出来的所有题解
        """
        url = 'http://acm.hdu.edu.cn/discuss/problem/list.php?problemid=%s' % problemID
        solutions = []
        solutionurls = []

        r = self.session.get(url)

        f = open('temp.html', 'wb')
        f.write(r.text.encode('utf-8'))
        f.close()

        soup = BeautifulSoup(r.text, 'html.parser')
        res = []
        res = soup.find_all('a', href=re.compile('\./post/reply\.php\?postid=\d+&messageid=1&deep=0'))
        #print_list(res)
        for item in res:
            item = item['href']
            item = item[1:]     # 将点截掉
            #print(item)
            solutionurls.append('http://acm.hdu.edu.cn/discuss/problem%s' % item)  # 拼接url
        print_list(solutionurls)

        return solutions

if __name__ == '__main__':
    c = ACM_Module()
    c.login('RunnerUp', '621374as')
    code0 = r'''#include <stdio.h>
    main(){int A,B;while(scanf("%d%d",&A,&B)!=EOF){printf("%d\n",A+B);}}'''
    #c.submit(1000, code0, language=3)
    #c.getsolved('hanzichi')
    c.getdiscuss(1236)