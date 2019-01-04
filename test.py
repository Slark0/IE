import tkinter
from tkinter import Label, Button, END
from tkinter.tix import Tk, Control, ComboBox
from tkinter.messagebox import showinfo, showwarning, showerror
from functools import partial
from tkinter import filedialog
from tkinter import *
import jieba
import jieba.posseg as pseg
from timeit import timeit
'''
seg_list = jieba.cut("我:来到北京清华大学“这里，有好多-朋友”", cut_all=False)
print("Default Mode: " + "\ ".join(seg_list))

words = pseg.cut("我:来到北京清华大学“这里，有好多-朋友”")
for word, flag in words:
    print("%s %s" % (word, flag))

result = jieba.tokenize("净投放2000亿元农产品多数飘绿，审核门槛在提高，我:来到北京清华大学“这里，有好多-朋友")
for tk in result:
    print("word %s\t\t start:%d\t\t end:%d" % (tk[0],tk[1],tk[2]))
'''

'''
def find(string, text):
    if string.find(text) > -1:
        pass


def re_find(string, text):
    if re.match(text, string):
        pass


def best_find(string, text):
    if text in string:
        pass


#re.search('www', 'www.runoobk.com').span()
print(timeit("find(string, text)", "from __main__ import find; string='lookforme'; text='look'"))
print(timeit("re_find(string, text)", "from __main__ import re_find; string='lookforme'; text='look'"))
print(timeit("best_find(string, text)", "from __main__ import best_find; string='lookforme'; text='look'"))


text = "标普500指数上涨1.2% 能源股集体表现强劲0.1124元/吨"
start = text.find('500指数上涨1.2% 能')
end = start + len('500指数上涨1.2% 能')

print(str(start) + '-' + str(end))
'''
'''
text2 = "LME期铜收跌0.3%，报6839美元/吨，一度录得5月8日以来盘中低位6727美元。 \
        伦锌收涨1.3%，报3130美元，一度刷新最近一个月盘中高位至3139.50美元。伦铝收跌0.2%， \
        报2270美元。伦铅收跌0.4%，报2435美元。伦镍收涨1.5%，报15135美吨。伦锡收涨0.7%，报20575美元。"
tm = re.finditer('美元', text2)
for m in tm:
    print(str(m.start()) + ',' + str(m.end()))
'''
text = "在无论如何2017年第10界中国各种博览会上，2019年界国际发展论坛， \
        在“2018年（第三届）中国钢铁金融衍生品国际大会”上表示，今年以来 \
        在第十届陆家嘴论坛上 \
        第9界美国论坛29年7月，29年5月2日，去年9月2日，今年12月15日，去年同期，前年一月，去年一月，去年十一月，2003年3月1日"
confenrence_pattern = re.compile(r'((\d{2,4}年)|(第\S*界))(第\S界)?\S*?(大会|会议|博览会|展览会|讨论会|研讨会|展销会|小组会|年会|论坛|峰会|博会)')
#print(re.search(confenrence_pattern, text).start())
match = re.finditer(confenrence_pattern, text)
for m in match:
    print(m.group(0))
content = r'<xxxx><xxxx><xxxx><xxxx>'
#惰性匹配
print(re.search('<.*>',content).span())
#非惰性匹配
print(re.search('<.*?>',content).span())

str1 = 'hello111-222-333'
p1 = r'.+\d+-\d+'
p2 = r'.+(\d+-\d+)'
p3 = r'.+?(\d+-\d+)'
print(re.match(p1, str1).group())
print(re.match(p2, str1).group(1))
print(re.match(p3, str1).group(1))

number_text = r'​财联社2018年12月31日讯，去年2月5日，今年2月，今年10月5日，本月7号凌晨，1日上午，25号夜晚，\
                本月15日，今年11月2号，2000年5月1号，19年9月，2019年9月15日，美元/日元刷新6个月低点，下跌0.49%至109个百分点，\
                财联社2018年2月32日讯，法国CAC40指数收盘上涨51.96点，涨幅1.11%，报4730.69点 \
                美银美林编制的中国国债指数今年回报率为7.6%。公司债回报率为6.9%，中国国家开发银行等官方政策性银行所发行债券的回报率为9.9% \
                在岸人民币兑美元收复6.85关口，涨0.000386%，破3000点大关，破3000大关较上一交易日涨超150个点，15点'
