# -*- coding: utf-8 -*- 
# 2019/12/23 14:26 
# Product
# test_card_manage.py 
# company

import pytest,os,sys,json
from page.card_manage_page import FlowCardManage
from time import sleep
from os.path import dirname, abspath
base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)
from selenium.webdriver.support.select import Select
from test_dir.common import Mysql,W_excel,Api

#只有当在脚本中执行的时候，os.path.abspath(__file__)才会起作用，因为该命令是获取的当前执行脚本的完整路径
# iccid_path = os.path.abspath(r'E:\yuxichen\Product\test_dir\data\ruku_iccid.xlsx')

iccid_path = base_path+r'\test_dir\data\ruku_iccid.xlsx'
mq = Mysql()
we = W_excel()
api = Api()

class TestRuku():
    '''
    流量卡管理-入库
    '''
    def get_data(file_path):
        """
        读取参数化文件
        """
        data = []
        with(open(file_path, "r",encoding='UTF-8')) as f:
            dict_data = json.loads(f.read())
            for i in dict_data:
                data.append(tuple(i.values()))
        return data

    @pytest.mark.parametrize(
        "name, supplier,businessType,cardsize,expensesPlanCode,remark",
        #get_data(base_path + "/test_dir/data/ruku_canshu.json")
        get_data(base_path + "/test_dir/data/ruku_canshu.json")
    )

    def test_ruku(self,name,browser,login_m,supplier,businessType,cardsize,expensesPlanCode,remark):
        '''
        入库
        '''
        #查询导入日志记录原来的数量
        sql_import_log = """
        SELECT count(uuid) FROM t_import_log
        """


        # 执行SQL语句
        old = mq.execQuery(sql_import_log)
        print(old)

        fc = FlowCardManage(browser)
        fc.card_manage.click()
        fc.flow_card_manage.click()
        #入库按钮
        fc.warehousing.click()
        Select(fc.supplier).select_by_visible_text(supplier)
        Select(fc.businessType).select_by_value(businessType)
        Select(fc.cardSize).select_by_index(cardsize)
        Select(fc.expensesPlanCode).select_by_visible_text(expensesPlanCode)
        fc.daoruFile.send_keys(iccid_path)
        sleep(5)
        fc.rukuRemark=(remark)
        fc.daoruSave.click()
        sleep(1)

        new  = mq.execQuery(sql_import_log)
        print(new)
        assert old[0][0] == new[0][0]


class TestHuabo():
    '''
    流量卡管理-划拨
    '''

    @pytest.mark.parametrize(
        "price,activetype, settlementType,imei,mark",
        [("1","自动激活", "月结日结算","不绑定IMEI","划拨测试")
         ],
        ids=["case1"])

    def test__huabo1(self,browser,login_m,price,activetype,settlementType,imei,mark):
        '''
        划拨-文件方式
        '''
        fh = FlowCardManage(browser)
        sleep(1)
        fh.card_manage.click()
        fh.flow_card_manage.click()
        fh.transferring.click()
        #划拨到假卡专用户
        fh.hbcustomername.click()
        fh.hbtestcustomer.click()
        fh.hbprice=(price)
        fh.hbFile.send_keys(iccid_path)
        Select(fh.hbactivetype).select_by_visible_text(activetype)
        Select(fh.hbsettlementType).select_by_visible_text(settlementType)
        Select(fh.hbimeiBind).select_by_visible_text(imei)
        fh.hbRemark=(mark)
        fh.huaboSave.click()


        # 执行SQL语句
        sql='''
        SELECT customer_name FROM `t_customer` t1 left join t_hierarchy t2 on  substring_index( t2.hierarchy_code, "_",- 1 ) = t1.uuid where t2.iccid_ = '%s'
        '''

        data=(we.get_some(iccid_path))

        self.customername = mq.execQuery(sql % data)
        assert self.customername[0][0] == "假卡专用户"

    @pytest.mark.parametrize(
        "price1,activetype1, settlementType1,imei1,mark1",
        [("1","自动激活", "月结日结算","不绑定IMEI","划拨测试2")
         ],
        ids=["case1"])

    def test__huabo2(self, browser,login_m, price1, activetype1, settlementType1, imei1, mark1):
        '''
        回划硕汉卡库,按iccid开始结束段
        '''
        sql_a = '''
                        SELECT customer_name FROM `t_customer` t1 left join t_hierarchy t2 on  substring_index( t2.hierarchy_code, "_",- 1 ) = t1.uuid where t2.iccid_ = '%s'
                        '''

        sql_b = '''
                        SELECT remark FROM `t_card_store` where iccid = '%s'
                        '''
        #获取到卡号iccid
        data = (we.get_some(iccid_path))


        fh = FlowCardManage(browser)
        sleep(1)
        fh.card_manage.click()
        fh.flow_card_manage.click()
        fh.transferring.click()
        fh.hbcustomername.click()
        # 划拨回硕汉卡库
        fh.hbtestcustomer1.click()
        fh.hbprice = (price1)
        fh.starticcid=(data)
        fh.endiccid=(data)
        Select(fh.hbactivetype).select_by_visible_text(activetype1)
        Select(fh.hbsettlementType).select_by_visible_text(settlementType1)
        Select(fh.hbimeiBind).select_by_visible_text(imei1)
        fh.hbRemark = (mark1)
        fh.huaboSave.click()

        self.customername = mq.execQuery(sql_a % data)
        self.test_mark=mq.execQuery(sql_b % data)

        assert self.customername[0][0] == "硕汉卡库" and self.test_mark[0][0] == mark1



