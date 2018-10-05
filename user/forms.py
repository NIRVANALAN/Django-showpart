from django import forms
from django.contrib.auth.models import User
import re


# Create your views here.
def email_check(email):
	pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
	return re.match(pattern, email)


class RegistrationForm(forms.Form):
	username = forms.CharField(label='Username', max_length=50)
	email = forms.EmailField(label='Email', )
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
	
	def clean_username(self):
		username = self.cleaned_data.get('username')
		if len(username) < 6:
			raise forms.ValidationError("Your username must be at least 6 characters long.")
		elif len(username) > 50:
			raise forms.ValidationError("Your username is too long.")
		else:
			filter_result = User.objects.filter(username__exact=username)
			if len(filter_result) > 0:
				raise forms.ValidationError("Your username already exists.")
		return username
	
	def clean_email(self):
		email = self.cleaned_data.get('email')
		if email_check(email):
			filter_result = User.objects.filter(email__exact=email)
			if len(filter_result) > 0:
				raise forms.ValidationError("Your email already exists.")
		else:
			raise forms.ValidationError("Please enter a valid email.")
		return email
	
	def clean_password1(self):
		password1 = self.cleaned_data.get('password1')
		if len(password1) < 6:
			raise forms.ValidationError("Your password is too short.")
		elif len(password1) > 20:
			raise forms.ValidationError("Your password is too long.")
		return password1
	
	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Password mismatch, enter again please")
		return password2


class LoginForm(forms.Form):
	username = forms.CharField(label='username', max_length=50)
	# use widget
	password = forms.CharField(label='password', widget=forms.PasswordInput)
	
	# user cleaned data to define custom validation data
	def clear_username(self):
		username = self.cleaned_data.get('username')
		if email_check(username):
			#
			filter_result = User.objects.filter(email__exact=username)
			if not filter_result:
				raise forms.ValidationError('This email does not exist')
		else:
			filter_result = User.objects.filter(username__exact=username)
			if not filter_result:
				raise forms.ValidationError('This username does not exist, please register first')
		return username


class ProfileForm(forms.Form):
	first_name = forms.CharField(label='First Name', max_length=50, required=False)
	last_name = forms.CharField(label='Last Name', max_length=50, required=False)
	org = forms.CharField(label='Organization', max_length=50, required=False)
	telephone = forms.CharField(label='Telephone', max_length=50, required=False)
