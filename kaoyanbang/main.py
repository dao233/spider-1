#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/5 16:34
# @Author  : gao
# @File    : main.py
import time

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

cap = {
    "platformName": "Android",
    "deviceName": "127.0.0.1:52001",
    "platformVersion": "5.1.1",
    "appPackage": "com.tal.kaoyan",
    "appActivity": "com.tal.kaoyan.ui.activity.SplashActivity",
    "noReset": True
}

name = ""
pwd = ""

driver = webdriver.Remote("http://localhost:4723/wd/hub", cap)


def get_size():
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return (x, y)


try:
    # 是否跳过
    if WebDriverWait(driver, 3).until(
            lambda x: x.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/tv_skip']")):
        driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/tv_skip']").click()
except:
    pass

try:
    if WebDriverWait(driver, 3).until(lambda x: x.find_element_by_xpath(
            "//android.widget.EditText[@resource-id='com.tal.kaoyan:id/login_email_edittext']")):
        driver.find_element_by_xpath(
            "//android.widget.EditText[@resource-id='com.tal.kaoyan:id/login_email_edittext']").send_keys(name)
        driver.find_element_by_xpath(
            "//android.widget.EditText[@resource-id='com.tal.kaoyan:id/login_password_edittext']").send_keys(pwd)
        driver.find_element_by_xpath(
            "//android.widget.Button[@resource-id='com.tal.kaoyan:id/login_login_btn']").click()
except:
    pass

try:
    # 隐私协议
    if WebDriverWait(driver, 3).until(
            lambda x: x.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/tv_title']")):
        driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/tv_agree']").click()
        driver.find_element_by_xpath(
            "//android.support.v7.widget.RecyclerView[@resource-id='com.tal.kaoyan:id/date_fix']/android.widget.RelativeLayout[3]").click()
except:
    pass

# 点击研讯
if WebDriverWait(driver, 3).until(lambda x: x.find_element_by_xpath(
        "//android.support.v7.widget.RecyclerView[@resource-id='com.tal.kaoyan:id/date_fix']/android.widget.RelativeLayout[3]/android.widget.LinearLayout[1]/android.widget.ImageView[1]")):
    driver.find_element_by_xpath(
        "//android.support.v7.widget.RecyclerView[@resource-id='com.tal.kaoyan:id/date_fix']/android.widget.RelativeLayout[3]/android.widget.LinearLayout[1]/android.widget.ImageView[1]").click()

    l = get_size()

    x1 = int(l[0] * 0.5)
    y1 = int(l[1] * 0.75)
    y2 = int(l[1] * 0.25)

    # 滑动操作
    while True:
        driver.swipe(x1, y1, x1, y2)
        time.sleep(0.5)
