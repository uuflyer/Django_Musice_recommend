from eapp.models import User
from django.contrib.auth.models import User
from rest_framework.authtoken.views import APIView, AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


from django.db import connection

# 用户删除
class UserDel(APIView):
    def post(self, request):
        userId = request.data.get('userId')
        delSql = 'UPDATE auth_user SET is_active=0 WHERE id= %d' % userId
        with connection.cursor() as cursor:
            cursor.execute(delSql)
        resp = {'status':'success'}
        return Response(resp)

# 获取全部用户
class UserQuery(APIView):
    def post(self, request):
        resp = {'total' : 0,'allData':[]}
        querySql = "select u.username as userName,t.interest_song_type as interestsSongType ,t.interest_singer as interestSinger,u.id from auth_user u left join tag t on t.user_id = u.id where u.is_active = 1 and u.username != 'admin'"
        with connection.cursor() as cursor:
            cursor.execute(querySql)
            row = cursor.fetchall()
            resp['total'] =len(row)
            arry = []
            for i in row:
                item = {'userName':i[0],'interestsSongType':i[1],'interestSinger':i[2],'id':i[3]}
                arry.append(item)
            resp['allData'] = arry
        return Response(resp)


# 模糊查询用户
class UserLikeQuery(APIView):
    def post(self, request):
        searchName = request.data.get('userName')
        resp = {'total' : 0,'allData':[]}
        sql = "select u.username as userName,t.interest_song_type as interestsSongType ,t.interest_singer as interestSinger,u.id from auth_user u left join tag t on t.user_id = u.id where u.is_active = 1 and u.username != 'admin' and u.username like '%"
        querySql =sql+ searchName+"%'"
        with connection.cursor() as cursor:
            cursor.execute(querySql)
            row = cursor.fetchall()
            resp['total'] =len(row)
            arry = []
            for i in row:
                item = {'userName':i[0],'interestsSongType':i[1],'interestSinger':i[2],'id':i[3]}
                arry.append(item)
            resp['allData'] = arry
        return Response(resp)

# 歌曲删除
class SongDel(APIView):
    def post(self, request):
        songId = request.data.get('songId')
        delSql = 'delete from songs_info where id = %d' % songId
        with connection.cursor() as cursor:
            cursor.execute(delSql)
        resp = {'status':'success'}
        return Response(resp)

# 歌曲查询
class SongQuery(APIView):
    def post(self, request):
        resp = {'total' : 0,'allData':[]}
        querySql = 'select id,name,type,singer,img_url as url  from songs_info '
        with connection.cursor() as cursor:
            cursor.execute(querySql)
            row = cursor.fetchall()
            resp['total'] = len(row)
            arry = []
            for i in row:
                item = {'id': i[0], 'songName': i[1], 'type': i[2], 'singer': i[3], 'url': i[4]}
                arry.append(item)
            resp['allData'] = arry
        return Response(resp)

class SongLikeQuery(APIView):
    def post(self, request):
        searchName = request.data.get('songName')
        resp = {'total' : 0,'allData':[]}
        itemPre = "select id,name,type,singer,img_url as url  from songs_info where name like '%"
        querySql = itemPre + searchName + "%'"
        with connection.cursor() as cursor:
            cursor.execute(querySql)
            row = cursor.fetchall()
            resp['total'] = len(row)
            arry = []
            for i in row:
                item = {'id': i[0],'songName': i[1], 'type': i[2], 'singer': i[3],'url':i[4] }
                arry.append(item)
            resp['allData'] = arry
        return Response(resp)