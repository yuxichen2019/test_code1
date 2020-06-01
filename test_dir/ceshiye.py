# -*- coding: utf-8 -*- 
# 2020/01/08 9:57 
# Product
# ceshiye.py 
# company



# -*- coding: utf-8 -*-
# 2019/10/24 14:16
# Test
# Download_File.py
# hanwenlu

#导出状态变更记录

from selenium import webdriver
from time import sleep
import os
import requests
import json
from test_dir.common import Mysql,W_excel,Api



#
# api = Api()
# '''
# options = webdriver.ChromeOptions()
# prefs = {'profile.default_content_settings.popups':0,#禁止弹出下载窗口
#          'download.default_directory': r'E:\yuxichen\Product\test_dir\data\down_file' } #设置下载路径
# options.add_experimental_option('prefs',prefs)
#
# #  这里将课本的 chrome_options=options 改为options=options
# dr = webdriver.Chrome(options=options)
#
# dr.get('http://192.168.1.104:7300/html/index.html')
# dr.maximize_window()
# sleep(1)
# #登录
# dr.find_element_by_xpath("//input[@class='lg_login_user_input']").send_keys('admin')
# dr.find_element_by_xpath("//input[@class='lg_login_pw_input']").send_keys('123456')
# dr.find_element_by_xpath("//div[@class='lg_login_btn_lg']").click()
# sleep(1)
#
# #卡片管理
# dr.find_element_by_xpath("//*[text()='卡片管理']").click()
# sleep(2)
#
# dr.find_element_by_xpath("/html/body/div/div[1]/div/div[4]/div[3]/div[1]/p/span").click()
# sleep(1)
#
# dr.find_element_by_class_name('allwrap').click()
# dr.find_element_by_xpath('//*[@code="lmRV7c3XESzgBPuIQRlrQMkGJqLpT9Pq"]').click()
# dr.find_element_by_name('iccidOrMsisdn').send_keys('89860619050008947664')
# dr.find_element_by_name('搜索').click()
# dr.find_element_by_xpath("//*[@id='dataCon_mc']/div[12]/div[2]/div/div[3]/ul/li[13]/div").click()
#
# dr.find_element_by_name('reflesh2').click()'''

# dr.find_element_by_name('export').click()
# sleep(2)
#
# file_path = r'E:\yuxichen\Product\test_dir\data\down_file'
#
# list=os.listdir(file_path)
# print(list[-1])
#
# print(os.path.join(file_path,list[-1]))


# headers = {    "Content-Type":"application/json" }
# url= 'http://192.168.6.99:7300/index/m2m/api/v1'

# data_json={
#     "iccid":"89860619050008947664",
#     "method":"sohan.m2m.iccid.deactivate",
#     "sign":"84FB4DAF697852EDD74E778137EA53D8",
#     "timestamp":"1578385382980",
#     "username":"客户演示"
# }
# #data = json.dumps(data_json)
#
# api=Api()
#
# res=api.stop_card_699(data_json)
# print(res)
# print(res.get('errorCode'))

# res = requests.post(url, data=data_json, headers=headers)
# print(res.text)
# print(type(res.text))
# dict=eval(res.text)
# print(dict.get('errorCode'))
# data_qc={"iccid":"89860619050008947664",
#                             "method":"sohan.m2m.iccidinfo.queryone",
#                             "sign":"E0469BBE55C252734E9EFA82A8F0CDAD",
#                             "timestamp":"1578553270141",
#                             "username":"一级客户"
#                             }
#
# res_query=api.ask_104(data_qc)
# dict = res_query.get('data')
# print('调用查询接口成功~~~~ %s' % (dict.get('cardStatus')))
# print(type(dict.get('cardStatus')))


m=Mysql()
m.execQuery('SELECT iccid FROM t_card_store')