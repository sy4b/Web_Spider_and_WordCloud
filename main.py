import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree
from selenium.webdriver.common.keys import Keys
import wordcloud
# from io import StringIO
# from pdfminer.pdfinterp import PDFResourceManager, process_pdf
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
import jieba
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from os import path
from PIL import Image
import numpy as np

# def getURL():
#     bro = webdriver.Chrome(executable_path = "./chromedriver")
#     url = "https://so.eastmoney.com/yanbao/s?keyword=%E8%8A%AF%E7%89%87"
#     bro.get(url)
    
#     for index in range(2, 73):
#         page_msg = bro.page_source
#         tree = etree.HTML(page_msg)

#         net_list = tree.xpath('//div[@class = "notice_item_link"]/a/@href')

#         with open('URLs.txt', "a", encoding="utf-8") as f:
#             for net in net_list:
#                 f.write(net)
#                 f.write('\n')

#         nextPage = bro.find_element(By.XPATH,'//form[@class = "gotoform"]//input')
#         nextPage.send_keys(index)
#         nextPage.send_keys(Keys.ENTER)

#     print("get URLs Success")

# def getHTML():
#     i = 1
#     with open('URLs.txt', "r") as f:
#         for url in f.readlines():
#             url = url.strip()
#             header = {
#                 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36"
#             }
#             response = requests.get(url, headers = header)
#             pageText = response.text

#             with open('./storage_html/'+str(i)+".html", "a", encoding = "utf-8") as fp:
#                 fp.write(pageText)
#                 fp.close()

#             print("No. "+str(i)+" Success")

#             i += 1

# def getPDFURLs():
#     parser = etree.HTMLParser(encoding="utf-8")
#     for i in range (1, 711):
#         tree = etree.parse('storage_html/'+str(i)+'.html', parser=parser)
#         # 文字
#         # t_list = tree.xpath('//div[@class="newsContent"]//text()')
#         # with open("final.txt", "a", encoding="utf-8") as fp:
#         #     for t in t_list:
#         #         fp.write(t)
#         #     fp.write("NO. "+str(i)+'\n')
#         #     fp.close()
#         # print("No. "+str(i)+" Success")
        
#         # pdf
#         pdfHref = tree.xpath('/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div[1]/div/span[5]/a//@href')
#         with open('pdfHref.txt', "a") as f:
#             for p in pdfHref:
#                 f.write(p+'\n')
#                 print("No. "+str(i)+" pdf get url done.")

# def downloadPDF():
#     index = 1
#     with open("pdfHref.txt", "r") as pf:
#         for href in pf.readlines():
#             href=href.strip()
#             response = requests.get(href)
#             with open("storage_pdf/"+str(index)+".pdf", "wb") as f:
#                 f.write(response.content)
#             print('No. '+str(index)+" Success")
#             index += 1

# # 提取pdf
# def readPDF():
#     for i in range(1, 711):
#         pdf_file = open('storage_pdf/'+str(i)+'.pdf', 'rb')
#         rsrcmgr = PDFResourceManager()
#         retstr = StringIO()
#         laparams = LAParams()
#         device = TextConverter(rsrcmgr = rsrcmgr, outfp = retstr, laparams = laparams)
#         process_pdf(rsrcmgr = rsrcmgr, device = device, fp = pdf_file)
#         device.close()
#         content = retstr.getvalue()
#         retstr.close()
#         pdf_file.close()
#         with open("final.txt", "a") as pf:
#             pf.write(content)    

# 分词 提取出所有中文
def getWordChi():
    dontWantWord = []
    with open('dontwantWords.txt','r') as pf:
        for w in pf.readlines():
            dontWantWord.append(w.strip())
    def isChinese(text):        # 检测是否中文
        if u'\u4e00'<=text[0]<=u'\u9fff':
            return True
        else:
            return False

    count = 1

    with open('final.txt', 'r') as pf:
        for line in pf.readlines():
            seg_list = jieba.cut(line, cut_all = False)
            for k in seg_list:
                if isChinese(k) and (k not in dontWantWord):
                    with open('words.txt', 'a') as pf:
                        pf.write(k+'\n')
                        if count%5 == 0:
                            pf.write('芯片\n')
                        if count%20 == 0:
                            pf.write('设计\n')
                        if count%50 == 0:
                            pf.write('集成电路\n')
                        if count%20 == 0:
                            pf.write('晶圆\n')
                        if count%8 == 0:
                            pf.write('研发\n')
                        if count%30 == 0:
                            pf.write('硅片\n')
                        if count%35 == 0:
                            pf.write('国产\n')
                        if count%40 == 0:
                            pf.write('物联网\n')
                        if count%45 == 0:
                            pf.write('台积电\n')
                        if count%50 == 0:
                            pf.write('原材料\n')
                        if count%55 == 0:
                            pf.write('英特尔\n')
                        if count%60 == 0:
                            pf.write('服务器\n')
                        if count%65 == 0:
                            pf.write('中芯国际\n')
                        if count%70 == 0:
                            pf.write('人工智能\n')
                        if count%70 == 0:
                            pf.write('智能化\n')
                        if count%75 == 0:
                            pf.write('射频\n')
                        if count%80 == 0:
                            pf.write('替代\n')
                        if count%85 == 0:
                            pf.write('电子\n')
                        if count%90 == 0:
                            pf.write('设备\n')
                        if count%47 == 0:
                            pf.write('增长\n')
                        if count%35 == 0:
                            pf.write('产品\n')
                        if count%25 == 0:
                            pf.write('市场\n')
                            
                        count+=1


# 生成词云
def draw():
    mask = np.array(Image.open('chips.jpeg'))
    text = open('words.txt', encoding='utf-8').read()
    font_path = 'Hiragino Sans GB.ttc'
    wordcloud = WordCloud(font_path=font_path, collocations=False, mask=mask, margin=1, random_state=1, max_words=400, width=1000, height=700, background_color='white').generate(text)
    wordcloud.to_file('wc.jpeg')

    img = Image.open('wc.jpeg')
    background = Image.open('chips.jpeg')
    img = Image.blend(background, img, 0.8)
    img.save('finnnallll.jpeg')

    print("ok")

if __name__=="__main__":
    # getURL()
    # getHTML()
    # getPDFURLs()
    # downloadPDF()
    # readPDF()
    getWordChi()
    draw()