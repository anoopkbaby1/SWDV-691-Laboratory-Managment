from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^$',views.load_home2,name='load_home2'),
	url(r'^sign_out/$',views.go_home2,name='go_home2'),
	url(r'^menu/$',views.menu,name='menu_ag'),
	url(r'^view_t/$',views.view_t,name='view_t'),
	url(r'^track_t/$',views.track_t,name='track_t'),
	url(r'^sel_test/$',views.sel_test,name='sel_test'),
	url(r'^update_details/$',views.update_d,name='update_d'),
	url(r'^patient/$',views.patient,name='patient'),
	url(r'^display/$',views.display,name='display')
]