#! -*- coding: utf-8 -*-
# @Time    : 18-1-21
# @Author  : Wutao Lin
# @Environment : Python 3.5
# @function:

import pandas as pd
import zhihu_oauth
from zhihu_oauth.zhcls import SearchType
import codecs
import ujson as json
import crash_on_ipy

def get_author_name(excel_path):
    sheet = pd.read_excel(excel_path, sheetname='data')

    authors = set()
    for author in sheet['答主']:
        authors.add(author)

    print(authors)
    return authors


def get_author_info(author, client):
    info = dict()
    p = client.search(author, SearchType.PEOPLE)[0].obj
    info['follower_count'] = p.follower_count
    info['thanked_count'] = p.thanked_count
    info['voteup_count'] = p.voteup_count
    info['name'] = p.name
    info['business'] = p.business._json
    info['collected_count'] = p.collected_count
    info['description'] = p.description
    info['educations'] = p.educations._json
    info['employments'] = p.employments._json
    info['gender'] = p.gender
    info['locations'] = p.locations._json
    return info


def crawl_info():
    authors = get_author_name("zhihu_data.xlsx")

    client = zhihu_oauth.ZhihuClient()
    try:
        client.login("your account", "your password")
    except:
        # validation code needed
        with open('a.gif', 'wb') as f:
            f.write(client.get_captcha())
        captcha = input('please input captcha:')
        client.login("your account", "your password", captcha)

    result = dict()
    for author in authors:
        try:
            result[author] = get_author_info(author, client)
        except:
            result[author] = dict()
            print("Author %s error" % author)

    with codecs.open("zhihu.json", 'w', encoding='utf-8') as fout:
        json.dump(result, fout, ensure_ascii=False)


def main():
    crawl_info()


if __name__ == "__main__":
    main()