class TestSearch():

    def test_search_by_customer(self,browser,login_m):
        '''
        搜索--客户
        '''
        fs=FlowCardManage(browser)
        fs.card_manage.click()
        fs.flow_card_manage.click()
        fs.searchcustomer1.click()

        #搜索假卡专用户名下有多少假卡
        fs.searchcustomer2.click()
        fs.search.click()
        sleep(2)
        count2 = int(fs.count.text)


        #从数据库中找出假卡专用户有多少张卡
        sql='''SELECT count(iccid_) from t_hierarchy t1 left join t_customer t2 on t2.uuid = substring_index( t1.hierarchy_code, "_",- 1 ) where t2.customer_name = '假卡专用户'
        '''
        count1 = mq.execQuery(sql)

        assert count1[0][0] == count2

    def test_search_by_iccid(self,browser,login_m):
        '''
        搜索--ICCID
        '''
        iccid = "99999888886666610001"
        fs=FlowCardManage(browser)
        fs.card_manage.click()
        fs.flow_card_manage.click()
        fs.searchiccid=(iccid)
        fs.search.click()
        #结果列表的客户名称
        text= fs.s_cusname.text

        sql='''select t1.customer_name from t_customer t1  left join t_hierarchy t2 on t1.uuid = substring_index( t2.hierarchy_code, "_",- 1 ) WHERE t2.iccid_ = "%s"
        '''
        data = iccid
        customername  = mq.execQuery(sql % data)

        assert text == customername[0][0]

