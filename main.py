import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree
from selenium.webdriver.common.keys import Keys
import wordcloud
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import jieba
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from os import path
from PIL import Image
import numpy as np

# 获取东方财富网所有研报的网址url
def getURL():
    bro = webdriver.Chrome(executable_path = "./chromedriver")              # Chrome浏览器驱动
    url = "https://so.eastmoney.com/yanbao/s?keyword=%E8%8A%AF%E7%89%87"    # 目标网址
    bro.get(url)                                                            # 发送get请求
    
    for index in range(2, 73):                                              # 逐页爬取
        page_msg = bro.page_source                                          # 页面html源码信息
        tree = etree.HTML(page_msg)                                         # 使用xPath解析

        net_list = tree.xpath('//div[@class = "notice_item_link"]/a/@href') # 解析出每篇研报的url 位于href属性中

        with open('URLs.txt', "a", encoding="utf-8") as f:                  # 记录在URLs.txt文件
            for net in net_list:
                f.write(net)
                f.write('\n')                                               # 换行

        nextPage = bro.find_element(By.XPATH,'//form[@class = "gotoform"]//input')  # 找到页面跳转框
        nextPage.send_keys(index)                                                   # 向跳转框写入页码
        nextPage.send_keys(Keys.ENTER)                                              # 模拟回车 页面跳转

    print("get URLs Success")

# 获取每篇研报的html信息
def getHTML():
    i = 1
    with open('URLs.txt', "r") as f:                # 打开存储URL的文本
        for url in f.readlines():                   # 逐行读取
            url = url.strip()                       # 清除末尾换行符\n
            header = {                              # UA伪装
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36"
            }
            response = requests.get(url, headers = header)  # 发送一个get请求，得到相应resopnse
            pageText = response.text                        # text/html解析

            with open('./storage_html/'+str(i)+".html", "a", encoding = "utf-8") as fp:     # 记录在html文件中，按序号命名
                fp.write(pageText)
                fp.close()

            print("No. "+str(i)+" Success")

            i += 1

# 获取pdf的URL
def getPDFURLs():
    parser = etree.HTMLParser(encoding="utf-8")         # 避免读取不标准的html文件报错（无语
    for i in range (1, 711):                            # 挨个读取
        tree = etree.parse('storage_html/'+str(i)+'.html', parser=parser)   # 本地文件xPath解析
        # 文字
        # t_list = tree.xpath('//div[@class="newsContent"]//text()')
        # with open("final.txt", "a", encoding="utf-8") as fp:
        #     for t in t_list:
        #         fp.write(t)
        #     fp.write("NO. "+str(i)+'\n')
        #     fp.close()
        # print("No. "+str(i)+" Success")
        
        # pdf
        pdfHref = tree.xpath('/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div[1]/div/span[5]/a//@href')   # 找到pdf url
        with open('pdfHref.txt', "a") as f:             # 记录在pdfHref.txt文件中
            for p in pdfHref:
                f.write(p+'\n')
                print("No. "+str(i)+" pdf get url done.")

# 下载pdf
def downloadPDF():
    index = 1
    with open("pdfHref.txt", "r") as pf:
        for href in pf.readlines():
            href=href.strip()
            response = requests.get(href)                               # get
            with open("storage_pdf/"+str(index)+".pdf", "wb") as f:
                f.write(response.content)
            print('No. '+str(index)+" Success")
            index += 1

# 识别pdf文字
def readPDF():
    for i in range(1, 711):
        pdf_file = open('storage_pdf/'+str(i)+'.pdf', 'rb')
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        laparams = LAParams()
        device = TextConverter(rsrcmgr = rsrcmgr, outfp = retstr, laparams = laparams)
        process_pdf(rsrcmgr = rsrcmgr, device = device, fp = pdf_file)
        device.close()
        content = retstr.getvalue()
        retstr.close()
        pdf_file.close()
        with open("final.txt", "a") as pf:
            pf.write(content)    

# 分词 提取出所有中文
def getWordChi():
    dontWantWord = []                                   
    with open('dontwantWords.txt','r') as pf:
        for w in pf.readlines():                
            dontWantWord.append(w.strip())              # 读入屏蔽词，可在dontwantWords.txt设置
    def isChinese(text):        # 检测是否中文
        if u'\u4e00'<=text[0]<=u'\u9fff':
            return True
        else:
            return False

    with open('final.txt', 'r') as pf:
        for line in pf.readlines():
            seg_list = jieba.cut(line, cut_all = False)
            for k in seg_list:
                if isChinese(k) and (k not in dontWantWord):
                    with open('words.txt', 'a') as pf:
                        pf.write(k+'\n')

# 生成词云
def draw():
    mask = np.array(Image.open('chips.jpeg'))                   # 云的轮廓
    text = open('words.txt', encoding='utf-8').read()           # 词语
    font_path = 'Hiragino Sans GB.ttc'                          # 字体
    wordcloud = WordCloud(font_path=font_path, collocations=False, mask=mask, margin=1, random_state=1, max_words=400, width=1000, height=700, background_color='white').generate(text)
    wordcloud.to_file('wc.jpeg')                                # 保存起来

    img = Image.open('wc.jpeg')
    background = Image.open('chips.jpeg')                       # 背景
    img = Image.blend(background, img, 0.8)                     # 重叠
    img.save('finnnallll.jpeg')

    print("ok")

if __name__=="__main__":
    getURL()
    getHTML()
    getPDFURLs()
    downloadPDF()
    readPDF()
    getWordChi()
    draw()