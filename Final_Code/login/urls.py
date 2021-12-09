from django.conf.urls import include,url
from . import views

urlpatterns = [
	url(r'^$', views.log_in, name='log_in'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^login_auth/$', views.login_auth, name='login_auth'),
	url(r'^new_check/$', views.reg, name='reg'),
	url(r'^red_home/$',views.red,name='red')
]