class TestSuperSearch():
    '''
    高级搜索功能
    '''

    '''1可激活  2已激活 3停用 4失效 5库存'''

    @pytest.mark.parametrize(
        " wenben, type,statu",
        [( "1","1","1"),
         ( "2","2","2"),
         ( "3","3","2"),
         ( "4","4","4"),
         ],
        ids=["S1", "X", "W","S2"])

    def test_cusname_cardtype_simstatu(self,browser,login_m,wenben,type,statu):
        '''
        高级搜索的客户（假卡专用户）+卡片类型（1234）
        '''
        fss=FlowCardManage(browser)
        fss.card_manage.click()
        fss.flow_card_manage.click()
        fss.supersearch.click()
        fss.sscustomername.click()
        #假卡专用户
        fss.searchcustomer2.click()
        Select(fss.ss_sourcetype).select_by_index(type)
        Select(fss.ss_simstatus).select_by_index(statu)
        fss.searchSave.click()
        sleep(2)

        #查询搜出来多少条记录
        text = int(fss.ss_count.text)
        #查询假卡专业户名下有多少张对应类型的卡片
        sql ='''SELECT	count( iccid ) FROM	t_card_store t1	LEFT JOIN t_hierarchy t2 ON t1.iccid = t2.iccid_	LEFT JOIN t_suppliers t3 ON t1.supplier_uuid = t3.uuid WHERE	SUBSTRING_INDEX( t2.hierarchy_code, "_",- 1 ) = "eOW1D05c6QmSKal0pxVIG1Vui1xkNFBg" 	AND t3.source_type = "%s"  and t1.sim_status = "%s"      '''
        data = (type,statu)
        count = mq.execQuery(sql % data)
        assert count[0][0] == text

    def test_min_max(self,browser,login_m):
        '''
        按iccid区间查找
        '''
        miniccid='99999888886666610001'
        maxiccid='99999888886666610010'
        fmm=FlowCardManage(browser)
        fmm.card_manage.click()
        fmm.flow_card_manage.click()
        fmm.supersearch.click()
        fmm.ssminiccid=(miniccid)
        fmm.ssmaxiccid=(maxiccid)
        fmm.searchSave.click()
        sleep(2)
        text = int(fmm.ss_count.text)

        sql='''SELECT count(iccid) FROM `t_card_store` where iccid BETWEEN '%s' and '%s'
        '''
        data=(miniccid,maxiccid)
        count = mq.execQuery(sql % data)

        assert text == count[0][0]

    def test_create_time(self,browser,login_m):
        '''
        高级搜索--发卡时间
        '''
        fct = FlowCardManage(browser)

        fct.card_manage.click()
        fct.flow_card_manage.click()
        fct.supersearch.click()
        # 设置发卡开始时间
        fct.ss_ctstart.click()
        fct.ss_act_year.click()
        fct.ss_set_year_2019.click()
        fct.ss_act_month.click()
        fct.ss_set_month_12.click()
        fct.ss_set_day_27.click()

        # 设置发卡结束时间
        fct.ss_ctend.click()
        fct.se_act_year.click()
        fct.ss_set_year_2020.click()
        fct.ss_act_month.click()
        fct.ss_set_month_01.click()
        fct.ss_set_day_04.click()
        fct.searchSave.click()


        sql = '''SELECT count(iccid) FROM `t_card_store` where create_time BETWEEN '2019-12-27 00:00:00' and '2020-01-04 23:59:59'
                '''
        count = mq.execQuery(sql)

        text = int(fct.ss_count.text)

        assert text == count[0][0]



    def test_activetime(self,browser,login_m):
        '''
        高级搜索--激活时间
        '''
        fac=FlowCardManage(browser)
        fac.card_manage.click()
        fac.flow_card_manage.click()
        fac.supersearch.click()
        #设置激活开始时间
        fac.ss_atstart.click()
        fac.ss_act_year.click()
        fac.ss_set_year_2019.click()
        fac.ss_act_month.click()
        fac.ss_set_month_12.click()
        fac.ss_set_day_27.click()

        #设置激活结束时间
        fac.ss_atend.click()
        fac.se_act_year.click()
        fac.ss_set_year_2020.click()
        fac.ss_act_month.click()
        fac.ss_set_month_01.click()
        fac.ss_set_day_04.click()

        fac.searchSave.click()

        text = int(fac.ss_count.text)

        sql='''SELECT count(iccid) FROM `t_card_store` where activate_time BETWEEN '2019-12-27 00:00:00' and '2020-01-04 23:59:59'
        '''
        count = mq.execQuery(sql)

        assert text==count[0][0]

    def test_stoptime(self,browser,login_m):
        '''
        高级搜索--到期时间
        '''
        fst = FlowCardManage(browser)
        fst.card_manage.click()
        fst.flow_card_manage.click()
        fst.supersearch.click()
        # 设置到期开始时间
        fst.ss_ststart.click()
        fst.ss_act_year.click()
        fst.ss_set_year_2019.click()
        fst.ss_act_month.click()
        fst.ss_set_month_12.click()
        fst.ss_set_day_27.click()

        # 设置到期结束时间
        fst.ss_stend.click()
        fst.se_act_year.click()
        fst.ss_set_year_2020.click()
        fst.ss_act_month.click()
        fst.ss_set_month_01.click()
        fst.ss_set_day_04.click()

        fst.searchSave.click()
        sleep(2)

        text = int(fst.ss_count.text)

        sql = '''SELECT count(iccid) FROM `t_card_store` where stop_time BETWEEN '2019-12-27 00:00:00' and '2020-01-04 23:59:59'
                '''
        count = mq.execQuery(sql)
        assert text == count[0][0]



    @pytest.mark.parametrize(
        " share, share_sql,settlement,settlement_sql",
        [("独享卡","1", "月结日结算","1"),
         ("共享卡","2", "激活日结算","2"),
         ],
        ids=["1+1", "2+2"])
    def test_share_settlementType(self,browser,login_m,share,share_sql,settlement,settlement_sql):
        '''
        高级搜索--共享类型 和 结算类型
        '''
        fss = FlowCardManage(browser)
        fss.card_manage.click()
        fss.flow_card_manage.click()
        fss.supersearch.click()
        # 选择共享类型
        Select(fss.ss_shareType).select_by_visible_text(share)
        Select(fss.ss_settlementType).select_by_visible_text(settlement)
        fss.searchSave.click()
        sleep(2)

        text = int(fss.ss_count.text)
        sql = '''SELECT count(iccid) FROM `t_card_store` where share_type='%s' and settlement_type = '%s'
              '''
        data = (share_sql,settlement_sql)
        count = mq.execQuery(sql % data)

        assert text == count[0][0]


    def test_mark(self,browser,login_m):
        '''
        高级搜索--备注关键字查询
        '''
        fsm = FlowCardManage(browser)
        fsm.card_manage.click()
        fsm.flow_card_manage.click()
        fsm.supersearch.click()
        fsm.ss_mark=('自动化test')
        fsm.searchSave.click()

        text = int(fsm.ss_count.text)

        sql = '''SELECT	count( iccid ) FROM	`t_card_store` WHERE	remark LIKE "%自动化test%"
              '''

        count = mq.execQuery(sql )

        assert text == count[0][0]


