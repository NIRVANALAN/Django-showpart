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
# import logging
import json
from django.utils import timezone

pic_upload_add = 'http://192.168.254.117:8806/picture/uploadAndFind'
pic_upload_andFind = 'http://172.20.10.2:8806/picture/uploadAndFind'

frame = 1
sequenceId = '20190508001'
cameraId = 2

# logging
# logger = logging.getLogger('django')
# logger.info('logger "django" start')


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
def visuService(request):
	return render(request, "main/visu.html")


def class_router(request):
	return render(request, "main/class.html")


def codes(request):
	return render(request, "main/codes.html")


def paint(request):
	return render(request, 'main/paint.html')


data = [{"sequenceId": "20190508001", "cameraId": 2, "boxes": "[0, 0, 386, 1052, 0]", "frame": 2640,
         "similarities": 0.7460789036139179,
         "pic_path": "./data/Pictures/20190508001/2/2640.jpg"},
        {"sequenceId": "20190508001", "cameraId": 2, "boxes": "[668, 111, 951, 1017, 0]", "frame": 2670,
         "similarities": 0.8126308847975244,
         "pic_path": "./data/Pictures/20190508001/2/2670.jpg"}]


def track(request):
	_data = None
	if request.method == 'POST':
		form = PicFrom(request.POST, request.FILES)
		if form.is_valid():
			# username = form.cleaned_data['user_name']
			# head_img = form.cleaned_data['headImg']
			Pic(
				img=request.FILES.get('img'),
				time=timezone.now()
			).save()
			files = {'file': open('./Media/img/' + request.FILES.get('img').name, 'rb')}
			# response = requests.post(pic_upload_andFind,
			#                          data={'startFrame': 0, 'finishFrame': 6000, 'sequenceId': sequenceId,
			#                                'galleryCameraId': int(request.POST['camera'])}, files=files)
			# response = requests.post(pic_upload_andFind)  # for test
			
			# response = requests.post(tmp_utl, data={
			# 	'startFrame': 0,
			# 	'finishFrame': 4,
			# 	'sequenceId': 20181005001,
			# 	'galleryCameraId': 1
			# })
			global data
			# data = eval(eval(response.text)['data'])
			# logger.info(data_)
			# data = eval(open('apps/main/res.txt').readline())
			for i in data:
				i['frame'] = '{}:{}'.format(int(i['frame'] / 30 // 60), int(i['frame'] / 30) % 60)
				pass
			'''
			test output
			{"sequenceId": "20190508001", "cameraId": 1, "boxes": "[663, 71, 859, 696, 0]", "frame": 4110, "similarities": 0.6661713832802965}
			'''
			return HttpResponseRedirect('/main/success')
	else:
		form = PicFrom()
	return render(request, "main/track.html", {'form': form, 'data': data})


def save_info(request):
	if request.method == 'POST':
		info = request.POST['cameraInfo']
		info = json.load(info)
		pass
	pass
# def file_down(request):
# 	file = open('static/bm.mp4', 'rb')
# 	response = FileResponse(file)
# 	response['Content-Type'] = 'application/octet-stream'
# 	response['Content-Disposition'] = 'attachment;filename="bm.mp4"'
# 	return response


def trace_dot_data_down(request):
	file = open('main/static/main/json/dotbook.json', 'rb')
	response = FileResponse(file)
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="dotbook.json"'
	return response


def trace_path_data_down(request):
	file = open('main/static/main/json/pathbook.json', 'rb')
	response = FileResponse(file)
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="pathbook.json"'
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
