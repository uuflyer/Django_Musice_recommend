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
            token, created = Token.objects.get_or_create(user=user)
            resp['token'] = token.key
            resp['userId'] = user.pk
            resp['userName'] = user.username
            resp['isSuperUser'] = user.is_superuser
        resp['status'] = status

        return Response(resp)


from django.db import connection


# 热门推荐
class Hot(APIView):
    def get_top10_movie_info(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "select distinct movie_id , count(1) as total from rating group by movie_id order by total desc limit 10")
            row = cursor.fetchall()
        return row

    def post(self, request):
        r_number = Hot().get_top10_movie_info()
        resp = []
        for i in r_number:
            m_id = i[0]
            m_url = '%d.jpg' % (m_id)
            re = {'id': m_id, 'url': m_url}
            resp.append(re)
        return Response(resp)


# 用户评分过得电影
class movieRate(APIView):
    def ratedMovies(self, userId, page_size, offset):
        sql = 'select m.id,m.title,m.year,m.tags,r.rating from movie m join rating r on m.id = r.movie_id where  user_id= %d order by r.update_time desc limit %d offset %d' % (
            userId, page_size, offset)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchall()
        return row

    def post(self, request):
        u_id = request.data.get("userId")
        page_size = request.data.get("pageSize")
        offset = request.data.get("offset")
        r_number = self.ratedMovies(u_id, page_size, offset)
        resp = []
        for i in r_number:
            m_id = i[0]
            m_url = '%d.jpg' % (m_id)
            re = {'name': i[1], 'url': m_url, 'releaseDate': i[2], 'type': i[3], 'rate': i[4], 'movieId': m_id}
            resp.append(re)
        return Response(resp)


# 用户未评分过得电影
class unmovieRate(APIView):
    def unratedMovies(self, userId, page_size, offset):
        sql = "select id,title,year,tags,director from movie where id not in(select movie_id from rating where user_id = %d ) order by id limit %d offset %d" % (
            userId, page_size, offset)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchall()
        return row

    def post(self, request):
        u_id = request.data.get("userId")
        page_size = request.data.get("pageSize")
        offset = request.data.get("offset")
        r_data = self.unratedMovies(u_id, page_size, offset)
        resp = []
        for i in r_data:
            m_id = i[0]
            m_url = '%d.jpg' % (m_id)
            re = {'name': i[1], 'url': m_url, 'releaseDate': i[2], 'type': i[3], 'leader': i[4], 'movieId': m_id}
            resp.append(re)
        return Response(resp)


# 保存用户对电影的评分信息
class saveMovieRate(APIView):
    def post(self, request):
        u_id = request.data.get("userId")
        m_id = request.data.get("movieId")
        rate = request.data.get("rate")
        sql = 'insert into rating(user_id,movie_id,rating) values(%d,%d,%f) ON DUPLICATE KEY UPDATE rating=%f ' % (u_id, m_id, rate,rate)
        with connection.cursor() as cursor:
            cursor.execute(sql)
        status = {'status': 'success'}
        return Response(status)


# 社交列表
class tableData(APIView):
    def relation(self, userId):
        sql = "select r.friend_user_id,r.trust,u.username from user_relation r left join auth_user u on u.id = r.friend_user_id  where r.primary_user_id = %d order by u.id" % (userId)
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
            sql = "select group_concat(distinct tag) AS tag from tags where user_id =%d" % (user_Id)
            with connection.cursor() as cursor:
                cursor.execute(sql)
                row = cursor.fetchone()
                re = {'id': user_Id, 'userName': user_name, 'interests': row[0], 'trustStatus': trustStatus}
                allData.append(re)
            resp= {'allData':allData,'total':len(r_relation)}
        return Response(resp)
# 查询增加社交列表
class query_non_related_tableData(APIView):
    def relation(self, userId):
        sql = "select distinct t.user_id, u.username from tags t left join auth_user u on u.id = t.user_id where t.user_id not in(select friend_user_id from user_relation where primary_user_id = %d) order by u.id" % (userId)
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
            add_sql = "select group_concat(distinct tag) AS tag from tags where user_id = %d" % (user_Id)
            with connection.cursor() as cursor:
                cursor.execute(add_sql)
                row = cursor.fetchone()
                re = {'id': user_Id, 'userName': user_name, 'interests': row[0],'trustStatus':0}
                allData.append(re)
            resp = {'allData':allData,'total':len(r_relation)}
        return Response(resp)
#增加社交关系
class add_tableData(APIView):
    def post(self,request):
        primary_user_id = int(request.data.get("primaryUserId"))
        friend_user_id = int(request.data.get("friendUserId"))
        relation = int(request.data.get("trustStatus"))
        add_sql = 'INSERT into user_relation (primary_user_id,friend_user_id,trust,create_time,update_time) VALUES (%d,%d,%d,NOW(),NOW())' % (primary_user_id, friend_user_id, relation)
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
        update_sql = 'update user_relation set trust = %d where primary_user_id = %d and friend_user_id = %d' % (relation, primary_user_id, friend_user_id)
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


class recommend(APIView):
    def Recommend(self, user_id):
        sql = 'select movie_ids from recommend_res where user_id = %d' %(user_id)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()
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

    def post(self, request):
        u_id = request.data.get("userId")
        movie_ids = self.Recommend(u_id)
        if movie_ids is None:
            fresh = refreshRecommend()
            movie_info = fresh.post(request)
            return movie_info
        else:
            movie_ids = ''.join(self.Recommend(u_id))
            movie_info = self.get_movie_info(movie_ids)
            return Response(movie_info)


