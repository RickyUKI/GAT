#!/usr/bin/python3
# -*- coding: utf-8 -*-

# JAVLibrary 番号搜索工具，根据 AV 番号搜索标题

import io
import re
import sys
import bs4
import requests


def search(keyword, pages):
    x = keyword
    y = pages
    url = 'http://www.javlib3.com/cn/vl_searchbyid.php'
    payload = {'keyword': x, 'page': y}
    response = requests.get(url, params=payload)
    link_response = requests.get(response.url)
    html = bs4.BeautifulSoup(link_response.text, "html.parser")

    return html  # 返回页面内容


def result(contents):

    global key_text

    contents_filter = contents.find('div', id='content').find('div', id='rightcolumn')

    if contents_filter.find(attrs={'class': 'page next'}) is not None:  # 判断是否存在下一页
        page_last = contents_filter.find(attrs={'class': 'page last'})
        page_num_top = int(str(page_last).find('page=')) + 5
        page_num_last = int(str(page_last).find('>>|')) - 14
        total_page = int(str(page_last)[page_num_top:page_num_last])  # 获取总页数

        pn = 1

        while pn < total_page - 1:  # 遍历所有页面内容
            new_contents = search(key_text, pn)  # 获取新页面内容
            pn += 1
            video = new_contents.find('div', id='content').find_all(attrs={'class': 'video'})

            for title in video:
                title_num = title.find(attrs={'class': 'id'}).text  # 番号
                title_text = title.find(attrs={'class': 'title'}).text  # 标题
                yield title_num + ' ' + title_text

    elif contents.title.text[:-13][-2:] == '结果':
        video = contents.find('div', id='content').find_all(attrs={'class': 'video'})

        for title in video:
            title_num = title.find(attrs={'class': 'id'}).text
            title_text = title.find(attrs={'class': 'title'}).text
            yield title_num + ' ' + title_text

    else:
        yield contents.title.text[:-13]


sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='UTF-8')  # 解决编码错误

page_num = 1

while True:
        key_regex = input('请输入想要搜索的番号：')
        if re.match('[0-9a-zA-Z\-]+', key_regex) is not None:
            key_text = key_regex
            break
        else:
            key_text = input('输入有误，请重新输入想要搜索的番号：')

source = search(key_text, page_num)

for target in result(source):
    print(target)
