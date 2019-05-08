from django.conf.urls import *
from main.views import *
from django.urls import path

urlpatterns = [
	path('', index),
	path('index/', index),
	path('about/', about),
	path('create/', create_blog_post),
	path('download_path/', trace_path_data_down),
	path('download_dot/', trace_dot_data_down),
	path('upload/', upload),
	path('class/', class_router),
	path('contact/', contact),
	path('trainers/', trainers),
	path('codes/', codes),
	path('paint/', paint),
]
