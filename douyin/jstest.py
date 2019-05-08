#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/7 19:40
# @Author  : gao
# @File    : jstest.py

from selenium import webdriver

driver = webdriver.Chrome()
driver.get("file://E:\\Python\\Spider\\douyin\\test.html")
driver.close()