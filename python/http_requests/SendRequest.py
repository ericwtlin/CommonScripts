# -*- coding: utf-8 -*-
"""
Sending HTTP Post/Get request

Authors:    Wutao Lin
Date:       17/10/20 下午5:23

Validated on Python 2.7
"""
import httplib
import urllib
import urllib2
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
    params = urllib.urlencode(json_data)
    headers = {"Content-Type": "application/x-www-form-urlencoded",
        "Connection": "Keep-Alive"}
    conn = httplib.HTTPConnection(ip, port=port)
    conn.request(method=method, url=url, body=params, headers=headers)
    response = conn.getresponse()
    print(response + "\n")
    if response.status == 302 or response.status == 200:
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
    data = urllib.urlencode(json_data)
    if method == "GET":
        #solution 1
        response = urllib2.urlopen(url, data)

        #solution 2 :   doesn't work yet
        #headers = {'User-Agent': user_agent, "Content-Type": "text/html"}
        #response = requests.get(url, json.dumps(json_data), headers=headers)
    else:
        #solution 1
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)

        #solution 2 :   doesn't work yet
        #headers = {'User-Agent': user_agent, "Content-Type": "text/html"}
        #response = requests.post(url, json.dumps(json_data), headers=headers) #allow_redirects=True
    print (response.read() + "\n")
    print (response.info())  # get response header


if __name__ == "__main__":
    connect("localhost", 8080, "/api/v1/addrecord/1", {"sentence": "我是中国人"})
    one_time("http://127.0.0.1:8080/api/v1/addrecord/1", {"sentence": "我是中国人"})
