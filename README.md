# Webspider_exp3
用Ajax爬取今日头条图片集
### Ajax原理
&ensp; 在用requests抓取页面时，得到的结果可能和浏览器中看到的不一样：在浏览器中可以正常显示的页面数据，但用requests得到的结果并没有。这是因为requests获取的都是原始 HTML文档，而浏览器中页面
则是经过Ajax处理数据后生成的。这些数据可能在HTML文档中，也可能是经过JavaScript和特定算法后生成的。
&ensp; 刚开始HTML文档中不包含某些数据，当原始页面加载完后，会向服务器发送Ajax请求获取数据，这些数据被JavaScript处理形成一些新页面。

&ensp; **Ajax: 即异步的JavaScript和XML，是利用JavaScript在保证页面不刷新、链接不改变的情况下与服务器交换数据的并更新
部分网页的技术。**


### 示例：用Ajax爬取今日头条图片

最近想买工装裤穿，可又不知道怎么搭配，所以就用爬虫爬下头条上`工装裤`的穿搭图片啦
##### (1)   获取网页页面的JSON文档
```Python
import os
import requests
from urllib.parse import urlencode           #来构造url参数的
from hashlib import md5                      #用来解析图片二进制的

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
        #用urlencode构造url中参数
    try:
        response=requests.get(url)
        if response.status_code==200:                #当请求成功时(status_code=200时)才继续下面代码
            return response.json()                   #用json方法将结果转化成JSON格式
    except requests.ConnectionError:
        return None

```
注意：
1）构造Ajax请求时，先探索清楚当前页面中Ajax请求链接的结构和规律。这里是Offest改变，其他参数不变。
2）使用urlencode方法构造请求的GET参数
3）发现只有offest发生改变，第一页0，第二页20，第三页40，依次增加20
##### (2)构造包含图片链接和标题的字典

```python
#提取图片url和标题
def parse_page(json):
    if json.get('data'):
        for item in json.get('data'):      #找到所需数据所处位置
            if item.get('title')==None:    #运行后发现不是每个item里都有图片链接和title，没有的直接跳过
                continue
            title=item.get('title')        #找到标题
            print(title)
            images=item.get('image_list')
            print(images)
            for image in images:
                yield{
                    'image':image.get('url'), #找到这个标题下的所以图片url 形成字典生成器
                    'title':title
                }

```
注意：
1）yield{}方法构造字典生成器非常简单，快速。
2）用json.get()方法在json文档中找取参数值非常快。

##### (3)把数据保存到本地
```Python
#实现保存图片的方法
def save_image(item):
    if not os.path.exists(item.get('title')):      #创建以标题为名称的文件夹
        os.mkdir(item.get('title'))
    try:
        response=requests.get(item.get('image'))  #访问图片的url
        if response.status_code==200:
            file_path='{0}/{1}.{2}'.format(item.get('title'),md5(response.content).hexdigest(),'jpg')
            if not os.path.exists(file_path):     #名称file_path使用其内容的md5值，可以去除重复
                with open(file_path,'wb') as f:  #访问成功后，将其二进制代码存入file_path.jpg中
                    f.write(response.content)
            else:
                print('Already Download',file_path)
    except requests.ConnectionError:
        print('Failed to save image')

```
注意：
1）这里的item就是(2)中得到的包含url和标题的字典
1）是以二进制写的方式存入文件，'wb'

##### (4)构造offest 进行遍历

```Python
def main(offest):
    json=get_page(offest)
    for item in parse_page(json):
        print(item)
        save_image(item)

if __name__=='__main__':
    for i in range(0,4):
        offest=i*20
        main(offest)

```

##### PS：代码叙述有不完整的地方，欢迎大家私信我。完整代码链接https://github.com/xubin97
