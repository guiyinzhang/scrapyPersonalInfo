# -*- coding: utf-8 -*-

import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings


class ResumeinfospiderPipeline(object):
    def process_item(self, item, spider):
        return item


class PersonalInfoPipeline(object):
    """
    CREATE TABLE `personal_info` (
        name varchar(20),
        birth varchar(20),
        sex varchar(10),
        workTime varchar(10),
        maritalStatus varchar(10),
        phone  varchar(20),
        email  varchar(50),
        income  varchar(10),
        salaryExpectation  varchar(10),
        major  varchar(20),
        School  varchar(30),
        education  varchar(10)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

    "insert into personal_info(name ,birth ,sex ,workTime ,maritalStatus ,phone ,email ,income ,salaryExpectation ,major ,School ,education) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (item["name"] ,item["birth"] ,item["sex"] ,item["workTime"] ,item["maritalStatus"] ,item["phone"] ,item["email"] ,item["income"] ,item["salaryExpectation"] ,item["major"] ,item["School"] ,item["education"])
    """

    def process_item(self, item, spider):
        host = '172.16.192.35'
        db = 'btxa'
        port = 3306
        user = 'root'
        psd = 'btxa@123'
        charset = 'utf8'

        con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=charset, port=port)
        cue = con.cursor()
        print("mysql connect succes")
        try:
            cue.execute("insert into personal_info(name ,birth ,sex ,workTime ,maritalStatus ,phone ,email ,income ,salaryExpectation ,major ,school ,education) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                ,(item["name"], item["birth"], item["sex"], item["workTime"], item["maritalStatus"], item["phone"],
                  item["email"], item["income"], item["salaryExpectation"], item["major"], item["school"],
                  item["education"]))
            print("insert success")
        except Exception as e:
            print('Insert error:', e)
            con.rollback()
        else:
            con.commit()
        con.close()
        return item
