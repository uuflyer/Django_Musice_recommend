from django.db import models

class User(models.Model):
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=20)

    class Meta:
        db_table = 'user'  #用于模型的数据库表的名称：
        verbose_name = verbose_name_plural = '用户信息表'

class userToken(models.Model):
    username = models.OneToOneField(to='User', on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=60)

    class Meta:
        db_table = 'user_token'
        verbose_name = verbose_name_plural = '用户token表'

class rating(models.Model):
    user_id = models.IntegerField(default=0,verbose_name='用户id')
    movie_id = models.IntegerField(default=0,verbose_name='电影id')
    rating = models.IntegerField(default=0,verbose_name='评分')

    class Meta:
        db_table = 'rating'

# class movie(models.Model):
