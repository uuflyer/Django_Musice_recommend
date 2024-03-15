from eapp.models import User
from django.contrib.auth.models import User
from rest_framework.authtoken.views import APIView, AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


# 用户注册
class Register(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            resp = {
                'status': False,
                'data': '用户名已被注册'
            }
        else:
            # user = User(username=username,password=password)
            # user.save()
            user = User.objects.create_user(username=username, password=password)
            token, created = Token.objects.get_or_create(user=user)
            resp = {
                'status': True,
                'token': token.key,
                'user_id': user.pk,
                'user_name': user.username,
            }
        return Response(resp)


# 用户登录
class Login(APIView):
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data, context={'request': request})
        status = False
        resp = {}
        if (serializer.is_valid() == True):
            status = True
            user = serializer.validated_data['user']
            resp['userId'] = user.pk
            resp['userName'] = user.username
            resp['isSuperUser'] = user.is_superuser
        resp['status'] = status

        return Response(resp)


from django.db import connection


# 热门推荐








#推荐模型
from eapp.sbrec import UserBasedCF

class refreshRecommend(APIView):
    def rating(self):
        sql = 'select user_id,movie_id,rating from rating'
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchall()
        return row

    def get_movie_info(self, movie_ids):
        sql = 'select id as movieId,concat(id,\'.jpg\') as url,title as name,year as releaseDate,tags as type,director as leader from movie where id in(%s)' % movie_ids
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = list(cursor.fetchall())
            title = [title[0] for title in cursor.description]
            res = []
            for item in row:
                res.append(dict(list(zip(title, item))))
        return res

    def get_recommend_res(self, user_id):
        sql = 'select movie_ids from recommend_res where user_id = %d' %(user_id)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()
        if row is None:
            return 0
        else:
            return 1

    def save_movie_info(self, user_id, movie_ids):
        add_sql = 'INSERT into recommend_res (user_id,movie_ids) VALUES (%d, \'%s\')' %(user_id, movie_ids)
        with connection.cursor() as cursor:
            cursor.execute(add_sql)
        status = {'status': 'success'}
        return Response(status)

    def update_movie_info(self, user_id, movie_ids):
        add_sql = 'UPDATE recommend_res SET movie_ids= \'%s\' where user_id = %d' %( movie_ids, user_id)
        with connection.cursor() as cursor:
            cursor.execute(add_sql)
        status = {'status': 'success'}
        return Response(status)

    def post(self, request):
        u_id = request.data.get("userId")
        userrecommend = UserBasedCF()
        row = self.rating()
        userrecommend.generate_dataset(row)
        userrecommend.calc_user_sim()
        r_data = userrecommend.recommend(u_id)
        movie_ids = ''
        j = 0
        for i in r_data:
            if j != 0:
                movie_ids += ',' + str(i)
            else:
                movie_ids += str(i)
            j += 1
        movie_info = self.get_movie_info(movie_ids)
        res = self.get_recommend_res(u_id)
        if res == 0:
            self.save_movie_info(u_id, movie_ids)
        elif res == 1:
            self.update_movie_info(u_id,movie_ids)
        return Response(movie_info)





