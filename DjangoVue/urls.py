"""DjangoVue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from eapp.views import views, sysManager,Recommd,MusicRate,Relationship


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', views.Register.as_view()),
    path('api/login/', views.Login.as_view()),
    path('api/Hot/', Recommd.Hot.as_view()),
    path('api/recommend/', Recommd.recommend.as_view()),
    path('api/ratedMusic/', MusicRate.MusicRate.as_view()),
    path('api/unratedMusic/', MusicRate.UnRatedMusic.as_view()),
    path('api/saveMusicRate/', MusicRate.saveMusicRate.as_view()),
    path('api/updateMusicRate/', MusicRate.updateMusicRate.as_view()),
    path('api/delMusicRate/', MusicRate.delMusicRate.as_view()),


    path('api/tableData/', Relationship.Relationship.as_view()),
    path('api/query_non_related_tableData/', Relationship.query_non_related_tableData.as_view()),
    path('api/add_tableData/', Relationship.add_tableData.as_view()),
    path('api/update_tableData/', Relationship.update_tableData.as_view()),
    path('api/delete_tableData/', Relationship.delete_tableData.as_view()),
    path('api/delUser/', sysManager.UserDel.as_view()),
    path('api/loadAllUser/', sysManager.UserQuery.as_view()),
    path('api/loadSearchUser/', sysManager.UserLikeQuery.as_view()),
    path('api/loadSearchSong/', sysManager.SongLikeQuery.as_view()),
    path('api/loadAllSong/', sysManager.SongQuery.as_view()),
    path('api/delSong/', sysManager.SongDel.as_view()),



    # path('api/refreshRecommend/', views.refreshRecommend.as_view()),
]
