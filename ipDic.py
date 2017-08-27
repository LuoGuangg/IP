import requests
from lxml import html
import config


class Ip(object):
    def __init__(self):
        super().__init__()
        self._dris = config.WEB_IP

    #index = 0 1<url<34 -- index = 2 url==nn or nt --  index = 2 url==nn or nt 
    def getip(self, index, url = 0, ty = 0):
        d = self._dris[index]
        dic = []
        if url == 0:
            dic = self.getDic(d['url'], d, 'utf-8', ty)
        else:
            dic = self.getDic(d['url']%url, d, 'utf-8', ty)

        # if index == 3 or index == 0 and len(dic)>0:
        #     del dic[0]

        return dic

    def getDic(self, url, dri ,encoding, ty = 0):

        index = 0
        
        while True:
            try:
                if index > config.IP_NUM:
                    return

                request = requests.get(url,headers = config.HEADER, timeout = config.TIMEOUT)
            except Exception as e:
                index += 1
            else:
                break

        request.encoding = encoding

        #print (request.text)

        tree = html.fromstring(request.text)
        ips = tree.xpath(dri['ip'])
        ports = tree.xpath(dri['port'])

        listDirs = []

        for i, exp in enumerate(ips):

            if ty == 'coobobo':
                left = exp.find('(')
                right = exp.find(')')
                exp = str(exp)
                exp = exp[left+1:right]
                exp = exp.replace('\"',"").replace('+',"").replace('\'',"").replace(' ',"")

            dirs = {
                'ip': exp,
                'port': ports[i],
            }

            listDirs.append(dirs)

        return listDirs


# i = Ip()
# a=i.getip(9)
# print (a)
#https://www.proxynova.com/proxy-server-list/country-id/