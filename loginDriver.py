from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from urllib import parse
from selenium.webdriver.common.keys import Keys
import urllib
import math
import re
import operator
import time
import json

driver={}
# 跳转登录线路选择页 url-登录链接 safeCode-安全码
def redirectLoginPage(url, safeCode):
    global driver
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200'
    }
    cap = DesiredCapabilities.PHANTOMJS
    for key, value in headers.items():
        cap['phantomjs.page.customHeaders.{}'.format(key)] = value
    driver = webdriver.PhantomJS(executable_path="phantomjs.exe", desired_capabilities=cap)
    driver.execute_script("""
            function post(path, params) {
            var form = document.createElement('form');
            form.action = path;

            for (var key in params) {
                if (params.hasOwnProperty(key)) {
                    var hiddenField = document.createElement('input');
                    hiddenField.type = 'hidden';
                    hiddenField.name = key;
                    hiddenField.value = params[key];

                    form.appendChild(hiddenField);
                }
            }

            document.body.appendChild(form);
            form.submit();
        }

        post(arguments[0], {'SafeCode':arguments[1]});
        """, url, safeCode)
    sleep(3)
    print("登录成功")

# 选取线路 跳转登录页
def choiceLink():
    global driver
    items = driver.find_elements_by_class_name("item")
    minItems = {}
    minTimes = 9999999
    # 寻找最佳线路
    for item in items:
        times = item.find_elements_by_class_name("line")[0].text
        times = re.findall(r'\d+', times)
        if len(times) == 0:
            print("超时")
            continue
        timesInt = int(times[0])
        print("耗时: ", timesInt, item)
        if operator.lt(timesInt, minTimes):
            minTimes = timesInt
            minItems = item

    # 找到网速最好的线路
    print("[已获得最佳线路, 耗时: ", minTimes, "]")
    # 检查是否获取网速 没获取就记得断开连接 打日志 TODO

    # 点击跳转登录界面
    minItems.find_element_by_tag_name("a").click()
    sleep(1)

# 登录
def login(username, password):
    global driver
    driver.find_element_by_id("Account").send_keys(username)
    Password = driver.find_element_by_id("Password").send_keys(password)
    driver.find_element_by_id("btn-submit").click()
    sleep(1)
    print("登录成功")
    # 检查是否登录跳转成功 TODO

# 拼接接口url 点击报表 点击分类账 获取前缀URL与开盘日期
def getReportUrl(terminalType):
    global driver
    # 点击报表
    header = driver.find_element_by_id("header")
    nav = header.find_element_by_id("nav")
    report={}
    if terminalType == 1:
        report = nav.find_element_by_name("report")
        report.find_element_by_tag_name("a").click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="report_index"]/form/table/tbody/tr[3]/td[2]/label[2]').click()
        driver.find_element_by_xpath('//input[@value="查询"]').click()
        sleep(1)
    if terminalType == 2:
        report = nav.find_element_by_name("summaryreport")
        report.find_element_by_tag_name("a").click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="summary_report_index"]/form/table/tbody/tr[3]/td[2]/label[2]').click()
        driver.find_element_by_xpath('//input[@value="查询"]').click()
        sleep(1)

    # 点击分类账

    print("查询成功")

    # 检查是否为分类账页面
    url = driver.current_url
    if url.find("ledger") == -1:
        print("url不是分类账的url，请排查问题")
    # exitApp()
    return url

# URL处理 BetTypeId 1-A 2-B terminalType 1-1 2-2
def getUrlByParam(url, betTypeId, terminalType):
    # 解析url 用户拼接 获取A的接口
    url = urllib.parse.unquote(url)

    # 截取域名 https://t5.tt700825.xyz/(S(ez2yh42lkazfhuy3kz0gdtp5))
    prefix = url.split("?")[0].split("/App")[0]

    # 截取时间参数 StartDt=2023-08-10+16:24:05&EndDt=2023-08-10+16:24:05
    param = url.split("?")[2].split("&")
    StartDtStr = param[0]
    EndDtStr = param[1]

    # 获取时间戳
    timeStr = str(time.time())
    timeArr = timeStr[:14].split(".")
    ts = timeArr[0] + timeArr[1]

    # 拼接url
    return prefix + getUrlTypeByTerminalType(terminalType) + StartDtStr + "&" + EndDtStr + "&Report=2&Action=ledger&PlayTypeId=1&BetTypeId=" + betTypeId + "&_=" + ts

def getUrlTypeByTerminalType(terminalType):
    if terminalType == 1:
        return "/Report/GetTopManagePlayGroup?"
    elif terminalType == 2:
        return "/ReportTopManage/GetReportTopManagePlayGroup?"
    else:
        print("Invalid")
        return "Invalid"

# 调用接口 获取数据
def getData(url):
    global driver
    driver.get(url)
    sleep(1)
    page =driver.page_source
    # 解析数据 SelfAward-占成
    data = driver.page_source.split("<html><head></head><body>")[1].split("</body></html>")[0]
    data = json.loads(data)["Data"]
    detailList = data["DetailList"]
    selfAwards = []
    for detail in detailList:
        selfAwards.append(round(detail["HigherHoldMoney"]))
    print(selfAwards)
    return selfAwards