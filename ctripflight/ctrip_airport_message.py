import re

import requests
from bs4 import BeautifulSoup

import Utils as Utils


# 全球机场
class Airport:
    # 简单配置Header
    def Headers(self):
        return {
            "Host": 'flights.ctrip.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        }
    session = requests.session()

    # 获取网页内容
    def getFirstHtml(self):
        html = 0
        try:
            url = 'http://flights.ctrip.com/actualtime'
            html = self.session.get(url, headers=self.Headers(), timeout=10).content.decode('GBK')
            # print(html)
        except Exception as err:
            print(url + "爬取失败------->" + str(err))
        return html

    # 模拟请求查航班信息
    def getSecondHtml(self):
        html = 0
        searchKey = 0
        try:
            url = 'http://flights.ctrip.com/actualtime/BJS_PEK-SHA_PVG/t20170911'
            html = self.session.get(url, headers=self.Headers(), timeout=10).content.decode('GBK')
            soup = BeautifulSoup(html, 'html.parser')
            script = soup.select("script")[3].text
            search = re.search("SearchKey\":\"(.*)\"}'", script)
            if search != None:
                searchKey = search.group(1)
                print(searchKey)
            url='https://accounts.ctrip.com/member/ajax/AjaxGetCookie.ashx?jsonp=BuildHTML&r=0.35096247353868604&encoding=0'
            h=requests.get(url,headers=self.Headers(),timeout=10)
            print(h.text)
        except Exception as err:
            print(url + "爬取失败------->" + str(err))

        return (url, searchKey)

    # 模拟请求查航班详情
    def getThirdHtml(self, ms):
        headers={
            "Host": 'flights.ctrip.com',
            'Connection': 'keep-alive',
            'Referer':'flights.ctrip.com/actualtime/BJS_PEK-SHA_PVG/t20170911',
            'Accept':'*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        }
        html = 0
        if ms[1] != 0:
            try:
                url = """http://flights.ctrip.com/process/FlightStatus/FindByCityWithJson?from=BJS_PEK&to=SHA_PVG&
                date=20170911&
                searchKey=""" + ms[1]
                print(url)
                html = self.session.get(url, headers=self.Headers(), timeout=10).content.decode('GBK')
                print(html)

            except Exception as err:
                print(url + "爬取失败------->" + str(err))
        return html

    # 解析网页内容提取机场信息
    def parseHtml(self, html):
        return 0


# -------start--------
start = Utils.logTime()

air = Airport()
# db=Utils.getCon()
air.getFirstHtml()
key=air.getSecondHtml()
air.getThirdHtml(key)
# --------end---------
end = Utils.logTime()
print("总用时 ----->{0}".format(str(end - start)))