class TestCardExport:
    '''
    流量卡管理导出功能
    '''
    def test_export(self,login_m,browser):
        '''
        流量卡管理--导出
        '''
        file_path = r'E:\yuxichen\Product\test_dir\data\down_file'

        fe = FlowCardManage(browser)
        #卡片管理
        fe.card_manage.click()
        fe.flow_card_manage.click()

        #导出按钮
        fe.export.click()
        sleep(2)

        #找出多少条数据
        text = int(fe.ss_count.text)

        #查找下载文件有多少条数据
        list = os.listdir(file_path)
        file = os.path.join(file_path,list[-1])
        bk=we.read_excel(file)
        st=bk.sheet_by_name("Sheet0")
        allline = st.nrows

        assert allline-1 == text


class TestOrder:
    '''
    套餐订购
    '''
    def test_resetbag(self,browser,login_m):
        '''
        重置套餐
        '''
        frb = FlowCardManage(browser)
        frb.card_manage.click()
        frb.flow_card_manage.click()
        frb.searchiccid=('89860619050008947664')
        frb.search.click()
        frb.gouxuankuang.click()
        frb.resetbag.click()
        frb.resetbagsave.click()

        sql = '''select count(iccid) from t_bag_iccid where iccid = '89860619050008947664'
                '''
        count = mq.execQuery(sql)
        assert count[0][0] == 0


    def test_order_1(self,browser,login_m):
        '''
        套餐订购--续订生效--单张卡片
        '''
        #先接口停用卡片
        data_stop={
            "iccid":"89860619050008947664",
            "method":"sohan.m2m.iccid.deactivate",
            "sign":"84FB4DAF697852EDD74E778137EA53D8",
            "timestamp":"1578385382980",
            "username":"客户演示"
        }
        try:
            res_stop=api.ask_699(data_stop)
            print('调用停卡接口成功~~~~ %s' % (res_stop.get('errorCode')))
        except:
            print('接口调用失败！！！！')


        fob = FlowCardManage(browser)
        fob.card_manage.click()
        fob.flow_card_manage.click()
        fob.searchiccid=(data_stop.get('iccid'))
        fob.search.click()
        sleep(1)
        #勾选第一张卡片89860619050008947664
        fob.gouxuankuang.click()
        #查询该卡现在是否存在生效套餐
        sql='''select count(iccid) from t_bag_iccid where iccid = '%s'
        '''
        data=(data_stop.get('iccid'))
        count = mq.execQuery(sql % data)
        print('该卡当前存在%s个套餐' % count[0])
        print(type(count[0][0]))

        retry = 2
        while count[0][0]:
            #重置套餐
            fob.resetbag.click()
            fob.resetbagsave.click()
            fob.gouxuankuang.click()
            count = mq.execQuery(sql % data)
            retry-=1

        #开始给该卡（无套餐，停用）上套餐
        fob.searchcustomer1.click()
        fob.searchcustomer3.click()
        fob.orderbag.click()
        Select(fob.osourcetype).select_by_value("1")
        fob.obag.click()
        fob.ochosebag.click()
        Select(fob.ochosenum).select_by_value('1')
        fob.osavebag.click()
        sleep(5)
        fob.gouxuankuang.click()
        fob.reflesh.click()

        #先看104有没有生效套餐
        count1 = mq.execQuery(sql % data)
        assert count1[0][0] == 1


        #调用单个卡片查询接口检查是否激活(实际上返回的也是104数据库的字段值)
        data_qc={"iccid":"89860619050008947664",
                            "method":"sohan.m2m.iccidinfo.queryone",
                            "sign":"E0469BBE55C252734E9EFA82A8F0CDAD",
                            "timestamp":"1578553270141",
                            "username":"一级客户"
                            }
        try:
            res_query = api.ask_104(data_qc)
            print('调用查询接口成功~~~~ %s' % (res_query.get('errorCode')))
            dict = res_query.get("data")
            result = dict.get('cardStatus')
            assert result == '2'
        except:
            print('接口调用失败！！！！')



        # dict = res_query.get("data")
        # print(dict.get('cardStatus'))
        #
