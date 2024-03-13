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
from eapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', views.Register.as_view()),
    path('api/login/', views.Login.as_view()),
    path('api/Hot/', views.Hot.as_view()),
    path('api/ratedMovie/', views.movieRate.as_view()),
    path('api/unratedMovie/', views.unmovieRate.as_view()),
    path('api/tableData/', views.tableData.as_view()),
    path('api/saveMovieRate/', views.saveMovieRate.as_view()),
    path('api/tableData/', views.tableData.as_view()),
    path('api/query_non_related_tableData/', views.query_non_related_tableData.as_view()),
    path('api/add_tableData/', views.add_tableData.as_view()),
    path('api/update_tableData/', views.update_tableData.as_view()),
    path('api/delete_tableData/', views.delete_tableData.as_view()),
    path('api/recommend/', views.recommend.as_view()),
    path('api/refreshRecommend/', views.refreshRecommend.as_view()),
]
