#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 13:13:58 2018

@author: oyc
"""

from selenium import webdriver
import time
from multiprocessing.pool import Pool


def get_productlist(browser,current_page):
    print('正在爬取'+'第'+str(current_page)+'页内容')
    productlist=browser.find_elements_by_xpath("//div[@class='t_myarea t_mainbox clearfix mt15 t_zindex0']//div[@class='t_newlistbox']//ul[@id='houseList']//li[@class='clearfix']")
    #print('66666'+str(productlist))
    
    for product in productlist:
        room={}
        name=product.find_element_by_xpath(".//div[@class='txt']//h3//a").text
        url_room=product.find_element_by_xpath(".//div[@class='txt']//h3//a").get_attribute('href')
        #print('6666'+str(name)+'  '+str(url_room))
        room['name']=name
        room['url_room']=url_room
        yield room
    
        
def txt(room):
    #写入文件中
    with open('ziru_url.txt','a+',encoding='utf-8') as f:
        f.write(str(room)+'\n')
      

        
def main(i):
    browser=get_Chrome(i)
    time.sleep(1)
    rooms=get_productlist(browser,i)
    for room in rooms:
        print(room)
        txt(room)
    browser.close()


def get_Chrome(index):
    url='http://www.ziroom.com/z/nl/z3.html?utm_source=baidu&utm_medium=cpc&utm_term=bj.58.com%2Fzufang&utm_content=%E5%B9%B3%E5%8F%B0&utm_campaign=%E5%8C%97%E4%BA%AC-pc-%E8%A1%8C%E4%B8%9A%E5%AE%9A%E6%8A%95&p='+str(index)
    browser=webdriver.Chrome()
    browser.get(url)
    time.sleep(3)
    return browser
    
if __name__=='__main__':      
    '''
    options = webdriver.ChromeOptions()# 进入浏览器设置
    options.add_argument('lang=zh_CN.UTF-8')# 设置中文
    #selenium设置chrome请求头
    options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"')# 更换头部
    '''
    
    '''
    rooms=get_productlist(browser,1)
    for room in rooms:
        print(room)
    
    '''
    '''
    for i in range(5,10):
        rooms=get_productlist(browser,i)
        for room in rooms:
            print(room)
            txt(room)
        hanle(browser)#获取句柄
    '''  
    pool=Pool()
    groups=([x for x in range(1,50)])
    pool.map(main,groups)#利用线程池
    pool.close()
    pool.join()