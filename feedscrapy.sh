#!/bin/bash
scrapy shell "http://jiaoyu.baidu.com/k12Bank/textbook/?stage=3&subject=4"
sel=response.css(".question-item")
sel0=sel[0]
sel0.xpath('div[1]/div/table/tbody/tr/td/div/text()').extract() #question
sel0.xpath('div[1]/div/table/tbody/tr/td/div/table/tr/td/text()').extract() #options
sel0.xpath('div[2]/span/text()').extract() #physics-singlechoice easy
sel0.xpath('div[1]/a/@href').extract() #answer link
alink = sel0.xpath('div[1]/a/@href').extract()[0]
fetch(alink)
answer_sel = response.css(".answer-content")
answers = answer_sel.xpath('div[1]/table[1]/tbody/tr/td/div/text()').extract()
dlink = answer_sel.xpath('div[2]/a/@href').extract()[0]
fetch(dlink)
danswer_sel = response.css('#q_indexkuai321')
danswers = danswer_sel.xpath('table[2]/tbody/tr/td/div/text()').extract()
outline_sel = response.css("#secinfoPanel")
outline_name = outline_sel.xpath('div[1]/div/span/text()').extract()[0]
outline_text = outline_sel.xpath('div[1]/ul').extract()


url='http://jiaoyu.baidu.com/K12BankBws/searchPoint?textbookType=&textbookId=568+&chapterId=33985&outlineId=&pointId=&stage=3&subject=4&quesOrder=1&quesType=&page=2&pageType=1'
fetch(url)
import json
jsondata = json.loads(response.body_as_unicode())
questions = jsondata['data']['tpl']['question_list']
from scrapy.selector import HtmlXPathSelector
from scrapy import Selector
s1=Selector(h5)
sel=s1.css(".question-item")
sel0=sel[0]


/var/tmp/hxkimg/questions/15d7f093c77695f1dffeb341ede12131df819bcf.jpg
/var/tmp/hxkimg/questions/15d7f093c77695f1dffeb341ede12131df819bcf.jpg

url='http://jiaoyu.baidu.com/K12BankBws/searchPoint?textbookType=&textbookId=568+&chapterId=33984&outlineId=&pointId=33984&stage=3&subject=4&quesOrder=1&quesType=&page=168&pageType=1'


scrapy shell "http://jiaoyu.baidu.com/K12BankBws/searchPoint?textbookType=&textbookId=568+&chapterId=33984&outlineId=&pointId=33984&stage=3&subject=4&quesOrder=1&quesType=&page=168&pageType=1"
import json
from scrapy import Selector
jsondata = json.loads(response.body_as_unicode())
questions = jsondata['data']['tpl']['question_list']
selection = Selector(text=questions)
qsels = selection.css(".question-item")
qsel = qsels[0]

#In [43]: import codecs
#In [44]: f=codecs.open('/tmp/a1','w+','utf-8')
#In [45]: f.write(question_content[0])
#In [46]: f.close()

def pstr1(content):
    import codecs
    f=codecs.open('/tmp/a1','w+','utf-8')
    f.write(content)
    f.close()
scrapy shell "http://jiaoyu.baidu.com/K12BankBws/searchPoint?textbookType=&textbookId=568+&chapterId=33984&outlineId=&pointId=33984&stage=3&subject=4&quesOrder=1&quesType=&page=17&pageType=1"
import json
from scrapy import Selector
jsondata = json.loads(response.body_as_unicode())
questions = jsondata['data']['tpl']['question_list']
selection = Selector(text=questions)
qsels = selection.css(".question-item")
xpath_content1 = 'div[1]/div/table/tbody/tr/td/div'
xpath_content2 = 'div[1]/div/table/tbody/tr/td'
xpath_meta1 = 'div[2]/span/text()'
qsel = qsels[0]
sel0 = qsel

"""
feed_id
story_id
title
link
published
updated
author
description
content
"""
####################################

scrapy shell "http://bohaishibei.com"
#import json
from scrapy import Selector
txt=response.body_as_unicode()
selection = Selector(text=txt)
asels = selection.css("article")
sel0 = asels[0]
#/html/body/section/div/div/article[1]
#/html/body/section/div/div/article[1]/header/h2/a #title
title_xpath = 'header/h2/a/text()'
title = sel0.xpath(title_xpath).extract()
link_xpath = 'header/h2/a/@href'
link = sel0.xpath(link_xpath).extract()
#/html/body/section/div/div/article[1]/p[1]
#author_xpath = 'p'
#author = sel0.xpath(author_xpath).extract()
#/html/body/section/div/div/article[1]/p[3]
summary_xpath = 'p[3]/text()'
summary = sel0.xpath(summary_xpath).extract()

#/html/body/section/div/div/article
#/html/body/section/div/div/article[1]/p[1]



######################################
#http://sh.sofang.com/home?cityid=332&cityareaid=2981&busid=0&pricetype=&housetype=&keywords=&page=1
scrapy shell "http://sh.sofang.com/home?cityid=332&cityareaid=2981&busid=0&pricetype=&housetype=&keywords=&page=1"
from scrapy import Selector
txt=response.body_as_unicode()
sel = Selector(text=txt)
sel.xpath('/html/body/div[4]/table/tr')

#houselist page
txt=response.body_as_unicode()
sel = Selector(text=txt)
sel.xpath('/html/body/div[5]/table/tr')

#houselist page
url2='http://sh.sofang.com/community/saa186963-3.htm'
fetch(url2)
txt=response.body_as_unicode()
sel = Selector(text=txt)
ss=sel.xpath('/html/body/div[5]/table/tr')
s1=ss[0]
print s1.xpath('td[2]/div/p[1]/a/text()')

#cm list page
#
url3 = 'http://sh.sofang.com/home?cityid=332&cityareaid=2992&busid=&pricetype=&housetype=&keywords='
fetch(url3)
txt3=response.body_as_unicode()
sel3 = Selector(text=txt3)

/html/body/div[4]/div[2]/ul/li

url4 = 'http://sh.sofang.com/community/raa729354-1.htm'
fetch(url4)
txt4=response.body_as_unicode()
sel4 = Selector(text=txt4)



#############################################
url1="http://shanghai.anjuke.com/sale/pudong/p1/#filtersort"
fetch(url1)

url2="http://shanghai.anjuke.com/prop/view/A452471080?from=structured_dict-saleMetro&spread=filtersearch_p&equid=2016032774b31061-0c&ab=expclick-AJKERSHOUFANG_101_65949717"
fetch(url2)
from scrapy import Selector
txt3=response.body_as_unicode()
sel3 = Selector(text=txt3)
s1=sel3.xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[1]/dl[1]/dd//text()')


url4='http://sh.zu.anjuke.com/fangyuan/pudong/p2/'

fetch(url4)
from scrapy import Selector
txt3=response.body_as_unicode()
sel3 = Selector(text=txt3)



############################################

url4='http://sh.lianjia.com/xiaoqu/d1'

fetch(url4)
from scrapy import Selector
txt3=response.body_as_unicode()
sel3 = Selector(text=txt3)







