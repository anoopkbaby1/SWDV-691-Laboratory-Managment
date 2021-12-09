from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^labs/$',views.lab,name='lab'),
	url(r'^testnames/$',views.tetnam,name='tetnam'),
	url(r'^pathologistInfo/$',views.pathologistInfo,name='pathologistInfo'),
	url(r'^menuhom/$',views.menuhom,name='home_menu'),
	url(r'^tid_sub/$',views.tid_sub,name='tid_sub'),
	url(r'^testty/$',views.testty,name='tetty'),
	url(r'^agent_show/$',views.agent_show,name='agent_show'),
	url(r'^getBills/$',views.getBills,name='getBills'),
    url(r'^getPatients/$',views.getPatients,name='getPatients'),
    url(r'^showGraph/$',views.showGraph,name='showGraph')
]