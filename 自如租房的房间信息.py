#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 13:01:40 2018

@author: oyc
"""

from selenium import webdriver
import time
from multiprocessing.pool import Pool
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import pytesseract


class RoomItem(object):
    title=None
    location=None
    price=None
    MianJi=None
    ChaoXiang=None
    HuXing=None
    LouCeng=None
    JiaoTong=None
    Bed=None
    YiGui=None
    ShuZhuo=None
    WiFi=None
    XiYiJi=None
    ReShuiQi=None
    KongTiao=None
    WeiBoLun=None
    ZhiNengSuo=None
    
    ImageUrl=None
    
    
def get_productlist(browser,price):
    print('价格为:'+str(price))
    roomIn_List=[]
    rooitem=RoomItem()
    rooitem.title=browser.find_element_by_xpath("//div[@class='area clearfix']//div[@class='room_detail_right']//div[@class='room_name']//h2").text.strip()
    rooitem.location=browser.find_element_by_xpath("//div[@class='area clearfix']//div[@class='room_detail_right']//div[@class='room_name']//p[@class='pr']//span[@class='ellipsis']").text.strip()
    rooitem.price=price
    #rooitem.price=browser.find_element_by_xpath("//div[@class='area clearfix']//div[@class='room_detail_right']//div[@class='room_name']//p[@class='pr']//span[@class='price']").text.strip()
    li=browser.find_elements_by_xpath("//div[@class='area clearfix']//div[@class='room_detail_right']//ul[@class='detail_room']//li")
    rooitem.MianJi=li[0].text.strip()
    rooitem.ChaoXiang=li[1].text.strip()
    rooitem.HuXing=li[2].text.strip()
    rooitem.LouCeng=li[3].text.strip()
    rooitem.JiaoTong=li[4].find_element_by_xpath(".//span").text.strip()
    
    
    room_li=browser.find_elements_by_xpath("//div[@class='area clearfix']//div[@class='room_detail_left']//div[@class='configBox']//ul[@class='configuration clearfix']//li")
    if(room_li[0].text.strip() is None):
        rooitem.Bed=0
    else:
        rooitem.Bed=1
     
    if(room_li[1].text.strip() is None):
        rooitem.YiGui=0
    else:
        rooitem.YiGui=1
        
    if(room_li[2].text.strip() is None):
        rooitem.ShuZhuo=0
    else:
        rooitem.ShuZhuo=1
    
    if(room_li[3].text.strip() is None):
        rooitem.WiFi=0
    else:
        rooitem.WiFi=1
        
    if(room_li[4].text.strip() is None):
        rooitem.XiYiJi=0
    else:
        rooitem.XiYiJi=1
        
    if(room_li[5].text.strip() is None):
        rooitem.ReShuiQi=0
    else:
        rooitem.ReShuiQi=1
        
    if(room_li[6].text.strip() is None):
        rooitem.KongTiao=0
    else:
        rooitem.KongTiao=1
        
    if(room_li[7].text.strip() is None):
        rooitem.WeiBoLun=0
    else:
        rooitem.WeiBoLun=1
        
    if(room_li[8].text.strip() is None):
        rooitem.ZhiNengSuo=0
    else:
        rooitem.ZhiNengSuo=1
        
        
    ''' 
    rooitem.Bed=room_li[0].text.strip()
    rooitem.YiGui=room_li[1].text.strip()
    rooitem.ShuZhuo=room_li[2].text.strip()
    rooitem.WiFi=room_li[3].text.strip()
    rooitem.XiYiJi=room_li[4].text.strip()
    rooitem.ReShuiQi=room_li[5].text.strip()
    rooitem.KongTiao=room_li[6].text.strip()
    rooitem.WeiBoLun=room_li[7].text.strip()
    rooitem.ZhiNengSuo=room_li[8].text.strip()
    '''
    
    Image_li=browser.find_elements_by_xpath("//div[@class='area clearfix']//div[@class='room_detail_left']//div[@id='lofslidecontent45']//div[@class='lof-main-outer']//ul//li")
    rooitem.ImageUrl=Image_li[0].find_element_by_xpath(".//a").get_attribute('href')
    
    
    #print('1111'+str(rooitem.Bed))
    roomIn_List.append(rooitem)
    return roomIn_List
        
def txt(rooms):
    #写入文件中
    with open('roomInfo.txt','a+',encoding='utf-8') as f:
        for room in rooms:
            f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(room.title,room.location,room.price,room.MianJi,room.ChaoXiang,room.HuXing,room.LouCeng,room.JiaoTong,room.Bed,room.YiGui,room.ShuZhuo,room.WiFi,room.XiYiJi,room.ReShuiQi,room.KongTiao,room.WeiBoLun,room.ZhiNengSuo,room.ImageUrl))

#获取价格的位置
def get_position(browser):
    img = WebDriverWait(browser,20).until(EC.presence_of_element_located((By.CLASS_NAME, 'room_price')))
    time.sleep(2)
    location = img.location
    size = img.size
    top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
    return (top, bottom, left, right)

#截图全网页的
def get_screenshot(browser,name):

    browser.save_screenshot(name)
    screenshot = Image.open(name)
    return screenshot

def get_geetest_image(name1,name2,browser):

    top, bottom, left, right = get_position(browser)  #获取价格位置
    #print('验证码位置', top, bottom, left, right)
    screenshot = get_screenshot(browser,name1) #获取网页截图
    #crop():从图像中提取出某个矩形大小的图像。它接收一个四元素的元组作为参数，各元素为(left, upper, right, lower),坐标系统的原点(0, 0)是左上角。
    #用ps看了图形验证码的像素位置,刚好是给的位置参数乘以2
    captcha = screenshot.crop((2*left, 2*top, 2*right, 2*bottom))  #调用crop（）方法将图片裁剪出来，返回的是Image对象
    #所以保存下来的2张验证码的图还要压缩一下分辨率
    size=258,159
    captcha.thumbnail(size) #生成缩略图 
    captcha.save(name2)#保存图片
    return captcha
        
def main(url):
    browser=get_Chrome(url)
    get_geetest_image('captcha1.png','captcha2.png',browser)
    
    try:
        image=Image.open('captcha2.png')
        price=pytesseract.image_to_string(image).split('¥')
        #print(price[1])
    
        rooms=get_productlist(browser,price[1])
    except:
        rooms=get_productlist(browser,2000)
        
        
    txt(rooms)#存储
    browser.close()

def get_Chrome(url):
    #url='http://www.ziroom.com/z/vr/61546574.html'
    browser=webdriver.Chrome()
    browser.get(url)
    time.sleep(3)
    return browser


    

if __name__=='__main__':
    with open('room_url.txt','r+',encoding='utf-8') as f:
        pool=Pool()
        groups=([url for url in f.readlines()])
        pool.map(main,groups)#利用线程池
        pool.close()
        pool.join()
            
    
    
            
            
    