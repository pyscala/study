import requests
import Utils
from bs4 import BeautifulSoup


class aihuishou(object):
    pass

    def __init__(self):
        self.session = requests.session()
        self.root_url = "http://www.aihuishou.com"
        self.root_url_shouji = "http://www.aihuishou.com/shouji?all=True"
        # 分类
        self.category = []
        # 品牌
        self.brand = []
        # 细分
        self.brands = []
        # 产品
        self.products = []
        # sku 组合
        self.sku_property_value_ids = []
        # product 选项
        self.product_select_property_tetail = []

        pass

    def get_ai_category(self):
        response = self.session.get(self.root_url_shouji, headers=Utils.header(), timeout=10)
        # print(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        category = soup.select("div.list-box")[0].select("dd")
        for cate in category:
            alink = cate.select("a")[0]
            # print(alink["href"])
            self.category.append({"category": alink.text, "url": self.root_url + alink["href"]})

    def get_ai_brand(self, category):
        if category is None:
            return None
        brands = []
        url = category["url"]
        response = self.session.get(url, timeout=10, headers=Utils.header())
        soup = BeautifulSoup(response.text, "html.parser")
        dds = soup.select("div.list-box")[1].select("dd")
        for dd in dds:
            alink = dd.select("a")[0]
            brands.append(
                {"category": category["category"], "brand": alink.text, "url": self.root_url + str(alink["href"])})
        return brands

    def get_ai_second_category(self, brand):
        brands = []
        for b in brand:

            cate = b["category"]
            url = b["url"]
            if cate == "摄影摄像" or cate == "智能数码":
                response = self.session.get(url, timeout=10, headers=Utils.header())
                soup = BeautifulSoup(response.text, "html.parser")
                lists = soup.select("div.list-box")
                if len(lists) == 3:
                    dds = lists[2].select("dd")
                    for dd in dds:
                        alink = dd.select("a")[0]
                        brands.append({"category": b["category"], "second_category": b["brand"], "brand": alink.text,
                                       "url": self.root_url + alink["href"]})
            else:

                d = {"category": b["category"], "second_category": b["category"], "brand": b["brand"],
                     "url": b["url"]}
                brands.append(d)
        self.brands = brands

    def print(self):

        print("------category-----")
        for i in range(0, len(self.category)):
            print(str(i) + "-----" + str(self.category[i]))

        # print("--------brand--------")
        # for i in range(0, len(self.brand)):
        #     print(str(i) + "-----" + str(self.brand[i]))

        print("--------brands--------")
        for i in range(0, len(self.brands[0:10])):
            print(str(i) + "-----" + str(self.brands[i]))

        print("--------products--------")
        for i in range(0, len(self.products)):
            print(str(i) + "-----" + str(self.products[i]))

        print("--------sku_property_value_ids--------")
        for i in range(0, len(self.sku_property_value_ids)):
            print(str(i) + "-----" + str(self.sku_property_value_ids[i]))

        print("--------product_select_property_tetail--------")
        for i in range(0, len(self.product_select_property_tetail)):
            print(str(i) + "-----" + str(self.product_select_property_tetail[i]))

    def get_ai_product(self, brand):
        if brand is None:
            return
        products = []
        url = brand["url"]
        response = self.session.get(url, headers=Utils.header(), timeout=10)
        print(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        lis = soup.select(".product-list-wrapper")[0].select("li");
        for li in lis:
            alink = li.select("a")[0]
            count = li.select("span")[0].text.replace('已有', '').replace('人回收', '')
            type = li.select("p")[0].text
            products.append(
                {"category": brand["category"], "second_category": brand["second_category"], "brand": brand["brand"],
                 "type": type, "simple_type": type.replace(' ', ''), "count": count,
                 "url": self.root_url + alink["href"],
                 "productId": alink["href"].replace("/product/", '').replace(".html", '')})
        return products

    def get_ai_product_test(self):
        brands = [
            {'category': '手机', 'second_category': '手机', 'brand': '苹果', 'url': 'http://www.aihuishou.com/shouji/b52'},
            {'category': '手机', 'second_category': '手机', 'brand': '三星', 'url': 'http://www.aihuishou.com/shouji/b7'},
            {'category': '手机', 'second_category': '手机', 'brand': '小米', 'url': 'http://www.aihuishou.com/shouji/b184'},
            {'category': '手机', 'second_category': '手机', 'brand': '华为 ', 'url': 'http://www.aihuishou.com/shouji/b9'}]

        for brand in brands:
            products = self.get_ai_product(brand)
            self.products.extend(products)

    def get_ai_product_detail(self, product):
        if product is None:
            return
        url = product["url"]
        details = [];

        response = self.session.get(url, timeout=10, headers=Utils.header())
        soup = BeautifulSoup(response.text, "html.parser")
        # print(response.text)
        data_sku_properky_value_ids = soup.find(name="div", id="group-property")[
            "data-sku-property-value-ids"]
        print(data_sku_properky_value_ids)
        self.sku_property_value_ids.append({"productId": product["productId"], "simple_type": product["simple_type"],
                                            "sku_ids": data_sku_properky_value_ids})

        # 三大详情
        divs = soup.find_all(name="div", attrs={"class": "select-property"})
        for div in divs:
            type = div.select("h2")[0].text.strip()
            dls = div.select("dl")
            for dl in dls:
                dt = dl.select("dt")
                if len(dt) == 0:
                    name = type
                else:
                    name = dt[0]["data-value"]
                lis = dl.select("li")
                for li in lis:
                    data_id = li["data-id"]
                    value = li.text.replace(r"\n", '').strip()
                    details.append({
                        "productId": product["productId"], "simple_type": product["simple_type"], "option_type": type,
                        "option_name": name, "option_value": value, "option_id": data_id
                    })
        self.product_select_property_tetail.extend(details)
        return details

    def get_ai_product_detail_test(self):
        products = [
            {'category': '手机', 'second_category': '手机', 'brand': '苹果', 'type': '苹果 iPhone 6',
             'simple_type': '苹果iPhone6', 'count': '4756', 'url': 'http://www.aihuishou.com/product/17461.html',
             'productId': '17461'},
            {'category': '手机', 'second_category': '手机', 'brand': '苹果', 'type': '苹果 iPhone 6 Plus',
             'simple_type': '苹果iPhone6Plus', 'count': '3018', 'url': 'http://www.aihuishou.com/product/17462.html',
             'productId': '17462'},
            {'category': '手机', 'second_category': '手机', 'brand': '苹果', 'type': '苹果 iPhone 7 Plus',
             'simple_type': '苹果iPhone7Plus', 'count': '696', 'url': 'http://www.aihuishou.com/product/23423.html',
             'productId': '23423'},
            {'category': '手机', 'second_category': '手机', 'brand': '苹果', 'type': '苹果 iPhone 6S',
             'simple_type': '苹果iPhone6S', 'count': '1670', 'url': 'http://www.aihuishou.com/product/17726.html',
             'productId': '17726'},
            {'category': '手机', 'second_category': '手机', 'brand': '苹果', 'type': '苹果 iPhone 6S Plus',
             'simple_type': '苹果iPhone6SPlus', 'count': '1049', 'url': 'http://www.aihuishou.com/product/17752.html',
             'productId': '17752'},
            {'category': '手机', 'second_category': '手机', 'brand': '苹果', 'type': '苹果 iPhone 7',
             'simple_type': '苹果iPhone7', 'count': '644', 'url': 'http://www.aihuishou.com/product/23422.html',
             'productId': '23422'}
        ]
        for product in products:
            self.get_ai_product_detail(product)

    def get_ai_product_price(self, product):
        url = product["url"]
        response0 = self.session.get(url, timeout=20, headers=Utils.header())
        print(response0.text)
        json = {
            "AuctionProductId": "17461",
            "PriceUnits": "3212;2021;2014;2452;2072;2100;2125;2118;2114;2067;2107;2135;;;;;3169;\
            2108;2026;2045;2102;2104;2129;2808;",
            "ProductModelId": ""
        }
        response = self.session.post(
            "http://www.aihuishou.com/userinquiry/create.html?u_asec=099%23KAFEV7EBEyGEhYTLEEEEEpEQz0yFD6twSciID6ATSui\
            qW6ATDcw5C60FuYFEw3inNEjr%2F3iStq9NllUTEEaStV7ENRaSt3ii5%2FtZE7EKt3hDEEZdtcIkfYFE19iAU7Ec%2F3i%2BPNQTEExCbP\
            i5jYFET%2FiDlllP%2FqMTEpcC96xY6wO3a4TtuQCsraSpwqCgCR4SL7dt%2BO%2FkNagcLob3PdcB8Jul3lsW4LeZaoa3aWxXNVX3LQdtP\
            fGSrYCcaIZgLshnwBZTwWw6Os86wSWpbMCVbYZKxYetZyUiwdd6%2ByvoqO73w7FcUoEnbGu6%2BoWtSa%2BGwwb3asv8byE6aYUqbtZXcE\
            A6aYetQOcW14Z31OOfOa%2Bp%2BMG7UlCMhyQu%2FGwYsEFEp3iSlllP%2F3xut37MDcZdtCOStTLtsyaGC3iSh6iP%2F3wIt37MDcZddq\
            goE7EIt37E9xYSa5arE7Eht%2FMFE6r3WEFE5YwvMfmq2bsMk6ArtioWxKNf8Z%2Bg2hWy1PbR9lAWoPD2JfgLlB5znPgMnhsDqweokjDfX\
            ybY060qaHoZbHUAaH9p%2BJW8I%2BCoiSAqquobftP2h7LuE7EFNIaHFf7TEEiStEE7VEFETRRCD6jZE7EKt3J6EEZdtc68uYFEw3in8E1\
            N%2F3iSt6wclDQTEExCbPi5BYFETRpCD6iWE7Eqt3X5EF%2Bdt3iSnYBlBYFETRpCD6iWE7Eqt3X5EwCdt3iSZbiluYFEw3inNEE7%2F3i\
            StqxNlZITEEaCdlllUiuJdzysUoS%3D&u_atype=2", json=json, timeout=20, headers=Utils.header())
        soup = BeautifulSoup(response.text, "html.parser")
        print(response.text)

    def get_ai_product_price_test(self):

        products = [
            {'category': '手机', 'second_category': '手机', 'brand': '苹果', 'type': '苹果 iPhone 6',
             'simple_type': '苹果iPhone6', 'count': '4756', 'url': 'http://www.aihuishou.com/product/17461.html',
             'productId': '17461'},
            {'category': '手机', 'second_category': '手机', 'brand': '苹果', 'type': '苹果 iPhone 6 Plus',
             'simple_type': '苹果iPhone6Plus', 'count': '3018', 'url': 'http://www.aihuishou.com/product/17462.html',
             'productId': '17462'},
            {'category': '手机', 'second_category': '手机', 'brand': '苹果', 'type': '苹果 iPhone 7 Plus',
             'simple_type': '苹果iPhone7Plus', 'count': '696', 'url': 'http://www.aihuishou.com/product/23423.html',
             'productId': '23423'},
            {'category': '手机', 'second_category': '手机', 'brand': '苹果', 'type': '苹果 iPhone 6S',
             'simple_type': '苹果iPhone6S', 'count': '1670', 'url': 'http://www.aihuishou.com/product/17726.html',
             'productId': '17726'},
            {'category': '手机', 'second_category': '手机', 'brand': '苹果', 'type': '苹果 iPhone 6S Plus',
             'simple_type': '苹果iPhone6SPlus', 'count': '1049', 'url': 'http://www.aihuishou.com/product/17752.html',
             'productId': '17752'},
            {'category': '手机', 'second_category': '手机', 'brand': '苹果', 'type': '苹果 iPhone 7',
             'simple_type': '苹果iPhone7', 'count': '644', 'url': 'http://www.aihuishou.com/product/23422.html',
             'productId': '23422'}
        ]
        for product in products[:1]:
            self.get_ai_product_price(product)

    def get_ai_product_price_by_app(self):
        params = {"productId": 17461,
                  "pricePropertyValues": [3212, 2021, 2014, 2452, 2072, 2100, 2125, 2118, 2114, 2067, 2107, 2135, 3169,
                                          2108, 2026, 2045, 2102, 2104, 2129, 2808], "cityId": 1}
        import time
        print(str(time.time()).split(".")[0])
        timestamp=str(time.time()).split(".")[0]
        request = requests.post(
            "http://gw.aihuishou.com/app-portal/product/inquiry?appId=10001&sign=f22166f9d1d861693a2d02c28c28f625\
            &timestamp="+timestamp+"&token=f9a33a38-c82d-41a7-b40e-21117db5978f",
            json=str(params), headers={"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.0; DUK-AL20 Build/HUAWEIDUK-AL20)",
                                  "Content-Type": "application/json; charset=utf-8"})
        print(request.text)


if __name__ == "__main__":
    print("------ start ----------")
    ai = aihuishou()
    # ai.get_ai_category()
    # for cate in ai.category:
    #     brands = ai.get_ai_brand(cate)
    #     if brands is not None:
    #         ai.brand.extend(brands)
    # ai.get_ai_second_category(ai.brand)

    #   table 1    品牌分类表    ahs_brand

    # 0 - ----{'category': '手机', 'second_category': '手机', 'brand': '苹果', 'url': 'http://www.aihuishou.com/shouji/b52'}
    # 1 - ----{'category': '手机', 'second_category': '手机', 'brand': '三星', 'url': 'http://www.aihuishou.com/shouji/b7'}
    # 2 - ----{'category': '手机', 'second_category': '手机', 'brand': '小米', 'url': 'http://www.aihuishou.com/shouji/b184'}
    # 3 - ----{'category': '手机', 'second_category': '手机', 'brand': '华为 ', 'url': 'http://www.aihuishou.com/shouji/b9'}

    #  table 2  产品分类表  ahs_product

    # {'category': '手机', 'second_category': '手机', 'brand': '苹果', 'type': '苹果 iPhone 6S Plus',
    #  'simple_type': '苹果iPhone6SPlus', 'count': '1049', 'url': 'http://www.aihuishou.com/product/17752.html',
    #  'productId': '17752'},
    # {'category': '手机', 'second_category': '手机', 'brand': '苹果', 'type': '苹果 iPhone 7',
    #  'simple_type': '苹果iPhone7', 'count': '644', 'url': 'http://www.aihuishou.com/product/23422.html',
    #  'productId': '23422'}

    # table 3  sku组合类  ahs_product_sku

    # {'productId': '17461', 'simple_type': '苹果iPhone6', 'sku_ids': '[["2014","2022","2075","2452","3212"],["2019","202
    #  {'productId': '17462', 'simple_type': '苹果iPhone6Plus', 'sku_ids': '[["2014","2022","2075","2454","3217"],["2024",

    # table 4  产品选项详情类 ahs_product_option_detail

    # {'productId': '17461', 'simple_type': '苹果iPhone6', 'option_type': '基本信息', 'option_name': '型号',
    #  'option_value': 'A1586-全网通', 'option_id': '3212'}
    # {'productId': '17461', 'simple_type': '苹果iPhone6', 'option_type': '基本信息', 'option_name': '型号',
    # 'option_value': '其他','option_id': '3213'}
    # {'productId': '17461', 'simple_type': '苹果iPhone6', 'option_type': '基本信息', 'option_name': '存储容量',
    #  'option_value': '16G', 'option_id': '2021'}
    # {'productId': '17461', 'simple_type': '苹果iPhone6', 'option_type': '基本信息', 'option_name': '存储容量',
    #  'option_value': '32G', 'option_id': '2022'}


    # table 5 查询组合类  ahs_product_priceUnits


    # ai.get_ai_product_test()


    # ai.get_ai_product_detail_test()

    # ai.get_ai_product_price_test()
    ai.get_ai_product_price_by_app()
    ai.print()
    print("------ end ----------")
