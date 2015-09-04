#!/usr/bin/env python

import mechanize
import cookielib
import re
import time

def make_browser():
    """
    A function to make browser object.
    """
    brwser = mechanize.Browser()

    # Making Cookie Jar and bind it to browser
    cj = cookielib.LWPCookieJar()
    browser.set_cookiejar(cj)

    # Setting browser options
    browser.set_handle_equiv(True)
    browser.set_handle_redirect(True)
    browser.set_handle_referer(True)
    browser.set_handle_robots(False)
    browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),
                               max_time=1)

    browser.addheaders = [('User-agent',
                          ('Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:1.7.3)'
                           ' Gecko/20041001 Firefox/0.10.1'))]
    return browser


def time2minutes(s):
    """
    A function to obtain minutes of the day from given string.
    """
    hstr, rest = s.split(':')
    h = int(hstr)
    m = int(re.sub(r'am|pm', '', rest))
    if rest.endswith('pm'): h += 12;
    return h*60+m


if __name__ = '__main__':
    browser = make_browser()

    browser.open('https://www.tumblr.com/login')
    browser.select_form(nr=0)

    # Login
    browser.form['user[email]'] = 'ari.yu1221@gmail.com'
    browser.form['user[password]'] = 'masa11921857'
    browser.submit()

    # Go to queue
    browser.open('http://tumblr.com/queue')
    body = browser.response().read()

    # Getting a part containing time to be published
    ptpart = re.findall(r"""var publish_on_times = \[(.+?)];""",
                        body, re.M | re.S)
    ptpart = ''.join(ptpart)
    pubtimes = re.findall(r""".+?'(.+?)'.+?'(.+?)'""", ptpart, re.M | re.S)

    now = time2minutes(time.strftime('%H:%M', time.localtime(time.time())))

    for cnt, (wd, pt) in enumerate(pubtimes):
        pm = time2minutes(pt)
        if pm < now:
            try:
                browser.select_form(nr=2+cnt*2)
                browser.submit()
            except:
                pass

