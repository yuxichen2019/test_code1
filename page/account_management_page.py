# -*- coding: utf-8 -*- 
# 2019/12/19 9:45 
# Product
# account_management_page.py 
# company

from poium import Page, PageElement,PageElements

class AccountManagement(Page):
    customer_list = PageElement(xpath="/html/body/div/div[1]/div/div[4]/div[1]/div[2]/p", describe="客户列表",timeout=6)
    add_client = PageElement(name="add", describe="添加客户",timeout=2)
    input_cname=PageElement(xpath='//*[@name="customerName"]/div[2]/input',describe="输入客户名称",timeout=6)
    input_phone = PageElement(xpath='//*[@name="phone"]/div[2]/input', describe="输入电话号码")
    input_city = PageElement(xpath='//*[@name="region"]/div[2]/input', describe="输入省市")
    customer_level = PageElement(xpath='//*[@name="level"]/span',describe='选择客户级别')
    customer_level_1 =PageElement(xpath='//*[@name="level"]/div[1]/p[2]',describe='一级客户')
    pay_type=PageElement(xpath='//*[@name="payType"]/span',describe="付费方式")
    after_pay = PageElement(xpath='//*[@name="payType"]/div/p[3]',describe="后付费")
    save =PageElement(class_name='viewC_btnSave',describe="保存",timeout=1)
    customer_text = PageElements(xpath='//*[@class_name="tbCWrap"]/*',describe="客户列表资料",timeout=1)

