from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import auth
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required
def profile(request, pk):
	user = get_object_or_404(User, pk=pk)
	return render(request, 'users/profile.html', {'user': user})


@login_required
def profile_update(request, pk):
	user = get_object_or_404(User, pk=pk)
	user_profile = get_object_or_404(UserProfile, user=user)
	
	if request.method == "POST":
		form = ProfileForm(request.POST)
		
		if form.is_valid():
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.save()
			
			user_profile.org = form.cleaned_data['org']
			user_profile.telephone = form.cleaned_data['telephone']
			user_profile.save()
			
			return HttpResponseRedirect(reverse('users:profile', args=[user.id]))
	else:
		default_data = {'first_name': user.first_name, 'last_name': user.last_name, 'org': user_profile.org,
		                'telephone': user_profile.telephone, }
		form = ProfileForm(default_data)
	
	return render(request, 'users/profile_update.html', {'form': form, 'user': user})


def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password2']
			user = User.objects.create_user(username, password, email)
			# do not need to save'
			user_profile = UserProfile(user=user)
			user_profile.save()
			return HttpResponseRedirect("/account/login/")
	else:
		form = RegistrationForm()
	return render(request, 'users/registration.html', {'form': form})


def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = auth.authenticate(username=username, password=password)
			if user is not None and user.is_active:
				auth.login(request, user)
				# return HttpResponseRedirect(reverse('users:profile', args=[user.id]))
				return HttpResponseRedirect('/main/index')
		else:
			# 登陆失败
			return render(request, 'users/login.html', {'form': form, 'message': 'Wrong password. Please try again.'})
	
	else:
		form = LoginForm()
		return render(request, 'users/login.html', {'form': form})


def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/account/login')
