#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from scrapy import Request

__author__ = 'zhangguiyin'
import scrapy
from selenium import webdriver
import time
import re
from urllib import parse


class PersonalPageSpider(scrapy.spiders.Spider):
    name = "personalPage"
    start_urls = [
        "https://ehire.51job.com/InboxResume/InboxRecentEngine.aspx"
    ]
    reBirth = re.compile("\（(.*)\）")
    reWorkTime = re.compile("(.*)年")

    # @property
    # def start_requests(self):
    #     login = webdriver.Chrome(executable_path='/soft/python3.5/bin/chromedriver')
    #     # login
    #     login.get("https://ehire.51job.com/MainLogin.aspx")
    #     login.implicitly_wait(1)
    #     time.sleep(2)
    #     login.find_element_by_name("txtMemberNameCN").clear()
    #     login.find_element_by_name("txtMemberNameCN").send_keys("比特信安")  # 修改为自己的用户名
    #     login.find_element_by_name("txtUserNameCN").clear()
    #     login.find_element_by_name("txtUserNameCN").send_keys("btxa241")  # 修改为自己的密码
    #     login.find_element_by_name("txtPasswordCN").clear()
    #     login.find_element_by_name("txtPasswordCN").send_keys("btxa@123")  # 修改为自己的密码
    #     # login.maximize_window()
    #
    #     while (True):
    #         result = input("please input verify code. Y/N ?")
    #         if result is "Y" or len(result) == 0:
    #             break
    #     login.find_element_by_id("Login_btnLoginCN").click()
    #     cookies = login.get_cookies()
    #     while (True):
    #         result = input("please input verify code. Y/N ?")
    #         if result is "Y" or len(result) == 0:
    #             break
    #
    #
    #     login.execute_script('window.open("%s");' % self.start_urls[0])
    #     handles = login.window_handles
    #     for handle in handles:
    #         if handle != login.current_window_handle:
    #             print("--------------------->" + handle)
    #             login.switch_to_window(handle)
    #             break
    #
    #
    #     login.execute_script(
    #         '$("#ctlSearchInboxEngine1_hid_funtype_search").val("$计算机软件|0100$互联网/电子商务/网游|2500$IT-品管、技术支持及其它|2700$")')
    #     login.find_element_by_xpath("/html/body/form/div[2]/div/div[3]/div/div/dl[4]/dd/div[1]/a").click()
    #     time.sleep(2)
    #     while (True):
    #         result = input("please input verify code. Y/N ?")
    #         if result is "Y" or len(result) == 0:
    #             break
    #
    #     index = 0
    #     reqs = []
    #     domain = "https://ehire.51job.com"
    #     while (index < 1):
    #         index += 1
    #         users = login.find_element_by_xpath('//*[@id="trBaseInfo_1"]/td[3]/ul/li[1]/a').get_attribute("href")
    #         print(users)
    #         for user in users:
    #             href = user.get_attribute("href")
    #             url = domain + href
    #             print("--------------+>" + url)
    #             req = Request(url=url, cookies=cookies, callback=self.parse)
    #             req.meta['parse'] = True
    #             reqs.append(req)
    #         time.sleep(5)
    #         login.find_element_by_id("pagerBottomNew_nextButton").click()
    #
    #     return reqs

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
        login.find_element_by_name("txtPasswordCN").send_keys("xxxxxx")  # 修改为自己的密码
        # login.maximize_window()

        while (True):
            result = input("please input verify code. Y/N ?")
            if result is "Y" or len(result) == 0:
                break
        login.find_element_by_id("Login_btnLoginCN").click()
        cookies = login.get_cookies()
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

        login.execute_script(
            '$("#ctlSearchInboxEngine1_hid_funtype_search").val("$计算机软件|0100$互联网/电子商务/网游|2500$IT-品管、技术支持及其它|2700$")')
        login.find_element_by_xpath("/html/body/form/div[2]/div/div[3]/div/div/dl[4]/dd/div[1]/a").click()
        time.sleep(2)
        while (True):
            result = input("please input verify code. Y/N ?")
            if result is "Y" or len(result) == 0:
                break

        index = 0
        domain = "https://ehire.51job.com"
        while (True):
            index += 1
            users = login.find_elements_by_xpath('//a[@class="a_username"]')
            print(users)
            for user in users:
                href = user.get_attribute("href")
                req = Request(url=parse.urljoin(domain, href), cookies=cookies, callback=self.parse_detail)
                req.meta['parse'] = True
                yield req
            time.sleep(5)
            login.find_element_by_id("pagerBottomNew_nextButton").click()

    def parse_detail(self, response):
        item = {}
        name = "#divResume > tbody > tr > td > table:nth-child(4) > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table.box1 > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(1) > td.name"
        maritalStatus = "#divInfo > td > table:nth-child(1) > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td.txt2"
        phone = "#divResume > tbody > tr > td > table:nth-child(4) > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table.box1 > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(2) > td:nth-child(2)"
        email = "#divResume > tbody > tr > td > table:nth-child(4) > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table.box1 > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(2) > td:nth-child(3) > table > tbody > tr > td.m_com > a"
        income = "#divInfo > td > table:nth-child(2) > tbody > tr:nth-child(1) > td > span.f16"
        salaryExpectation = "#divInfo > td > table:nth-child(3) > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td:nth-child(1) > table > tbody > tr > td.txt2"
        major = "#divResume > tbody > tr > td > table:nth-child(4) > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table.box2 > tbody > tr > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(2) > td.txt2"
        School = "#divResume > tbody > tr > td > table:nth-child(4) > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table.box2 > tbody > tr > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(3) > td.txt2"
        education = "#divResume > tbody > tr > td > table:nth-child(4) > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table.box2 > tbody > tr > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(4) > td.txt2"
        info = "#divResume > tbody > tr > td > table:nth-child(4) > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table.box1 > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(3) > td"

        name = response.css(name).text()
        maritalStatus = response.css(maritalStatus).text()
        phone = response.css(phone).text()
        email = response.css(email).text()
        income = response.css(income).text()
        salaryExpectation = response.css(salaryExpectation).text()
        major = response.css(major).text()
        School = response.css(School).text()
        education = response.css(education).text()

        info = response.css(info).text()
        info = info.strip().split("|")

        birth = self.reBirth.search(info[1]).group(1).strip()
        sex = info[0]
        workTime = self.reWorkTime.search(info[1]).group(3).strip()

        item["name"] = name
        item["maritalStatus"] = maritalStatus
        item["phone"] = phone
        item["email"] = email
        item["income"] = income
        item["salaryExpectation"] = salaryExpectation
        item["major"] = major
        item["School"] = School
        item["education"] = education
        item["birth"] = birth
        item["sex"] = sex
        item["workTime"] = workTime

        print(item)
        return item
