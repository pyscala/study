# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

import Utils as Utils


# 全国机场
class Airport:

    # 获取网页内容
    def getHtml(self):
        html = 0
        try:
            url = "http://www.ip138.com/feijichang/"
            html = requests.get(url, headers=Utils.header(), timeout=10).content.decode("GBK")
            print(html)
        except Exception as err:
            print("爬取失败------->" + str(err))
        return html


    # 解析网页内容提取机场信息
    def parseHtml(self, html):
        airportList = [];
        if html != 0:
            try:
                soup = BeautifulSoup(html, "html.parser")
                trs = soup.find_all("table")[2].select("tr")
                province = ""
                for tr in trs[1:]:
                    try:
                        tds = tr.select("td")
                        if len(tds) == 1:
                            province = tds[0].select("b")[0].text

                        elif len(tds) == 10:
                            if len(tds[1].text) == 3:
                                # o = {
                                #     "threeCode": tds[1].text,
                                #     "name": tds[3].select("a")[0].text,
                                #     "fourCode": tds[2].text,
                                #     "city": tds[0].text,
                                #     "province": province,
                                #     "englishName": tds[4].text
                                # }
                                o = (
                                    tds[1].text,
                                    tds[3].select("a")[0].text,
                                    tds[2].text,
                                    tds[0].text,
                                    province,
                                    tds[4].text
                                )
                                airportList.append(o)

                            if len(tds[6].text) == 3:
                                # k = {
                                #     "threeCode": tds[1].text,
                                #     "name": tds[3].select("a")[0].text,
                                #     "fourCode": tds[2].text,
                                #     "city": tds[0].text,
                                #     "province": province,
                                #     "englishName": tds[4].text
                                # }
                                k = (
                                    tds[6].text,
                                    tds[8].select("a")[0].text,
                                    tds[7].text,
                                    tds[5].text,
                                    province,
                                    tds[9].text
                                )
                                airportList.append(k)
                    except Exception as err:
                        print("解析tr错误------->" + str(err))
            except Exception as err:
                print("解析html错误----->" + str(err))
        return airportList


# -------start--------
start = Utils.logTime()

air = Airport()
db = Utils.getCon()
h = air.getHtml()
ls = air.parseHtml(h)
Utils.addAirportOfChinaToMysql(db, ls)
db.close()

# ------end----------
end = Utils.logTime()
print("总用时 ----->{0}".format(str(end - start)))
