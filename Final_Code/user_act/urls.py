from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^$',views.load_home,name='load_home'),
	url(r'^sign_out/$',views.go_home,name='go_home'),
	url(r'^book/$',views.book,name='book'),
	url(r'^book_submit/$',views.book_submit,name='book_submit'),
	url(r'^prev/$',views.prev,name='prev'),
	url(r'^menu/$',views.menu,name='menu'),
	url(r'^track/$',views.track,name='track'),
	url(r'^update/$',views.update,name='update'),
	url(r'^update_check/$',views.update_check,name='update_check')
]