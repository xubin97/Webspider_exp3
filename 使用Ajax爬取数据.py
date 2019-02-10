# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 15:32:50 2019

@author: lenovo
"""
import os
import requests
from urllib.parse import urlencode
from hashlib import md5

#获取页面json
def get_page(offest):
    params={
            'aid':'24',
            'offest':offest,
            'format':'json',
            'keyword':'%E5%B7%A5%E8%A3%85%E8%A3%A4',
            'autoload':'true',
            'count':'20',
            'cur_tab':'1',
            'from':'search_tab',
            'pd':'synthesis'
            }
    url='https://www.toutiao.com/api/search/content/?aid=24&offset=0&format=json&keyword=%E5%B7%A5%E8%A3%85%E8%A3%A4&autoload=true&count=20&cur_tab=1&from=search_tab&pd=synthesis'+urlencode(params)
        #//用urlencode构造url中参数
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.json()                   #//用json方法将结果转化成JSON格式
    except requests.ConnectionError:
        return None

#提取图片url和标题
def parse_page(json):
    if json.get('data'):
        for item in json.get('data'):    
            if item.get('title')==None:
                continue
            title=item.get('title')
            print(title)
            images=item.get('image_list')
            print(images)
            for image in images:
                yield{
                    'image':image.get('url'),
                    'title':title
                }
                
#实现保存图片的方法
def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response=requests.get(item.get('image'))
        if response.status_code==200:
            file_path='{0}/{1}.{2}'.format(item.get('title'),md5(response.content).hexdigest(),'jpg')
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:
                    f.write(response.content)
            else:
                print('Already Download',file_path)
    except requests.ConnectionError:
        print('Failed to save image')
        
        
#最后构造一个offest数组，遍历
def main(offest):
    json=get_page(offest)
    for item in parse_page(json):
        print(item)
        save_image(item)

GROUP_start=1
GROUP_end=20

if __name__=='__main__':
    for i in range(0,4):
        offest=i*20
        main(offest)
#1.总结遇到错误
#    2.开头xzzzz