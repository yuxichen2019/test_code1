# -*- coding: utf-8 -*- 
# 2019/12/24 11:45 
# Product
# system_manage.py 
# company



from poium import Page, PageElement,PageElements

class SysManage(Page):
    '''
    系统管理
    '''
    sysmanage=PageElement(xpath="/html/body/div/div[1]/div/div[4]/div[12]/p/span[2]", describe="系统管理", timeout=2)
    import_log=PageElement(xpath="/html/body/div/div[1]/div/div[4]/div[12]/div[1]/p/span", describe="导入记录", timeout=2)
    count = PageElement(xpath='//*[@id="dataCon"]/div/div[3]/div[2]/div/span[2]', describe="条数统计", timeout=2)

