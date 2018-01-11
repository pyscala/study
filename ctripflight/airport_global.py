import requests
from bs4 import BeautifulSoup


# 全球机场
class Airport:

    # 获取网页内容
    def getHtml(self, pageNo):
        html = 0
        try:
            url = "http://airportcode.911cha.com/list_" + str(pageNo).strip() + ".html"
            html = requests.get(url, timeout=10).text
        except Exception:
            print("爬取失败------->" + str(pageNo))

        return html


    # 解析网页内容提取机场信息
    def parseHtml(self, html):
        airportList = [];
        if html != 0:
            try:
                soup = BeautifulSoup(html, "html.parser")
                trs = soup.select("tr")
                for tr in trs[1:]:
                    try:
                        tds = tr.select("td")
                        cityName = tds[0].text
                        threeCode = tds[1].text
                        fourCode = tds[2].text
                        airportName = tds[3].text
                        englishCityName = tds[4].text
                        o = (cityName, threeCode, fourCode,airportName, englishCityName)
                        if o[1] != "":
                            airportList.append(o)
                    except Exception:
                        print("解析tr错误------->" + str(tr))
            except Exception :
                print("解析html错误----->" + html)

        return airportList


# -------mian--------
# air=Airport()
# db=Utils.getCon()
# start=Utils.logTime()
# for i in range(1,285):
#     h=air.getHtml(i)
#     ls=air.parseHtml(h)
#     print("page {0} ----> {1}".format(i,ls))
#     Utils.addAirportToMysql(db,ls)
# db.close()
# end =Utils.logTime()
# print("总用时 ----->{0}".format(str(end-start)))


