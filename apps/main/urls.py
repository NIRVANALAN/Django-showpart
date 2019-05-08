from django.conf.urls import *
from main.views import *
from django.urls import path

urlpatterns = [
	path('', index),
	path('index/', index),
	path('about/', about),
	path('download_path/', trace_path_data_down),
	path('download_dot/', trace_dot_data_down),
	path('upload/', upload),
	path('class/', class_router),
	path('contact/', contact),
	path('paint/', paint),
	path('trainers/', visuService),
	path('codes/', codes),
	path('track/', track),
	path('success/', success)
]
