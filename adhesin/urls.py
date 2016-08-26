from django.conf.urls import url

from . import views

app_name = 'adhesin'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^intext$', views.inText, name='inText'),
    url(r'^wait$', views.wait, name='wait'),
    url(r'^infile$', views.inFile, name='inFile'),
    url(r'^infile/nPage$', views.nPage, name='nPage'),
]
