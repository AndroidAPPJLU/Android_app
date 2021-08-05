import requests
import re

"""
该爬虫目前已爬取内容为文章标题和文章中英文内容
如有需求还可补充文章属性标签，如：风景，美食等等

"""

url = 'https://www.adreep.cn'
url_xx = 'https://www.adreep.cn/xx/'            #小学作文网址     下列代码爬取目标为小学，可写一个循环来爬取其他两个
url_cz = 'https://www.adreep.cn/cz/'            #初中作文网址
url_gz = 'https://www.adreep.cn/gz/'            #高中作文网址
url_m = 'index.html.more.{}.html'   # 更多内容（该网页为动态网页，需要点击更多内容来刷新页面，该后缀为该网址更新的页面后缀）
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
}       #模仿浏览器的headers


pattern_list = u'<div class="article-list">.+<!-- 列表 -->'      #用于匹配整个列表
# pattern_link1 = r'<div class="media-left">(.+?)>'               #link1、link2用于匹配出网址，暂时抛弃，原因：该正则表达式无法完全匹配出网址
pattern_link11 = r'<h3 class="article-title">(.+?)>'            #link1的另一种情况
pattern_link2 = r'"/.+?html"'
pattern_text1 = r'article-text">(.+?)</div>'                     #用于匹配出text div块
pattern_title1 = u'<h1 class="metas-title">(.+)</h1>'                             #匹配文章标题  ,匹配中文需要u
pattern_text2 = r'>(.+?)</div>'                                 #精细化匹配到的内容，去掉部分无关数据
pattern_text3 = r'<p>.+</p>'                                    #去除<p>标签中的内容


rePattern_list = re.compile(pattern_list)
# rePattern_link1 = re.compile(pattern_link1)             #暂时抛弃，原因：该正则表达式无法完全匹配出网址
rePattern_link11 = re.compile(pattern_link11)
rePattern_link2 = re.compile(pattern_link2)
rePattern_text1 = re.compile(pattern_text1)
rePattern_text2 = re.compile(pattern_text2)
rePattern_text3 = re.compile(pattern_text3)
rePattern_title1 = re.compile(pattern_title1)

def get_article(href_list):        #获取文章的函数
    for h in href_list:
        h = rePattern_link2.search(h)[0]
        h = h.replace('"', '')
        h = url + h

        response = requests.get(h, headers=headers, verify=False)
        cont = response.content.decode()
        cont = cont.replace('\n', '')
        title = rePattern_title1.search(cont)  # 获取文章标题
        title = title.group()
        title = title.replace('<h1 class="metas-title">', '')  # 去掉多余标签
        title = title.replace('</h1>', '')  # 去掉多余标签
        title = title.replace('&mdash;', '—')  # &mdash; 在HTML中表示破折号—

        text = rePattern_text1.search(cont)[0]  # 匹配出article-text块
        text = text.replace('article-text">', '')  # 去掉article-text，以便匹配<img......> 中的 >
        if rePattern_text2.findall(text)!=[]:
            text = rePattern_text2.search(text)[0]  # 匹配出第一个 > 到</div?之间的内容，去除了<img.......

        text = text.replace('</div>', '')  # 去除多余的</div>
        text = text.replace('<div>', '')  # 去除多余的<div>
        text = text.replace('<br />', ' ')  # 去除多余的<br />
        text = text.replace('<br data-filtered="filtered">', '') #去掉多余的<br data-filtered="filtered">
        text = text.strip('>')  # 去除字符串首尾的 >
        text = text.strip(' ')
        pp = rePattern_text3.search(text)
        if pp != None:
            text = text.replace(pp[0], '')  #去掉<p>标签及其内容
        print(h)
    """可得到信息：文章标题 title 和文章内容 text"""




response = requests.get(url_gz, headers=headers, verify=False)

str = response.content.decode()   #解码获取的信息

str1 = str.replace('\n', '')        #去掉换行符

item = rePattern_list.search(str1)[0]              #含有所有列表信息的整块div区域内容

href_list = rePattern_link11.findall(item)           #存储匹配出的含有作文网址的短句

get_article(href_list)

for i in range(1, 31):
    url_more = url_xx+url_m.format(i)

    response = requests.get(url_more, headers=headers, verify=False)
    str = response.content.decode()  # 解码获取的信息
    str1 = str.replace('\n', '')  # 去掉换行符
    print(i)


    href_list11 = []
    href_list11 = rePattern_link11.findall(str1)
    if href_list11 != []:
       get_article(href_list11)
