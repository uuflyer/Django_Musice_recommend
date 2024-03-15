from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from django.db import connection


# 查询已有社交列表
class Relationship(APIView):
    def relation(self, userId):
        userId = int(userId)
        sql = "select r.friend_user_id,r.trustStatus,u.username from user_relation r left join auth_user u on u.id = r.friend_user_id  where r.primary_user_id = %d order by u.id" % userId
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchall()
        return row

    def post(self, request):
        u_id = request.data.get("userId")
        r_relation = self.relation(u_id)
        resp = {}
        allData = []
        for i in r_relation:
            user_Id = i[0]
            trustStatus = i[1]
            user_name = i[2]
            sql = "select interest_song_type,interest_singer from tag where user_id =%d" % (user_Id)
            with connection.cursor() as cursor:
                cursor.execute(sql)
                row = cursor.fetchone()
                interestsSongType = row[0] if row is not None else ''
                interestsSinger = row[1] if row is not None else ''
                if not row:
                    re = {'id': user_Id, 'userName': user_name, 'interestsSongType': interestsSongType, 'interestsSinger':interestsSinger,'trustStatus': trustStatus}
                allData.append(re)
            resp= {'allData':allData,'total':len(r_relation)}
        return Response(resp)
# 查询增加社交列表
class query_non_related_tableData(APIView):
    def relation(self, userId):
        sql = "select distinct u.id, u.username ,t.interest_song_type,t.interest_singer from auth_user u  left join tag t on u.id = t.user_id where u.id not in(select friend_user_id from user_relation where primary_user_id = %d) order by u.id" % (userId)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchall()
        return row

    def post(self, request):
        u_id = request.data.get("userId")
        r_relation = self.relation(u_id)
        resp = {}
        allData = []
        for i in r_relation:
            user_Id = i[0]
            user_name = i[1]
            # add_sql = "select interest_song_type,interest_singer from tag where user_id = %d" % (user_Id)
            # with connection.cursor() as cursor:
            #     cursor.execute(add_sql)
            #     row = cursor.fetchone()
            re = {'id': user_Id, 'userName': user_name, 'interestsSongType': i[2], 'interestsSinger': i[3],'trustStatus':0}
            allData.append(re)
        resp = {'allData':allData,'total':len(r_relation)}
        return Response(resp)
#增加社交关系
class add_tableData(APIView):
    def post(self,request):
        primary_user_id = int(request.data.get("primaryUserId"))
        friend_user_id = int(request.data.get("friendUserId"))
        relation = int(request.data.get("trustStatus"))
        add_sql = "INSERT into user_relation (primary_user_id,friend_user_id,trustStatus,create_time,create_user,update_time,update_user) VALUES (%d,%d,%d,NOW(),'admin',NOW(),'admin')" % (primary_user_id, friend_user_id, relation)
        with connection.cursor() as cursor:
            cursor.execute(add_sql)
        status = {'status': 'success'}
        return Response(status)

#修改社交关系
class update_tableData(APIView):
    def post(self, request):
        primary_user_id = int(request.data.get("primaryUserId"))
        friend_user_id = int(request.data.get("friendUserId"))
        relation = int(request.data.get("trustStatus"))
        update_sql = 'update user_relation set trustStatus = %d where primary_user_id = %d and friend_user_id = %d' % (relation, primary_user_id, friend_user_id)
        with connection.cursor() as cursor:
            cursor.execute(update_sql)
        status = {'status': 'success'}
        return Response(status)

#删除社交关系
class delete_tableData(APIView):
    def post(self, request):
        primary_user_id = int(request.data.get("primaryUserId"))
        friend_user_id = int(request.data.get("friendUserId"))
        delete_sql = 'delete from user_relation where primary_user_id = %d and friend_user_id = %d' % (primary_user_id, friend_user_id)
        with connection.cursor() as cursor:
            cursor.execute(delete_sql)
        status = {'status': 'success'}
        return Response(status)