percent_pattern = re.compile(r'\d+(\.\d+)?(%|点关口|关口|点大关|大关|个百分点|个点|点)')
ms = re.finditer(percent_pattern, number_text)
for mit in ms:
    print(mit.group())
print('percent------------------------------------------------------')
date_pattern = re.compile(r'((((去|今|\d{2,4})年)?(\d{1,2}|本|上)月(\d{1,2}(日|号))?)|(\d{1,2}(日|号)))(上午|下午|中午|晚间|夜晚|凌晨)?')
m3 = re.finditer(date_pattern, number_text)
for i in m3:
    print(i.group())
print('date------------------------------------------------------')
num = 5
period_text = r'美国商务部长罗斯5月31日表示，美国将从6月1日开始对欧盟、自本月1日起，2号起，自2019年起，10月期间，2000年期间从去年2月起起加拿大和墨西哥的钢铝产品分别征收25%和10%的关税'
period_pattern = r'(((去年|今年|\d{2,4}年)?(\d{1,2}|本|上)月(\d{1,2}(日|号))?)|((去|今|\d{2,4})年)|(\d{1,2}(日|号)))(以来|开始|始|起|期间)'
pms = re.finditer(period_pattern, period_text)
for pm in pms:
    print(pm.group())
print('period------------------------------------------------------')
price_pattern = re.compile(r'\d+(\.\d+)?(万元/平方米|美元/桶|美元/吨|美金/吨|元/立方米|万桶/日|欧元/公斤|6元/手|元/吨|美元关口|亿元|万美元|万亿美元|美元|亿美元|元人民币|万亿|美金|亿日元|万元|元)')
measure_pattern = re.compile(r'\d+(\.\d+)?(千公顷|万公顷|公顷|万平方米|千平方米|平方米)')
count_pattern = re.compile(r'第?\d+(起|次|宗|辆|台|套|场|件|项|家|万股|千股|股)')  # 个 usually used with 月， they stand for a period
supplementary_pledge_pattern = re.compile(r'补充质押') # event type

count_text = r'6月22日，自然资源部举行新闻发布会，6月21日，备受关注的华润城润府三期正式公布销售方案，40.66亿美元 \
             购买SQM公司23.77%股权的12项议案 \
             北京市经信局近日对外发布《北京市（fuck）智能网联汽车创新发展行动方案（2019年-2022年）》。 \
            今年北京计划建设用地供应总量4300公顷，其中住宅用地1200公顷 \
             LME期铜收平，报6789美元/吨，本周累跌3.2%。 （的发生（叫我）去几个人）LME期铝收跌0.2%，报2175.50美元/吨。 LME期铅收涨1.7%，报2414.50美元/吨 \
             第29项，第10家, 28321473289项法案 \
             开盘均价8.55万元/平方米，最低7.53万元/平方米，向社会公布16起违法案件查处结果，其中矿产案件4起，土地案件6起，海洋案件2起，林业案件4起。（北京日报）'
brackets_text = r'息化部无线电管理局（艹）组织召开5G基站与扩展C频段（3400－3700MHz）卫星地球站兼容共存分析讨论会。会议提出，继续做好5G基站与同频、邻频卫星地球站兼容共存的外场测试验证工作。（中国证券网）'
m4 = re.finditer(count_pattern, count_text)
for mm in m4:
    print(mm.group())

news_content = re.sub(r'(（[^）（]+?）)$', '', brackets_text)
print(news_content)


def test():
    a = 1
    b = 2
    return a, b


def testmain():
    c, d = test()
    print('c: ' + str(c) + ' d: ' + str(d))


testmain()