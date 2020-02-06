# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class NcovPipeline(object):
    def __init__(self):
        # 打开数据库连接
        self.fb = open("application.txt", "r", encoding="utf8")
        self.db = MySQLdb.connect(self.fb.readline().strip(), self.fb.readline().strip(), self.fb.readline().strip(),
                                  "nCov", charset='utf8')
        self.fb.close()

    def process_item(self, item, spider):
        getTime = item['date'][:10]

        cursor = self.db.cursor()
        cursor.execute("select * from dataFromTencent_dev where id = 1")
        latestUpdate = cursor.fetchone()[3]
        cursor.close()

        if latestUpdate.__format__('%Y-%m-%d') != getTime:
            cursorTime = self.db.cursor()
            cursorTime.execute(
                "UPDATE dataFromTencent_dev SET date = '%s' WHERE 'provinceName' = 'latestUpdate'" % (getTime))
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
                            "UPDATE dataFromTencent_dev SET totalConfirm = %d, totalSuspect = %d, totalDead = %d, totalHeal = %d, todayConfirm = %d, todaySuspect = %d, todayDead = %d, todayHeal = %d WHERE cityName = '%s' and date = '%s'" \
                            % (totalConfirm, totalSuspect, totalDead, totalHeal, todayConfirm, todaySuspect, todayDead,
                               todayHeal, cityName, getTime))
                        self.db.commit()
                    else:
                        sql = "INSERT INTO dataFromTencent_dev (provinceName, cityName, date, totalConfirm, totalSuspect, totalDead, totalHeal, todayConfirm, todaySuspect, todayDead, todayHeal) VALUES ('%s', '%s', '%s', %d, %d, %d, %d, %d, %d, %d, %d)" \
                              % (provinceName, cityName, getTime, totalConfirm, totalSuspect, totalDead,
                                 totalHeal, todayConfirm, todaySuspect, todayDead, todayHeal)
                        cursorThen.execute(sql)
                        self.db.commit()
                        pass
                except:
                    print("与数据库交互失败！")
                    self.db.rollback()
                cursorThen.close()
        return item

    def close_spiders(self, spider):
        self.db.close()
