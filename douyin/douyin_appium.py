#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/6 10:51
# @Author  : gao
# @File    : douyin_appium.py
import multiprocessing
import sys
import time
from selenium.webdriver.support.ui import WebDriverWait
from appium import webdriver

# desired_caps = {}
# desired_caps['platformName'] = 'Android'
# desired_caps['deviceName'] = '127.0.0.1:62001'
# desired_caps['platformVersion'] = '5.1.1'
# desired_caps['appPackage'] = 'com.ss.android.ugc.aweme'
# desired_caps['appActivity'] = 'com.ss.android.ugc.aweme.splash.SplashActivity'
# desired_caps['noReset'] = True
# desired_caps['unicodeKeyboard'] = True
# desired_caps['resetKeyboard'] = True
#
# driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)


def get_size(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return (x, y)


def handle_douyin(driver):
    while True:
        # 定位搜索框
        while WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath(
                "//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/afo']")):
            # 获取douyin_id进行搜索
            driver.find_element_by_xpath(
                "//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/afo']").send_keys('706942127')
            while driver.find_element_by_xpath(
                    "//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/afo']").text != '706942127':
                driver.find_element_by_xpath(
                    "//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/afo']").send_keys('706942127')
                time.sleep(0.1)
                break
            break
        # 点击搜索
        driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.ss.android.ugc.aweme:id/afr']").click()

        # 点击用户标签
        if WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath("//android.widget.TextView[@text='用户']")):
            driver.find_element_by_xpath("//android.widget.TextView[@text='用户']").click()

        # 点击头像
        if WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.support.v4.view.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View/android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/android.widget.ImageView[2]")):
            driver.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.support.v4.view.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View/android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/android.widget.ImageView[2]").click()
        # 点击粉丝按钮
        if WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("com.ss.android.ugc.aweme:id/aj1")):
            driver.find_element_by_id("com.ss.android.ugc.aweme:id/aj1").click()

        l = get_size(driver)
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.75)
        y2 = int(l[1] * 0.25)
        while True:
            if '没有更多了' in driver.page_source:
                break
            elif '还没有粉丝' in driver.page_source:
                break
            else:
                driver.swipe(x1, y1, x1, y2)
                time.sleep(0.5)

        driver.find_element_by_id("com.ss.android.ugc.aweme:id/n7").click()
        driver.find_element_by_id("com.ss.android.ugc.aweme:id/n7").click()
        driver.find_element_by_xpath(
            "//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/afo']").clear()


def handle_appium(device, port):
    caps = {}
    caps["platformName"] = "Android"
    caps["deviceName"] = device
    caps["platformVersion"] = "5.1.1"
    caps["appPackage"] = "com.ss.android.ugc.aweme"
    caps["appActivity"] = "com.ss.android.ugc.aweme.splash.SplashActivity"
    caps["noReset"] = True
    caps["unicodeKeyboard"] = True
    caps["resetKeyboard"] = True
    caps["udid"] = device

    driver = webdriver.Remote('http://localhost:'+str(port)+'/wd/hub', caps)

    try:
        # 点击搜索图标
        while WebDriverWait(driver, 20).until(lambda x: x.find_element_by_xpath(
                "//android.widget.LinearLayout[@resource-id='com.ss.android.ugc.aweme:id/aps']")):
            driver.find_element_by_xpath(
                "//android.widget.LinearLayout[@resource-id='com.ss.android.ugc.aweme:id/aps']").click()
            break
    except:
        print("找不到搜索按钮")

    handle_douyin(driver)

if __name__ == '__main__':
    m_list = []

    devices_list = ['127.0.0.1:52001', '127.0.0.1:52025']
    for device in range(len(devices_list)):
        port = 4723+2*device
        m_list.append(multiprocessing.Process(target=handle_appium, args=(devices_list[device], port)))

    for m in m_list:
        m.start()

    for m in m_list:
        m.join()
