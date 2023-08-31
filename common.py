import loginDriver


# 登录
def login(url, safecode, username, password):
    loginDriver.redirectLoginPage(url, safecode)
    loginDriver.choiceLink()
    loginDriver.login(username, password)


# 获取报告链接前缀
def getReportUrl(terminalType):
    return loginDriver.getReportUrl(terminalType)


# 获取数据 betTypeId A-1 B-2
def getData(reportUrl, betTypeId, terminalType):
    reportUrlByParam = loginDriver.getUrlByParam(reportUrl, betTypeId, terminalType)
    return loginDriver.getData(reportUrlByParam)


# 1
url_1 = "https://***/Navigation/NavigateByTarget"
safecode_1 = ""
username_1 = ""
password_1 = ""
terminalType_1 = 1

# 2
url_2 = "https://***/Navigation/NavigateByTarget"
safecode_2 = ""
username_2 = ""
password_2 = ""
terminalType_2 = 2

#  A-1 B-2
betTypeId_A = "1"
betTypeId_B = "2"

# 数据
data = []

# 登录1
login(url_1, safecode_1, username_1, password_1)
# 获取报告链接前缀
reportUrl = getReportUrl(terminalType_1)
print("1提数")
# A
print("1-A")
data.append(getData(reportUrl, betTypeId_A, terminalType_1))
# B
print("1-B")
data.append(getData(reportUrl, betTypeId_B, terminalType_1))

# 登录2
login(url_2, safecode_2, username_2, password_2)
# 获取报告链接前缀
reportUrl = getReportUrl(terminalType_2)
print("2提数")
# A
print("2-A")
data.append(getData(reportUrl, betTypeId_A, terminalType_2))
# B
print("2-B")
data.append(getData(reportUrl, betTypeId_B, terminalType_2))

print("-------------------------------------------------------------------------------------")
print("汇总如下")
print("1-A")
print(data[0])
print("1-B")
print(data[1])
print("2-A")
print(data[2])
print("2-B")
print(data[3])
print("-------------------------------------------------------------------------------------")

# total=zeros(49, dtype=int)
total = []
addTotal = []
a = 1
while a <= 49:
    total.append(0)
    addTotal.append(0)
    a += 1

for d in data:
    for index in range(len(d)):
        total[index] += d[index]

sum = 0
minNum = 9999999999999
for num in total:
    sum += num

for index in range(len(total)):
    addTotal[index] = sum - total[index]
    minNum = min(minNum, addTotal[index])

for index in range(len(addTotal)):
    addTotal[index] -= minNum

print("最小值: ", minNum)
print("原金额")
print(total)
print("反算后金额")
print(addTotal)