import os
import pytest
from py.xml import html
from selenium import webdriver
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options as CH_Options
from selenium.webdriver.firefox.options import Options as FF_Options
from page.login_page import LoginPage
from time import sleep
import pymysql
from selenium.common.exceptions import NoSuchElementException

# 项目目录配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = BASE_DIR + "/test_report/"

############################
'''
fixture的作用范围（scope）

ixture里面有个scope参数可以控制fixture的作用范围：session>module>class>function

-function：每一个函数或方法都会调用

-class：每一个类调用一次，一个类中可以有多个方法

-module：每一个.py文件调用一次，该文件内又有多个function和class

-session：是多个文件调用一次，可以跨.py文件调用，每个.py文件就是module

'''

# 配置浏览器驱动类型(chrome/firefox/chrome-headless/firefox-headless)。
driver_type = "chrome"
# 配置运行的 URL
url = "http://192.168.1.104:7300/html/index.html"
# 失败重跑次数
rerun = "1"
# 当达到最大失败数，停止执行
max_fail = "3"
# 运行测试用例的目录或文件
cases_path = "./test_dir/"
############################

# 定义基本测试环境
@pytest.fixture(scope='function')
def base_url():
    global url
    global driver

# 设置用例描述表头
@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.pop()
# 设置用例描述表格
@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.pop()

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    用于向测试用例中添加用例的开始时间、内部注释，和失败截图等.
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = description_html(item.function.__doc__)
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            case_path = report.nodeid.replace("::", "_") + ".png"
            if "[" in case_path:
                case_name = case_path.split("-")[0] + "].png"
            else:
                case_name = case_path
            capture_screenshot(case_name)
            img_path = "image/" + case_name.split("/")[-1]
            if img_path:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % img_path
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
def description_html(desc):
    """
    将用例中的描述转成HTML对象
    :param desc: 描述
    :return:
    """
    if desc is None:
        return "No case description"
    desc_ = ""
    for i in range(len(desc)):
        if i == 0:
            pass
        elif desc[i] == '\n':
            desc_ = desc_ + ";"
        else:
            desc_ = desc_ + desc[i]

    desc_lines = desc_.split(";")
    desc_html = html.html(
        html.head(
            html.meta(name="Content-Type", value="text/html; charset=latin1")),
        html.body(
            [html.p(line) for line in desc_lines]))
    return desc_html
def capture_screenshot(case_name):
    """
    配置用例失败截图路径
    """
    #driver = webdriver.Chrome()
    global driver
    file_name = case_name.split("/")[-1]
    new_report_dir = new_report_time()
    if new_report_dir is None:
        raise RuntimeError('没有初始化测试目录')
    image_dir = os.path.join(REPORT_DIR, new_report_dir, "image", file_name)
    driver.save_screenshot(image_dir)
def new_report_time():
    """
    获取最新报告的目录名（即运行时间，例如：2018_11_21_17_40_44）
    """
    files = os.listdir(REPORT_DIR)
    files.sort()
    try:
        return files[-1]
    except IndexError:
        return None

# 启动浏览器
@pytest.fixture(scope='session', autouse=True)
def browser():
    """
    全局定义浏览器驱动
    :return:
    """
    global driver
    global driver_type


    if driver_type == "chrome":
        # 本地chrome浏览器
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0,  # 禁止弹出下载窗口
                 'download.default_directory': r'E:\yuxichen\Product\test_dir\data\down_file'}  # 设置下载路径
        options.add_experimental_option('prefs', prefs)

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()

    elif driver_type == "firefox":
        # 本地firefox浏览器
        driver = webdriver.Firefox()
        driver.maximize_window()

    elif driver_type == "chrome-headless":
        # chrome headless模式
        chrome_options = CH_Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--window-size=1920x1080")
        driver = webdriver.Chrome(options=chrome_options)

    elif driver_type == "firefox-headless":
        # firefox headless模式
        firefox_options = FF_Options()
        firefox_options.headless = True
        driver = webdriver.Firefox(firefox_options=firefox_options)

    elif driver_type == "grid":
        # 通过远程节点运行
        driver = Remote(command_executor='http://10.2.16.182:4444/wd/hub',
                        desired_capabilities={
                            "browserName": "chrome",
                        })
        driver.set_window_size(1920, 1080)

    else:
        raise NameError("driver驱动类型定义错误！")
    #driver=webdriver.Chrome()
    return driver


#登录
@pytest.fixture(scope='function')
def login_m(browser):
    global driver
    loginpage=LoginPage(browser)
    loginpage.get('http://192.168.1.104:7300/html/index.html')
    loginpage.login_user='admin'
    loginpage.login_passwd='123456'
    loginpage.login.click()
    sleep(1)
    first_page_m = driver.current_url
    assert base_url != first_page_m

def login_c(browser):
    global driver
    loginpage = LoginPage(browser)
    loginpage.get('http://192.168.1.104:6300/html/index_sohan.html')
    browser.implicitly_wait(10)
    loginpage.login_user = 'yjkh'
    loginpage.login_passwd = '123456'
    loginpage.login.click()
    sleep(1)
    first_page_c = driver.current_url
    assert base_url != first_page_c



# 关闭浏览器
@pytest.fixture(scope="session", autouse=True)
def browser_close():
    yield driver
    driver.quit()
    print("test end!")


# if __name__ == "__main__":
#     capture_screenshot("test_dir/test_baidu_search.test_search_python.png")
