
from poium import Page, PageElement, PageElements



class LoginPage(Page):
    login_user = PageElement(id_="lg_user_input", describe="用户名")
    login_passwd = PageElement(id_="lg_pw_input", describe="密码")
    login = PageElement(id_="login", describe="登录按钮")


    # 定位一组元素
    #search_result = PageElements(xpath="//div/h3/a", describe="搜索结果")
