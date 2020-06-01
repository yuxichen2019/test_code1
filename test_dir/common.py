# -*- coding: utf-8 -*- 
# 2019/12/25 18:09 
# Product
# Mysql.py 
# company

import pymysql,json,requests,xlrd


class Mysql:
    """
    对pymysql的简单封装
    """
    def __init__(self):
        self.host = '192.168.1.104'
        self.port = 3308
        self.user = "root"
        self.pwd = "sy666.com"
        self.db = "icms"

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymysql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8",serverTimezone="Hongkong")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def execQuery(self,sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

        调用示例：
                ms = MYSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
                resList = ms.ExecQuery("SELECT id,NickName FROM WeiBoUser")
                for (id,NickName) in resList:
                    print str(id),NickName
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        #查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def execNonQuery(self,sql):
        """
        执行非查询语句

        调用示例：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()


class W_excel:
    '''
    读取excel文件
    '''
    def get_some(self,file_path,x=1,y=0):
        self.x = x
        self.y = y
        self.file_path = file_path
        data = xlrd.open_workbook(self.file_path)
        table = data.sheets()[0]
        self.iccid = table.cell(self.x, self.y).value
        return self.iccid



    def read_excel(self,file_path):
        bk = xlrd.open_workbook(file_path)
        return bk
    #     #指定名字是'0'的sheet为st：
    #     st = bk.sheet_by_name(sheet)
    #     #看看st里面，有效数据的行数和列数：
    #     a=st.nrows
    #     b=st.ncols
    #     return a,b


class Api(object):
    '''
    接口类
    '''
    def ask_699(self,data):
        headers = {"Content-Type": "application/json"}
        url = 'http://192.168.6.99:7300/index/m2m/api/v1'
        data_json = json.dumps(data)
        res_str = requests.post(url=url, data=data_json, headers=headers)
        #转化为字典
        res=  eval(res_str.text)

        return res

    def ask_104(self,data):
        headers = {"Content-Type": "application/json"}
        url = 'http://192.168.1.104:7300/index/m2m/api/v1'
        data_json = json.dumps(data)
        res_str = requests.post(url=url, data=data_json, headers=headers)
        #转化为字典
        res=  eval(res_str.text)

        return res