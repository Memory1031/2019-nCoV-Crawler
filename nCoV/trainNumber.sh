#! /bin/sh
export PATH=$PATH:/usr/local/bin

cd /home/2019-nCoV-Crawler

nohup scrapy crawl Tencent >> Tencent.log 2>&1 &
nohup scrapy crawl Community >> Community.log 2>&1 &