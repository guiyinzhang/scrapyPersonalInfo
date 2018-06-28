#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

__author__ = 'zhangguiyin'
import scrapy
from selenium import webdriver
import time
import re
from urllib import parse
from selenium.webdriver.support import expected_conditions as EC
from urllib import request
import http.cookiejar
from pyquery import PyQuery as pq


class PersonalPageSpider(scrapy.spiders.Spider):
    name = "personalPage"
    start_urls = [
        "https://ehire.51job.com/InboxResume/InboxRecentEngine.aspx"
    ]
    reBirth = re.compile("\（(.*)\）")
    reWorkTime = re.compile("(.*)年")

    def parse(self, response):
        login = webdriver.Chrome(executable_path='/soft/python3.5/bin/chromedriver')
        # login
        login.get("https://ehire.51job.com/MainLogin.aspx")
        login.implicitly_wait(1)
        time.sleep(2)
        login.find_element_by_name("txtMemberNameCN").clear()
        login.find_element_by_name("txtMemberNameCN").send_keys("比特信安")  # 修改为自己的用户名
        login.find_element_by_name("txtUserNameCN").clear()
        login.find_element_by_name("txtUserNameCN").send_keys("btxa241")  # 修改为自己的密码
        login.find_element_by_name("txtPasswordCN").clear()
        login.find_element_by_name("txtPasswordCN").send_keys("btxa@123")  # 修改为自己的密码
        # login.maximize_window()

        while (True):
            result = input("please input verify code. Y/N ?")
            if result is "Y" or len(result) == 0:
                break
        login.find_element_by_id("Login_btnLoginCN").click()
        while (True):
            result = input("please input verify code. Y/N ?")
            if result is "Y" or len(result) == 0:
                break

        login.execute_script('window.open("%s");' % self.start_urls[0])
        handles = login.window_handles
        for handle in handles:
            if handle != login.current_window_handle:
                print("--------------------->" + handle)
                login.switch_to_window(handle)
                break

        # login.execute_script(
        #     '$("#ctlSearchInboxEngine1_hid_funtype_search").val("$计算机软件|0100$互联网/电子商务/网游|2500$IT-品管、技术支持及其它|2700$")')
        # login.find_element_by_xpath("/html/body/form/div[2]/div/div[3]/div/div/dl[4]/dd/div[1]/a").click()
        # login.find_element_by_xpath('//*[@id="divdrop-posttime"]/div/a[5]').click()
        time.sleep(3)
        cookies = login.get_cookies()
        while (True):
            result = input("please input verify code. Y/N ?")
            if result is "Y" or len(result) == 0:
                break

        domain = "https://ehire.51job.com"
        while (True):
            # old = login.find_element_by_css_selector('.Search_page-numble > a.active::text').extract()
            # print("--------------------------------->" + old)
            users = login.find_elements_by_xpath('//a[@class="a_username"]')
            print(users)
            for user in users:
                href = user.get_attribute("href")
                time.sleep(1)
                yield Request(url=parse
                              .urljoin(domain, href), cookies=cookies, callback=self.parse_detail)
            time.sleep(5)

            login.find_element_by_id("pagerBottomNew_nextButton").click()
            last = login.find_element_by_id("pagerBottomNew_btnNum_ma").get_attribute("class")
            if last == "active":
                break

            # new = login.find_element_by_css_selector('.Search_page-numble > a.active::text').extract()
            # if str(old) is str(new):
            #     break

    def parse_detail(self, response):
        jq = pq(response.body)
        item = {"birth": "", "workTime": "", "sex": ""}
        jq(".name").children("span").remove()
        name = jq(".name").text()
        if 0 == len(name.strip()):
            while (True):
                result = input("please input verify code. Y/N ?")
                if result is "Y" or len(result) == 0:
                    break
            return

        maritalStatus = jq(
            "table.box:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)").text()
        phone = jq(".infr  > tr:nth-child(2) > td:nth-child(2)").text()
        email = jq(".blue").text()
        income = jq(".f16").text()
        salaryExpectation = jq(
            "table.box:nth-child(2) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)").html()
        major = jq(
            ".box2 > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > table:nth-child(1) > tr:nth-child(2) > td:nth-child(2)").text()
        school = jq(
            ".box2 > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > table:nth-child(1) > tr:nth-child(3) > td:nth-child(2)").text()
        education = jq(
            ".box2 > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > table:nth-child(1) > tr:nth-child(4) > td:nth-child(2)").text()

        info = jq(".infr > tr:nth-child(3) > td:nth-child(1)").text().split("|")
        try:
            item["birth"] = self.reBirth.search(info[1]).group(1).strip()
        except (BaseException) as e:
            pass
        try:
            item["workTime"] = self.reWorkTime.search(info[3]).group(1).strip()
        except (BaseException) as e:
            pass
        try:
            item["sex"] = info[0]
        except (BaseException) as e:
            pass

        item["name"] = name
        item["maritalStatus"] = maritalStatus
        item["phone"] = phone
        item["email"] = email
        item["income"] = income
        item["salaryExpectation"] = salaryExpectation
        item["major"] = major
        item["school"] = school
        item["education"] = education

        print(item)
        return item
