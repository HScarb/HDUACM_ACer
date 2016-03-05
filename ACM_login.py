# ACM_login.py
import requests

class ACM_login(object):
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
        print(r.text)
        print(r.cookies)


if __name__ == '__main__':
    c = ACM_login()
    c.login('RunnerUp', '621374as')