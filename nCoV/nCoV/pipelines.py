# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb


class NcovPipeline(object):
    def __init__(self):
        # 打开数据库连接
        self.fb = open("/home/spider/application.txt", "r")
        self.db = MySQLdb.connect(host=self.fb.readline().strip(), user=self.fb.readline().strip(),
                                  password=self.fb.readline().strip(), db="nCov",
                                  charset='utf8')
        self.fb.close()

    def process_item(self, item, spider):
        if spider.name == 'Tencent':
            getTime = item['date'][:10]

            cursor = self.db.cursor()
            cursor.execute("select * from dataFromTencent_dev where id = 1")
            latestUpdate = cursor.fetchone()[3]
            cursor.close()

            if latestUpdate.__format__('%Y-%m-%d') != getTime:
                print("New day. Life is fantasy.")
                cursorTime = self.db.cursor()
                cursorTime.execute(
                    "UPDATE dataFromTencent_dev SET date = '%s' WHERE Id = 1" % getTime)
                self.db.commit()
                cursorTime.close()

            for province in item['areaTree']:
                provinceName = province['name']
                print(provinceName)

                for city in province['children']:
                    cityName = city['name']
                    totalConfirm = city['total']['confirm']
                    totalSuspect = city['total']['suspect']
                    totalDead = city['total']['dead']
                    totalHeal = city['total']['heal']
                    todayConfirm = city['today']['confirm']
                    todaySuspect = city['today']['suspect']
                    todayDead = city['today']['dead']
                    todayHeal = city['today']['heal']

                    try:
                        cursorThen = self.db.cursor()
                        if latestUpdate.__format__('%Y-%m-%d') == getTime:
                            cursorThen.execute(
                                "UPDATE dataFromTencent_dev SET totalConfirm = %s, totalSuspect = %s, totalDead = %s, totalHeal = %s, todayConfirm = %s, todaySuspect = %s, todayDead = %s, todayHeal = %s WHERE cityName = '%s' and date = '%s'" \
                                % (
                                    totalConfirm, totalSuspect, totalDead, totalHeal, todayConfirm, todaySuspect,
                                    todayDead,
                                    todayHeal, cityName, getTime))
                            self.db.commit()
                            cursorThen.close()
                        else:
                            sql = "INSERT INTO dataFromTencent_dev (provinceName, cityName, date, totalConfirm, totalSuspect, totalDead, totalHeal, todayConfirm, todaySuspect, todayDead, todayHeal) VALUES ('%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s)" \
                                  % (provinceName, cityName, getTime, totalConfirm, totalSuspect, totalDead,
                                     totalHeal, todayConfirm, todaySuspect, todayDead, todayHeal)
                            cursorThen.execute(sql)
                            self.db.commit()
                            cursorThen.close()
                    except:
                        print("与数据库交互失败！")
                        self.db.rollback()
        elif spider.name == "Community":
            cursor = self.db.cursor()
            cursor.execute("select * from communityData where full_address = '%s'" % item['full_address'])
            latestUpdate = cursor.fetchone()
            if latestUpdate is None:
                insertSql = "INSERT INTO communityData (province, city, district, county, street, community, show_address, full_address, cnt_inc_uncertain, cnt_inc_certain, cnt_inc_die, cnt_inc_recure, cnt_sum_uncertain, cnt_sum_certain, cnt_sum_die, cnt_sum_recure, lng, lat) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " % (
                    item['province'], item['city'], item['district'], item['county'], item['street'], item['community'],
                    item['show_address'], item['full_address'], item['cnt_inc_uncertain'], item['cnt_inc_certain'],
                    item['cnt_inc_die'], item['cnt_inc_recure'], item['cnt_sum_uncertain'], item['cnt_sum_certain'],
                    item['cnt_sum_die'], item['cnt_sum_recure'], item['lng'], item['lat'])
                cursor.execute(insertSql)
                self.db.commit()
            else:
                updateSql = "UPDATE communityData SET cnt_inc_uncertain = %s, cnt_inc_certain = %s, cnt_inc_die = %s, cnt_inc_recure = %s, cnt_sum_uncertain = %s, cnt_sum_certain = %s, cnt_sum_die = %s, cnt_sum_recure = %s WHERE id = %d" % (
                    item['cnt_inc_uncertain'], item['cnt_inc_certain'], item['cnt_inc_die'], item['cnt_inc_recure'],
                    item['cnt_sum_uncertain'], item['cnt_sum_certain'], item['cnt_sum_die'], item['cnt_sum_recure'],
                    latestUpdate[0])
                cursor.execute(updateSql)
                self.db.commit()
        return item

    def close_spiders(self, spider):
        self.db.close()
