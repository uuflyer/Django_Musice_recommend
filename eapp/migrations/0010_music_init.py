# Generated by Django 4.1.7 on 2023-03-30 07:24
import null as null
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0009_rename_passwored_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(verbose_name='用户id')),
                ('songs_info_id', models.IntegerField(verbose_name='歌曲信息表ID')),
                ('rating', models.FloatField(verbose_name='评分')),
                ('create_time',models.TimeField(auto_now=True,auto_now_add=True,verbose_name='创建时间')),
                ('create_user', models.CharField(max_length=20,default='admin',verbose_name='创建人员')),
                ('update_time', models.TimeField(auto_now=True, auto_now_add=True, verbose_name='更新时间')),
                ('update_user', models.CharField(max_length=20,default='admin',verbose_name='更新人员')),
            ],
            options={
                'db_table': 'rating',
                'verbose_name': '用户评分表',
                'verbose_name_plural': '用户评分表',
            },
        ),
        migrations.CreateModel(
            name='user_relation',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_user_id', models.IntegerField(verbose_name='当前主用户ID')),
                ('friend_user_id', models.IntegerField(verbose_name='朋友用户ID')),
                ('trustStatus', models.IntegerField(verbose_name='1-关注,-1-不感兴趣,null-未标记')),
                ('create_time', models.TimeField(auto_now=True,  verbose_name='创建时间')),
                ('create_user', models.CharField(max_length=20, default='admin', verbose_name='创建人员')),
                ('update_time', models.TimeField(auto_now=True, verbose_name='更新时间')),
                ('update_user', models.CharField(max_length=20, default='admin', verbose_name='更新人员')),
            ],
            options={
                'db_table': 'user_relation',
                'verbose_name': '用户关系表',
                'verbose_name_plural': '用户关系表',
            },
        ),
        migrations.CreateModel(
            name='tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(verbose_name='当前主用户ID')),
                ('interest_song_type', models.CharField(max_length=100,verbose_name='感兴趣歌曲类型')),
                ('interest_singer', models.CharField(max_length=50,verbose_name='喜爱歌手')),
                ('create_time', models.TimeField(auto_now=True, auto_now_add=True, verbose_name='创建时间')),
                ('create_user', models.CharField(max_length=20,default='admin', verbose_name='创建人员')),
                ('update_time', models.TimeField(auto_now=True, auto_now_add=True, verbose_name='更新时间')),
                ('update_user', models.CharField(max_length=20,default='admin', verbose_name='更新人员')),
            ],
            options={
                'db_table': 'tag',
                'verbose_name': '用户兴趣信息表',
                'verbose_name_plural': '用户兴趣信息表',
            },
        ),
        migrations.CreateModel(
            name='songs_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50,verbose_name='歌曲名称')),
                ('type', models.CharField(max_length=50, verbose_name='歌曲类型')),
                ('singer', models.CharField(max_length=50, verbose_name='演唱歌手')),
                ('img_url', models.CharField(max_length=50, verbose_name='歌曲图片地址')),
                ('create_time', models.TimeField(auto_now=True, auto_now_add=True, verbose_name='创建时间')),
                ('create_user', models.CharField(max_length=20,default='admin', verbose_name='创建人员')),
                ('update_time', models.TimeField(auto_now=True, auto_now_add=True, verbose_name='更新时间')),
                ('update_user', models.CharField(max_length=20,default='admin', verbose_name='更新人员')),
            ],
            options={
                'db_table': 'songs_info',
                'verbose_name': '歌曲信息表',
                'verbose_name_plural': '歌曲信息表',
            },
        ),
    ]
