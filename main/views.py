from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from main.models import BlogPost, blogPostToForm, UserForm, Media
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
	return render(request, 'main/index.html')


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


def track(request):
	return render(request,"main/track.html")


def file_down(request):
	file = open('collected_static/bm.mp4', 'rb')
	response = FileResponse(file)
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="bm.mp4"'
	return response


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
		form = UserForm(request.POST, request.FILES)
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
		form = UserForm()
	return render(request, "main/register.html", {'form': form})
