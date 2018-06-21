# -*- coding: utf-8 -*-
"""
Sending HTTP Post/Get request

Authors:    Wutao Lin
Date:       18/5/16 下午5:23

Validated on Python 3.6
"""
import urllib.parse
import http.client
import requests
import ujson as json

def connect(ip, port, url, json_data, method="POST"):
    """ suitable for multiple request

    :param ip:
    :param port:
    :param url:
    :param json_data: ASCII only, utf-8 is forbidden
    :param method: POST/GET
    :return:
    """
    params = urllib.parse.urlencode(json_data)
    headers = {"Content-Type": "application/x-www-form-urlencoded",
        "Connection": "Keep-Alive"}
    conn = http.client.HTTPConnection(ip, port=port)        # ip can be url
    conn.request(method=method, url=url, body=params, headers=headers)
    response = conn.getresponse()
    if response.status == 302 or response.status == 200:
        res = response.read()
        print(res)
        print ("Success!")
    else:
        print ("Failed!")
    conn.close();


def one_time(url, json_data, method="GET"):
    """ one time request

    :param url: e.g. 'http://127.0.0.1:8080/api/v1/addrecord/1'
    :param json_data:
    :param method: GET/POST
    :return:
    """
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    if method == "GET":
        #solution 1
        response = requests.get(url, headers=headers)

        #solution 2 :   doesn't work yet
        #headers = {'User-Agent': user_agent, "Content-Type": "text/html"}
        #response = requests.get(url, json.dumps(json_data), headers=headers)
    else:
        #solution 1
        response = requests.post(url, json.dumps(json_data), headers=headers)

    print(response.text)



if __name__ == "__main__":
    connect("127.0.0.1", 8889, "/", {'who': 'me'}, 'GET')
    connect("127.0.0.1", 8889, "/", {'who': 'me'}, 'POST')
    one_time('http://127.0.0.1:8889/', {'who': 'me'}, 'POST')
    one_time('http://127.0.0.1:8889/?who=me', 'GET')

    one_time('http://127.0.0.1:8889/deal?website=baidu&city=beijing', 'GET')


