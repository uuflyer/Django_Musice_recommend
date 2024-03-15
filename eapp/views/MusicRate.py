
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from django.db import connection

# 用户评分过得音乐
class MusicRate(APIView):
    def ratedMovies(self, userId):
        sql = 'select s.id,s.name,s.singer,s.type,s.img_url,r.rating,r.id from songs_info s join rating r on s.id = r.songs_info_id where  r.user_id= %d order by r.update_time desc' % (
            userId)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchall()
        return row

    def post(self, request):
        u_id = request.data.get("userId")
        r_number = self.ratedMovies(u_id)
        resp = {'total':0,'allData':[]}
        arry = []
        resp['total'] = len(r_number)
        for i in r_number:
            re = {'id': i[0],'name': i[1],'singer': i[2], 'type': i[3],'url': i[4],'rate': i[5],'rateId':i[6]}
            arry.append(re)
        resp['allData'] = arry
        return Response(resp)


# 用户未评分过得音乐
class UnRatedMusic(APIView):
    def unratedMusic(self, userId):
        sql = "select id,name,singer,type,img_url from songs_info where id not in(select songs_info_id from rating where user_id = %d ) order by id " % (
            userId)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchall()
        return row

    def post(self, request):
        u_id = request.data.get("userId")
        r_data = self.unratedMusic(u_id)
        resp = {'total':0,'allData':[]}
        arry = []
        for i in r_data:
            re = {'id': i[0],'name': i[1],'singer': i[2], 'type': i[3],'url': i[4]}
            arry.append(re)
        resp['allData'] = arry
        return Response(resp)


# 保存用户对音乐的评分信息
class saveMusicRate(APIView):
    def post(self, request):
        u_id = request.data.get("userId")
        m_id = request.data.get("songId")
        rate = request.data.get("rate")
        sql = 'insert into rating(user_id,songs_info_id,rating) values(%d,%d,%f) ON DUPLICATE KEY UPDATE rating=%f ' % (u_id, m_id, rate,rate)
        with connection.cursor() as cursor:
            cursor.execute(sql)
        status = {'status': 'success'}
        return Response(status)

# 更新用户对音乐的评分信息
class updateMusicRate(APIView):
    def post(self, request):
        u_id = request.data.get("userId")
        rateId = request.data.get("rateId")
        rate = request.data.get("rate")
        sql = 'update rating set rating= %f where id = %d ' % (rate, rateId)
        with connection.cursor() as cursor:
            cursor.execute(sql)
        status = {'status': 'success'}
        return Response(status)

# 删除用户对音乐的评分信息
class delMusicRate(APIView):
    def post(self, request):
        rateId = request.data.get("rateId")
        sql = 'delete from rating  where id = %d ' % ( rateId)
        with connection.cursor() as cursor:
            cursor.execute(sql)
        status = {'status': 'success'}
        return Response(status)