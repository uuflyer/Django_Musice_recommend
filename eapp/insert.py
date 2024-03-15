import unittest

import pandas
import pymysql
from django.contrib.auth.models import User

class MyTestCase(unittest.TestCase):
    def insertUserInfo(self):
        password = 'test001'

        for i in range(1,100):
            username = "testUser00"+i
            user = User.objects.create_user(username=username, password=password)
            print("插入成功用户"+username)



    # def test_something(self):
    #     file = r'E:\MyStore\Final_Project\EsSystem2\音乐数据集.xlsx'
    #     df = pandas.read_excel(file)
    #     infoData = pandas.DataFrame(df).values
    #     print(infoData[0])
    #
    #     db = pymysql.connect(host='192.168.1.105',
    #                          user='root',
    #                          password='tangql2021',
    #                          port=3309,
    #                          database='music')
    #     cursor = db.cursor()
    #     for i in range(0,len(infoData)):
    #         item = []
    #         item = infoData[i]
    #         print(item)
    #         sql = "insert into songs_info(id,name,type,singer,img_url) values(%d,'%s','%s','%s','%s') " % (item[0],item[1],item[4],item[2],str(item[0])+'.png')
    #         try:
    #             cursor.execute(sql)
    #             db.commit()
    #         except:
    #             print("出错了")
    #             db.rollback()
    #     print("读取成功!")



if __name__ == '__main__':
    unittest.main()
