import requests
import threading
import time
import pymysql
import datetime

import config
import ipDic
from lxml import html
from DBUtils.PooledDB import PooledDB
from config import DB_CONFIG


pool = PooledDB(pymysql,50,host=DB_CONFIG['dbIp'],user=DB_CONFIG['dbUser'],passwd=DB_CONFIG['dbPass'],db=DB_CONFIG['dbName'],port=3306,charset="utf8")

class SpiderIp(threading.Thread):

    def __init__(self, index, source, url = 0, ty = 0):
        super().__init__()
        self._index = index
        self._source = source
        self._url = url
        self._ty = ty

    def run(self):

        while True:

            spider = ipDic.Ip()
            spiders = spider.getip(self._index, self._url, self._ty)

            for s in spiders:
                enuip = 'http://' + s['ip'] + ":" + s['port']
                proxies = {
                   'http': enuip,
                   'https': enuip,
                }
                if self.checkIp(proxies):

                    self.save(s['ip'], s['port'])
                    

            time.sleep(config.SLEEP_TIME)

    def checkIp(self, proxies):

        index = 0

        while True:

            try:
                htm = requests.get('https://www.douban.com/',proxies=proxies,timeout=config.TIMEOUT, headers=config.HEADER)
            except Exception as e:
                index += 1
                if index > config.IP_NUM:
                    #print ('失败')
                    return False
            else:
                return True
        
    def save(self, ip, port):
        db = pool.connection()
        cursor = db.cursor()
        dt=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT IGNORE INTO %s(ip, pot, source, insterTime) VALUES ('%s', '%s', '%s', '%s')"%(DB_CONFIG['tbName'], ip, port, self._source, str(dt))
        print (sql)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()
        finally:
            db.close()

class DeleteIp(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):

        while True:

            self.delete()

            time.sleep(config.MAXTIME)

    def delete(self):
        db = pool.connection()
        cursor = db.cursor()
        sql = "DELETE FROM %s WHERE insterTime < '%s'"%(DB_CONFIG['tbName'], (datetime.datetime.now() - datetime.timedelta(minutes=(config.MAXTIME/60))).strftime('%Y-%m-%d %H:%M:%S'))
        print (sql)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()
        finally:
            db.close()


        


def startIp():

    for i in range(0,  28):
        s0 = SpiderIp(0,source='www.66ip.cn',url=i)
        s0.start()

    for i in range(1, 3):
        s1 = SpiderIp(1,source='www.kuaidaili.com', url=i)
        s1.start()

    s2s = [
        'nn',
        'nt',
    ]
    for s in s2s:
        s2 = SpiderIp(2,source='www.xicidaili.com',url=s)
        s2.start()

    for i in range(1,3):
        s3 = SpiderIp(3,source='www.ip181.com',url=i)
        s3.start()

    for i in range(1,5):
        s4 = SpiderIp(4,source='www.coobobo.com',url=i)
        s4.start()

    for i in range(5,8):

        for j in range(1,4):
            s5 = SpiderIp(i,source='www.nianshao.me',url=j)
            s5.start()

  
    s8 = SpiderIp(8,source='www.us-proxy.org')
    s8.start()

    s9 = SpiderIp(9,source='www.sslproxies.org')
    s9.start()

def deleteIp():

    delete = DeleteIp()
    delete.start()


if __name__ == '__main__':

    startIp()
    deleteIp()
    #print ((datetime.datetime.now() - datetime.timedelta(minutes=(config.MAXTIME/60))).strftime('%Y-%m-%d %H:%M:%S'))
    



    # s2 = SpiderIp(0,1)
    # s2.start()
    
    # i = ipDic.Ip()
    # a=i.getip(0,2)
    # print (a)

    #kuaidaili()
    #test()