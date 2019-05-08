from . import views
from django.urls import path, re_path

app_name = 'users'
urlpatterns = [
	path('', views.login),
	re_path(r'^register/$', views.register, name='register'),
	re_path(r'^login/$', views.login, name='login'),
	re_path(r'^user/(?P<pk>\d+)/profile/$', views.profile, name='profile'),
	re_path(r'^user/(?P<pk>\d+)/profile/update/$', views.profile_update, name='profile_update'),
	# re_path(r'^user/(?P<pk>\d+)/pwdchange/$', views.pwd_change, name='pwd_change'),
	re_path(r'^logout/$', views.logout, name='logout'),
]
