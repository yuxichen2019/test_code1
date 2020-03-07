# -*- coding: utf-8 -*- 
# 2019/12/19 11:24 
# Product
# test_add_customer.py 
# company


import sys
from time import sleep
import pytest
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from page.account_management_page import AccountManagement


#global driver


class TestCustomerList():
    '''
    客户列表
    '''

    @pytest.mark.parametrize(
        "cname, phone, city",
        [("pytest0001","15112342277","广东省"),
         ("pytest0002","15112342277","广东省")
         ],
        ids=["case1", "case2"]
    )
    def test_add_customer(self,browser,login_m,cname, phone, city):
        '''
        添加一级客户
        '''
        customer_list = []
        ag=AccountManagement(browser)
        sleep(2)
        ag.customer_list.click()
        sleep(1)
        ag.add_client.click()
        ag.input_cname=cname
        ag.input_phone=phone
        ag.input_city=city
        ag.customer_level.click()
        ag.customer_level_1.click()
        ag.pay_type.click()
        ag.after_pay.click()
        ag.save.click()
        all_text=ag.customer_text
        for i in all_text:
            customer_list.append(i.text)

        for j in customer_list:
            if cname in j:
                assert True
            else:
                assert False



if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_add_customer.py"])