#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random
import requests
from userinfo import UserInfo


class LoginScript:
    URL = 'https://www.instagram.com/'
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    url_logout = 'https://www.instagram.com/accounts/logout/'
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
    accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'

    login_status = False
    csrftoken = ""
    user_id = 0

    def __init__(self,
                 username,
                 password,
                 proxy=""):

        self.user_login = username.lower()
        self.user_password = password
        self.s = requests.Session()
        if proxy != "":
            proxies = {
                'http': 'http://' + proxy,
                'https': 'http://' + proxy,
            }
            self.s.proxies.update(proxies)

    def login(self):
        log_string = 'Trying to login as %s...\n' % self.user_login
        self.write_log(log_string)
        self.s.cookies.update({
            'sessionid': '',
            'mid': '',
            'ig_pr': '1',
            'ig_vw': '1920',
            'csrftoken': '',
            's_network': '',
            'ds_user_id': ''
        })
        login_post = {
            'username': self.user_login,
            'password': self.user_password
        }
        self.s.headers.update({
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': self.accept_language,
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'User-Agent': self.user_agent,
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest'
        })
        r = self.s.get(self.URL)
        self.s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        time.sleep(5 * random.random())
        login = self.s.post(self.url_login, data=login_post, allow_redirects=True)
        self.s.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self.csrftoken = login.cookies['csrftoken']
        time.sleep(5 * random.random())

        if login.status_code == 200:
            r = self.s.get('https://www.instagram.com/')
            finder = r.text.find(self.user_login)
            if finder != -1:
                ui = UserInfo()
                self.user_id = ui.get_user_id_by_login(self.user_login)
                self.login_status = True
                log_string = '%s login success!' % self.user_login
                self.write_log(log_string)
                return True
            else:
                self.login_status = False
                self.write_log('Login error! Check your login data!')
                return False
        else:
            self.write_log('Login error! Connection error!')
            return False

    def write_log(self, log_text):
        """ Write log by print() or logger """

        try:
            print(log_text)
        except UnicodeEncodeError:
            print("Your text has unicode problem!")
