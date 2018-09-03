# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 22:53:22 2018

@author: BeepWalker
"""



from lxml import etree
from requests import get
import os

#用户输入区
pageNo = 1 #爬取的页面个数
thekeyWord = '债券'

#工作区，代码不要乱动
articleList = []

##记录目标文章的网址
initialURL = 'http://roll.finance.sina.com.cn/finance/zq2/zsscdt/index_{}.shtml'
for i in range(pageNo):
    data = get(initialURL.format(i+1)).text
    s = etree.HTML(data)
    singlePageArticleList = s.xpath('//*[@id="Main"]/div[3]/ul/li/a/@href')
    print('Page{} has {} records.'.format(i+1,len(singlePageArticleList)))
    articleList.extend(singlePageArticleList)
    
##存储各篇文章
cumulator = 0

targetFilePath = os.getcwd()+'\\articleSaving'
if not os.path.exists(targetFilePath): 
    os.mkdir(targetFilePath)
    os.chdir(targetFilePath)

for articleURL in articleList:
    data = get(articleURL).content.decode('utf-8','ignore')  #——解决http返回报文编码问题的范例  
    s = etree.HTML(data)
    kwList = s.xpath('//*[@id="article-bottom"]/div[1]/a/text()')
    if thekeyWord in kwList:
        title = s.xpath('//h1/text()')
        abstract = s.xpath('//*[@id="article_content"]/div[1]/div[2]/p/text()')
        textParts = s.xpath('//*[@id="artibody"]/p/text()')
        
        
        with open(str(title[0]) + '.txt','wt',encoding = 'utf-8') as f:
            f.writelines(title)
            f.writelines(['\n'])
            f.writelines(abstract)
            f.writelines(['\n'])
            f.writelines(textParts)
            f.writelines(['\n'])
            f.writelines(kwList)
        cumulator += 1
    print('运行中..........')
print('已经爬取了{}篇文章'.format(cumulator))

print('Happy Chinese Junior Year!!!')
        
            
            
