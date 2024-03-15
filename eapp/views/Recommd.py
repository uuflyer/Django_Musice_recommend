
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from django.db import connection

class recommend(APIView):
    def Recommend(self, userId,pageSize,offSet):
        sql = 'select s.id,s.name,s.singer,s.type,s.img_url,r.rating from songs_info s join rating r on s.id = r.songs_info_id where  r.user_id= %d order by r.rating desc limit %d offset %d' % (
            userId, pageSize, offSet)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            all = cursor.fetchall()
        return all

    def post(self, request):
        u_id = request.data.get("userId")
        page_size = request.data.get("pageSize")
        offset = request.data.get("offset")
        movie_ids = self.Recommend(u_id,page_size,offset)
        arr = []
        for item in movie_ids:
            rsp = {'id': item[0],'name':item[1],'singer':item[2],'type':item[3],'url':item[4],'rate':item[5]}
            arr.append(rsp)
        return Response(arr)


class Hot(APIView):
    def get_global_top10_song_info(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT r.songs_info_id ,song.name,song.img_url, avg(r.rating) as avg_rate from rating r join songs_info song on song.id = r.songs_info_id group by r.user_id,r.songs_info_id  order by avg_rate desc limit 10")
            row = cursor.fetchall()
        return row

    def post(self, request):
        r_number = Hot().get_global_top10_song_info()
        resp = []
        for i in r_number:
            m_id = i[0]
            m_url = i[2]
            re = {'id': m_id, 'url': m_url,'avg_rate':i[3]}
            resp.append(re)
        return Response(resp)