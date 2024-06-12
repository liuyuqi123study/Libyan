import csv
import os
import random
import re
import time

import dateutil.parser as dparser
from random import choice
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

start_date=dparser.parse("2023-01-20")#因为留言板上也只有这个日期之后的留言
chrome_options=Options()#对选项进行初始化
chrome_options.add_argument('blink-setting=imagesEnabled=false')
#禁止网页加载图片，减少对网络的带宽要求

def get_time():
    '''获取随机时间'''
    return round(random.uniform(3,6),1)

def get_user_agent():
    '''获取随机用户代理'''
    user_agents = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
        "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36",
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20",
        "Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
        "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html）"
    ]
    #在该列表中随机产生一个代理，作为模拟的浏览器
    user_agent=choice(user_agents)
    return user_agent
#生成具体的url
def get_detail_urls(list_url):
    """获取每个领导的所有留言链接"""
    user_agent=get_user_agent()#首先，获取一个用户代理服务器
    chrome_options.add_argument('user_agent=%s'%user_agent)
    drivertemp=webdriver.Chrome(options=chrome_options)
    drivertemp.maximize_window()
    drivertemp.get(list_url)
    #对指定的网页进行抓取
    time.sleep(2)
    #循环加载页面
    while True:
        datestr=WebDriverWait(drivertemp,10).until(
            lambda driver:driver.find_element(By.XPATH,'//*[@class="replyList"]/li[position()=last()]/div/div/p')).text.strip()
#寻找所有id属性为list_content的标签下最后一个li标签h3下面的span标签
        #获取日期
        datestr=re.search(r'\d{4}-\d{2}-\d{2}',datestr).group()
        date=dparser.parse(datestr,fuzzy=True)
        print('正在爬取链接 --','position','--',date)
        try:
                WebDriverWait(drivertemp,50,2).until(EC.element_to_be_clickable((By.CLASS_NAME,"mordList")))
                drivertemp.execute_script('window.scrollTo(document.body.scrollHeight,document.body.scrollHeight-600)')
                time.sleep(get_time())#滚动到某个坐标
                drivertemp.execute_script("window.scrollTo(document.body.scrollHeight-600,document.body.scrollHeight)")
                WebDriverWait(drivertemp,50,2).until(EC.element_to_be_clickable((By.CLASS_NAME,"mordList")))
                #这是一个什么样的加载行为
                #随便划一划再点击？
                drivertemp.find_element(By.CLASS_NAME,"mordList").click()
        except:
            break
        time.sleep(get_time()-1)
    #获取每条留言对应的ID
    detail_elements=drivertemp.find_elements(By.XPATH,'//*[@class="replyList"]/li//span[@class="t-mr1 t-ml1"]')
    for element in detail_elements:
        detail_ID=re.search(r'\d{8}',element.text).group()
        detail_url='http://liuyan.people.com.cn/threads/content?tid='+detail_ID
        yield detail_url
    drivertemp.quit()
    #因为我只爬取贺部长的留言，可能不需要position
def get_message_detail(driver,detail_url,writer):
    '''获取留言详情'''
    print("正在爬取留言","--",detail_url)
    driver.get(detail_url)#对特定的网页进行爬取
    #获取留言各部分内容
    message_date_temp=WebDriverWait(driver,2.5).until(lambda driver:driver.find_element(By.XPATH,"/html/body//li[@class='replyMsg']/span[2]")).text

    message_datetime=message_date_temp[:10]
    #获取留言的标题
    message_title=WebDriverWait(driver,2.5).until(
        lambda driver:driver.find_element(By.XPATH,'//div[@class="replyInfoHead clearfix"]/h1').text.strip()
    )
    message_content=WebDriverWait(driver,2.5).until(lambda driver:driver.find_element(By.XPATH,"//div[@class='clearfix replyContent']/p")).text.strip()
    writer.writerow([message_datetime,message_title,message_content])

#获取贺荣部长的留言详情
def get_officer_messages():
    user_agent=get_user_agent()
    chrome_options.add_argument('user-agent=%s'%user_agent)
    driver=webdriver.Chrome(options=chrome_options)
    list_url="http://liuyan.people.com.cn/threads/list?fid=5058&formName=%E5%8F%B8%E6%B3%95%E9%83%A8%E5%85%9A%E7%BB%84%E4%B9%A6%E8%AE%B0%E3%80%81%E9%83%A8%E9%95%BF%E8%B4%BA%E8%8D%A3&position=1"
    driver.get(list_url)
    #开始计时
    start_time=time.time()
    csv_name="Herong.csv"
    #文件如果存在就删除重新创建
    if os.path.exists(csv_name):
        os.remove(csv_name)
    with open(csv_name,"a+",newline='',encoding='gb18030') as f:
        writer=csv.writer(f,dialect='excel')
        writer.writerow(['留言日期','留言标题','留言内容'])
        for detail_url in get_detail_urls(list_url):
            get_message_detail(driver,detail_url,writer)
            time.sleep(get_time())
    end_time=time.time()
    crawl_time=int(end_time-start_time)
    crawl_minute=crawl_time//60
    crawl_second=crawl_time%60
    print("已经爬取结束！！")
    print("爬取用时：{}分{}秒".format(crawl_minute,crawl_second))
    driver.quit()
    time.sleep(5)
if __name__=='__main__':
    get_officer_messages()


