#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from scrapy import Request

__author__ = 'zhangguiyin'
import scrapy
from selenium import webdriver
import time


class PersonalPageSpider(scrapy.spiders.Spider):
    name = "csdnPage"
    start_urls = [
        "https://blog.csdn.net/qq_37303226"
    ]

    def start_requests(self):
        driver = webdriver.Chrome(executable_path='/soft/python3.5/bin/chromedriver')
        driver.get('https://passport.csdn.net/account/login')
        time.sleep(1)
        driver.find_elements_by_class_name("login-code__open")[0].click()
        time.sleep(1)
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("18502899659")  # 修改为自己的
        time.sleep(1)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("Gyz@123456")  # 修改为自己的密码
        # time.sleep(1)
        # driver.find_element_by_id("rememberMe").click()
        # while (True):
        #     result = input("please input verify code. Y/N ?")
        #     if result is "Y":
        #         break
        urlpase
        driver.find_element_by_class_name("logging").click()
        cookies = driver.get_cookies()
        driver.close()

        self.driver2 = webdriver.Chrome(executable_path='/soft/python3.5/bin/chromedriver')
        self.driver2.get(self.start_urls[0])

        return [Request(self.start_urls[0], cookies=cookies, callback=self.parse)]

    def parse(self, response):
        # print(response, type(response))
        # from scrapy.http.response.html import HtmlResponse
        # print(response.body_as_unicode())
        time.sleep(1)
        print("----------------->")
        print(self.driver2.find_element_by_xpath('//div[@id="mainBox"]').get_attribute("class"))
        print("----------------->")
        while (True):
            result = input("please input verify code. Y/N ?")
            if result is "Y" or len(result) == 0:
                break

        self.driver2.close()

        current_url = response.url  # 爬取时请求的url
        body = response.body  # 返回的html
        print(str(body.decode("utf-8")))
        unicode_body = response.body_as_unicode()  # 返回的html unicode编码
