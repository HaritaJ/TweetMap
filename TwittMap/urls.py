from django.conf.urls import url
from django.contrib import admin
from . import views
app_name='TwittMap'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^user/create/$', views.create_user, name="create_user"),
]