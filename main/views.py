from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from main.models import *
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import requests
import logging

pic_upload_add = 'http://192.168.254.117:8806/picture/uploadAndFind'
pic_upload_andFind = 'http://123.206.79.138:8806/picture/uploadAndFind'

frame = 1
sequenceId = '20181005001'
cameraId = 1

# logging
logger = logging.getLogger('django')
logger.info('logger "django" start')


@login_required
def index(request):
	return render(request, 'main/index.html')


def success(request):
	return render(request, 'main/success.html')


@login_required
def about(request):
	return render(request, "main/about.html")


@login_required
def contact(request):
	return render(request, "main/contact.html")


@login_required
def trainers(request):
	return render(request, "main/trainers.html")


def class_router(request):
	return render(request, "main/class.html")


def codes(request):
	return render(request, "main/codes.html")


data_ = []


def track(request):
	if request.method == 'POST':
		form = PicFrom(request.POST, request.FILES)
		if form.is_valid():
			# username = form.cleaned_data['user_name']
			# head_img = form.cleaned_data['headImg']
			Pic(
				img=request.FILES.get('img'),
				time=datetime.now()
			).save()
			files = {'file': open('./Media/img/' + request.FILES.get('img').name, 'rb')}
			response = requests.post(pic_upload_andFind, data={'startFrame': 0, 'finishFrame': 4, 'sequenceId': sequenceId,
			                                               'galleryCameraId': 1}, files=files)
			# response = requests.post(pic_upload_andFind)  # for test
			# response = requests.post(tmp_utl, data={
			# 	'startFrame': 0,
			# 	'finishFrame': 4,
			# 	'sequenceId': 20181005001,
			# 	'galleryCameraId': 1
			# })
			global data_
			data_ = eval(eval(response.text)['data'])
			logger.info(data_)
			'''
			test output
			[{'sequenceId': '20181005001', 'cameraId': 1, 'time': '10:38'}, {'sequenceId': '20181005001', 'cameraId': 2, 'time': '1:28'}, {'sequenceId': '20181005001', 'cameraId': 3, 'time': '5:30'}]
			'''
			return HttpResponseRedirect('/main/success')
	else:
		form = PicFrom()
	return render(request, "main/track.html", {'form': form, 'data': data_})


# def file_down(request):
# 	file = open('collected_static/bm.mp4', 'rb')
# 	response = FileResponse(file)
# 	response['Content-Type'] = 'application/octet-stream'
# 	response['Content-Disposition'] = 'attachment;filename="bm.mp4"'
# 	return response


def trace_dot_data_down(request):
	file = open('main/static/main/json/visudata_dotbook.json', 'rb')
	response = FileResponse(file)
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="visudata_dotbook.json"'
	return response


def trace_path_data_down(request):
	file = open('main/static/main/json/visudata_pathbook.json', 'rb')
	response = FileResponse(file)
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="visudata_pathbook.json"'
	return response


def upload(request):
	if request.method == 'POST':
		form = UserUploadForm(request.POST, request.FILES)
		if form.is_valid():
			# username = form.cleaned_data['user_name']
			# head_img = form.cleaned_data['headImg']
			Media(
				username=request.POST.get('username'),
				img=request.FILES.get('img'),
				video=request.FILES.get('video'),
				# django 里面上传文件默认只处理单个文件上传，批量上传的时候request.FILES 的类型
				# 为 MultiValueDict，这种字典类是特殊定义的，要取得list 需要调用 getlist方法:
				time=datetime.now()
			).save()
			
			return HttpResponseRedirect('/main/upload')
	else:
		form = UserUploadForm()
	return render(request, "main/file.html", {'form': form})
