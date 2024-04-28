from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import numpy
import json
import time

def inputCookie():
    with open('./cookie/cookie.json') as f:
        d = json.load(f)
        for cookie in d['cookies']:
            driver.add_cookie({"name": cookie['name'], "value": cookie['value']})
    driver.refresh()

def clear(index):
    try:
        inputList = '//*[@inputmode="numeric"]'
        driver.find_elements(By.XPATH, inputList)[index].send_keys(Keys.BACK_SPACE)
        driver.find_elements(By.XPATH, inputList)[index].send_keys(Keys.BACK_SPACE)
        driver.find_elements(By.XPATH, inputList)[index].send_keys(Keys.BACK_SPACE)
        driver.find_elements(By.XPATH, inputList)[index].send_keys(Keys.BACK_SPACE)
    except:
        clear(index)

def enableDeep():
    try:
        deep = '//*[@type="checkbox"]'
        driver.find_element(By.XPATH, deep).click()
    except:
        time.sleep(1)
        enableDeep()

def openSetting():
    try:
        description = '//*[@data-name="legend-source-description"]'
        driver.find_elements(By.XPATH, description)[1].click()
        settings = '//*[@data-name="legend-settings-action"]'
        driver.find_element(By.XPATH, settings).click()
    except:
        time.sleep(1)
        openSetting()

def setValue(index, value):
    try:
        inputList = '//*[@inputmode="numeric"]'
        driver.find_elements(By.XPATH, inputList)[index].send_keys(str(value))
        ok = '//*[@data-name="submit-button"]'
        driver.find_element(By.XPATH, ok).click()
    except:
        time.sleep(1)
        setValue(index, value)

def generateReport():
    try:
        generate = '//*[@data-overflow-tooltip-text="Generate report "]'
        driver.find_element(By.XPATH, generate).click()
    except:
        generateReport()

def getReport():
    try:
        reportPath = '//*[@class="container-Yvm0jjs7"]'
        reportDatas = driver.find_element(By.XPATH, reportPath).find_elements(By.TAG_NAME, "div")
        rs = []
        for data in reportDatas:
            if "\n" in data.text and not (data.text[0].isdigit() or data.text[0] == "−"):
                dttext = data.text.replace("\n", "|")
                rs.append(dttext)
        return rs
    except:
        return None

def convertReportValue(str):
    strList = str.split('|')
    num = strList[len(strList)-1]
    num1 = num.replace(" ", "")
    num2 = num1.replace("%", "")
    num3 = num2.replace("−", "-")
    return float(num3)

def inputcheck(index, range1, range2, step):
    try:
        enableDeep()
        for value in numpy.arange(range1, range2, step):
            openSetting()
            clear(index)
            setValue(index, round(value, 1))
            generateReport()
            while True:
                report = getReport()
                if report is not None:
                    finalReport = [
                        str(round(value, 1)),
                        str(convertReportValue(report[0])),
                        str(convertReportValue(report[1])),
                        str(convertReportValue(report[2])),
                        str(convertReportValue(report[3])),
                        str(convertReportValue(report[4])),
                    ]
                    # replace with tab '	'
                    print (' '.join(finalReport))
                    break
                time.sleep(1)
    except Exception as err:
        print (err)

driver = webdriver.Chrome()
driver.get("https://in.tradingview.com/chart/dJi9t8CK/")
inputCookie()
time.sleep(5)

inputcheck(0, 1, 100, 1)
# inputcheck(1, 1, 100, 1)
# inputcheck(2, 1, 200, 1)
# inputcheck(3, 1, 100, 1)
# inputcheck(4, 1, 100, 1)
# inputcheck(5, 1, 100, 1)
# inputcheck(6, 1, 100, 1)
# inputcheck(7, 1, 100, 1)
# inputcheck(8, 1, 10, 0.1)
# inputcheck(9, 1, 50, 1)
# inputcheck(10, 1, 100, 1)
input('End!')
