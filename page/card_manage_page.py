# -*- coding: utf-8 -*- 
# 2019/12/23 14:29 
# Product
# card_manage_page.py 
# company


from poium import Page, PageElement,PageElements


class FlowCardManage(Page):
    '''
    流量卡管理
    '''
    card_manage = PageElement(xpath="//*[text()='卡片管理']",describe="卡片管理", timeout=3)
    flow_card_manage = PageElement(xpath="//*[text()='流量卡管理']", describe="流量卡管理", timeout=3)
    #入库
    warehousing=PageElement(name="reflesh3",describe="入库", timeout=2)
    supplier=PageElement(id_='supplierUuid',describe="入库-选择供应商")
    cardType = PageElement(id_='cardType', describe="入库-选择卡片类型")
    businessType = PageElement(id_='businessType', describe="入库-选择业务类型")
    cardSize = PageElement(id_='cardSize', describe="入库-选择卡片尺寸")
    expensesPlanCode = PageElement(id_='expensesPlanCode', describe="入库-选择运营商套餐")
    daoruFile = PageElement(id_='daoruFile', describe="入库-选择iccid文件")
    rukuRemark=PageElement(id_='huaboRemark', describe="入库-备注")
    daoruSave = PageElement(id_='daoruSave', describe="入库-保存")


    #划拨
    transferring=PageElement(name="reflesh1",describe="划拨", timeout=2)
    hbcustomername=PageElement(xpath="//*[@id='selectWrap']/div/div/div/span",describe="客户名称")
    hbtestcustomer=PageElement(xpath="//*[@code='eOW1D05c6QmSKal0pxVIG1Vui1xkNFBg']",describe="特定客户名称-假卡专用户")
    hbtestcustomer1 = PageElement(xpath="//*[@code='3ZyHgdEKiSAu0mVkgszcdV25tN0lZ8uM']", describe="特定客户名称-硕汉卡库")
    hbtestcustomer2 = PageElement(xpath="//*[@code='jfM2KGe7NfK5QgnGKroDNM5yrpd8jVPs']", describe="特定客户名称-假卡接盘侠")
    hbprice=PageElement(id_='cardUnitPrice',describe="划拨-单价")
    hbFile = PageElement(id_='huaboFile', describe="划拨-选择iccid文件")
    hbactivetype=PageElement(id_='huaboActive',describe='划拨-激活类型')
    hbsettlementType = PageElement(id_='settlementType', describe='划拨-结算类型')
    hbimeiBind=PageElement(id_='_m2mC_imeiBind',describe='划拨-IMEI绑定')
    hbRemark = PageElement(id_='huaboRemark1', describe="划拨-备注")
    huaboSave = PageElement(id_='huaboSave', describe="划拨-保存")

    starticcid = PageElement(id_='mfi_minIccid',describe='开始的iccid')
    endiccid = PageElement(id_='mfi_maxIccid',describe='结束的iccid')

    #搜索
    search=PageElement(name="搜索",describe="搜索",timeout=2)
    searchcustomer1=PageElement(class_name='allwrap',describe="搜索-客户名称1")
    searchcustomer2=PageElement(xpath='//*[@code="eOW1D05c6QmSKal0pxVIG1Vui1xkNFBg"]',describe="搜索-假卡专用户")
    searchiccid=PageElement(name='iccidOrMsisdn',describe="搜索-iccid、msisdn")
    count=PageElement(xpath="//*[@class='allCount']/div/span[2]",describe="计数")
    #sedcuname = PageElement(xpath="//*[@title='假卡专用户']",describe="iccid搜索后的客户")
    s_cusname = PageElement(xpath='//li[@name="customerName"][@title="假卡专用户"]', describe="搜索-结果条数")

    #高级搜索
    supersearch = PageElement(name="searchAdv",describe="高级搜索",timeout=2)
    ssminiccid=PageElement(id_='minIccid',describe="高级搜索-最小iccid")
    ssmaxiccid=PageElement(id_='maxIccid',describe="高级搜索-最大iccid")
    sscustomername = PageElement(xpath='//*[@id="selectWrap"]/div/div/div/span', describe="高级搜索-客户名称")
    ss_sourcetype=PageElement(xpath='//span/*[@id="sourceType"][@name="sourceType"]',describe="高级搜索-卡片类型")
    ss_shareType = PageElement(id_='shareType',describe="高级搜索-共享类型")
    ss_settlementType = PageElement(xpath='//span/*[@id="settlementType"][@name="settlementType"]', describe="高级搜索-结算类型")
    ss_simstatus=PageElement(xpath='//span/*[@id="simStatus"]',describe="高级搜索-卡片状态")
    ss_mark=PageElement(xpath='//span/*[@id="remark"][@name="remark"]', describe="高级搜索-备注关键字")

    ss_count = PageElement(xpath='//*[@id="dataCon_mc"]/div[12]/div[3]/div[2]/div[1]/span[2]', describe="高级搜索-结果条数")

    ss_atstart=PageElement(id_='activateTimeStart',describe="高级搜索-激活时间开始")
    ss_atend=PageElement(id_='activateTimeEnd',describe="高级搜索-激活时间结束")
    ss_act_year=PageElement(xpath="//*[@lay-type='year']",describe="高级搜索-激活开始时间-年份")
    ss_set_year_2019=PageElement(xpath="//*[@lay-ym='2019']",describe="高级搜索-激活开始为2019年")
    ss_act_month=PageElement(xpath="//*[@lay-type='month']",describe="高级搜索-激活开始时间-月份")
    #0-11，对应1-12月
    ss_set_month_12 = PageElement(xpath="//*[@lay-ym='11']", describe="高级搜索-激活开始为12月")
    ss_set_day_27 = PageElement(xpath="//td[text()='27']", describe="高级搜索-激活开始时间-27日")

    se_act_year = PageElement(xpath="//*[@lay-type='year']", describe="高级搜索-激活结束时间-年份")
    se_act_month = PageElement(xpath="//*[@lay-type='month']", describe="高级搜索-激活结束时间-月份")
    se_act_day = PageElement(xpath="//*[@lay-type='day']", describe="高级搜索-激活结束时间-日")
    ss_set_year_2020 = PageElement(xpath="//*[@lay-ym='2020']", describe="高级搜索-激活开始为2020年")
    ss_set_month_01 = PageElement(xpath="//*[@lay-ym='0']", describe="高级搜索-激活开始为1月")
    ss_set_day_04 = PageElement(xpath="//td[text()='4']", describe="高级搜索-激活开始时间-4日")

    ss_ctstart=PageElement(id_='createTimeStart',describe="高级搜索-发卡时间开始")
    ss_ctend=PageElement(id_='createTimeEnd',describe="高级搜索-发卡时间结束")

    ss_ststart=PageElement(id_='stopTimeStart',describe="高级搜索-到期时间开始")
    ss_stend=PageElement(id_='stopTimeEnd',describe="高级搜索-到期时间结束")
    searchSave = PageElement(id_='searchSave', describe="高级搜索-查询")

    #导出
    export = PageElement(xpath="//*[@name='export']", describe="卡片管理--导出")


    #订购套餐
    orderbag = PageElement(name="reflesh2", describe="订购套餐", timeout=2)
    searchcustomer3 = PageElement(xpath='//*[@code="lmRV7c3XESzgBPuIQRlrQMkGJqLpT9Pq"]', describe="搜索-一级客户")
    gouxuankuang=PageElement(xpath='//*[@class="tbCWrap"]/ul/li[13]/div',describe="第一个勾选框")
    resetbag=PageElement(name='resetBag',describe="重置套餐")
    resetbagsave =PageElement(xpath="//*[@id='myModalResetBag']/div/div[3]/span",describe="套餐重置--确定")
    osourcetype=PageElement(xpath='//*[@id="myModalxufei"]/*/*/*/*/*/*[@id="sourceType"]',describe="订购套餐-卡片类型")
    obag=PageElement(xpath='//div[@class="packageId"]/div[1]/span',describe="订购套餐-套餐选择")
    ochosebag=PageElement(xpath='//*[@code="OPE2BFgg4zxQHgMQNCCrPN0g2uspK2MP"]', describe="订购套餐-选择主：联通10G/月")
    ochosenum=PageElement(id_="xufeiNum",describe="订购套餐-数量选择")


    osavebag=PageElement(id_='xufeiSave',describe="订购套餐-确定")



    #导入日志
    sysmanage=PageElement(xpath='/html/body/div[1]/div[1]/div/div[4]/div[12]/p/span[2]',describe="系统管理", timeout=2)
    im_log = PageElement(xpath='/html/body/div[1]/div[1]/div/div[4]/div[12]/div[1]/p/span',describe="导入日志记录", timeout=2)
    allcount = PageElement(xpath='//*[@class_name="allCount"]/div/span[2]',describe="客户列表资料",timeout=1)

    #刷新
    reflesh=PageElement(name="reflesh", describe="刷新")