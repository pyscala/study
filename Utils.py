import pymysql
import datetime


# 打印时间，并返回时间戳
def logTime():
    t = datetime.datetime.now()
    print(t.strftime('%Y-%m-%d %H:%M:%S'))
    return datetime.datetime.now().timestamp()


# 简单设置Header信息
def header():
    return {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            }


# 获取数据库连接
def getCon():
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'cashbus666888',
        'db': 'cashbus_meta',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor

    }
    return pymysql.connect(**config)


# 把全球机场信息插入数据库airport表中
def addAirportToMysql(db, list):
    cursor = db.cursor()
    sql = "insert into  airport values (%s,%s,%s,%s,%s)"
    try:
        cursor.executemany(sql, list)
        db.commit()
    except Exception as err:
        print("插入数据库表airport错误------>" + err)
    cursor.close()


# 把全国机场信息插入数据库airport_china表中
def addAirportOfChinaToMysql(db, list):
    cursor = db.cursor()
    sql = "insert into  airport_china values (%s,%s,%s,%s,%s,%s)"
    try:
        cursor.executemany(sql, list)
        db.commit()
    except Exception as err:
        print("插入数据库表airport_china错误------>" + err)
    cursor.close()


# 生成三字码，插入表airport_threecode中，一次性方法。
def creatThreeCode():
    ls = []
    for i in range(97, 123):
        first = chr(i).upper()
        for j in range(97, 123):
            second = chr(j).upper()
            for k in range(97, 123):
                three = chr(k).upper();
                ls.append((str(first) + str(second) + str(three), '0', '0'))
    db = getCon()
    try:
        with db.cursor() as cursor:
            sql = "insert into airport_threecode  VALUES (%s,%s,%s)"
            cursor.executemany(sql, ls)
            db.commit()
    finally:
        db.close()
