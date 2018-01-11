import requests
from bs4 import BeautifulSoup


class geetestCrawler(object):

    def __init__(self):
        self.req=requests.session()
        self.req.headers={'user-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/39.0.2171.71 Safari/537.36"}

    def getRequest(self):
        content=self.req.get("http://www.geetest.com/exp.html",timeout=6).text
        print("content--->"+content)



if __name__=="__main__":
    gee=geetestCrawler()
    print("------start--------")
    gee.getRequest()
    print(gee.req.cookies)
