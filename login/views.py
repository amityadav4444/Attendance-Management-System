from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseNotFound
from login.models import TimeTable,Student
from login import models
from django.db.models import F
from datetime import datetime
from django.template import loader
from django.urls import reverse
from django.http import HttpResponseRedirect
from login import forms
from collections import defaultdict
from datetime import time, timedelta, date
import re
from .forms import ChangePassword
from django.contrib.auth.models import User


# Create your views here.

def home(request):
	username = None
	if request.user.is_authenticated:
		username = request.user
		
	data = TimeTable.objects.get(user=username)
	holidays = models.Holiday.objects.filter(date__month__gte=date.today().month)
	context = {'data': data, 'holidays': holidays}
	return render(request, 'login/index.html',context)


def markAttendance(request, stri, st):
	# WRITE CODE TO CHECK WHETHER ATTENDANCE CAN BE ADDED OR NOT
	if(not request.user.is_authenticated):
		return render(request, 'login/404.html')
	
	day = date.today().weekday()
	if(st[0]!='-'):
		time= int(st[1])
		day=int(st[0])
	else:
		time=int(st[2])
		day=-1*int(st[1])


	date_now = datetime.now()
	date_mark=datetime(date.today().year,date.today().month,date.today().day,8,15,0)+timedelta(minutes=55*(time-1))-timedelta(days=(date.today().weekday()-day))
	
	if(time>3):
		date_mark=date_mark+timedelta(minutes=30)
	
	if(date_now<=date_mark):
		alert = 'alert("You can not mark attendance today !!");';
		return HttpResponse('<script> alert("You can not mark attendance today !! data<date_mark"); </script>');
	
	
	#print(date_mark)

	if(date_now>=date_mark+timedelta(days=3)+timedelta(hours=7)):
		alert = 'alert("You can not mark attendance today !!");';
		print(str(date_now)+" "+str(date_mark+timedelta(days=3)))
		return HttpResponse('<script> alert("You can not mark attendance today!! data>date_mark+3"); </script>');

	list_of_string = stri.lower().split(' ',1)
	if(len(models.Attendance_table.objects.filter(section__section_name=list_of_string[0], subject__subject_name=list_of_string[1],attendance__date=date_mark))>0):
		alert = 'alert("You can not mark attendance today !!");';
		return HttpResponse('<script> alert("You can not mark attendance today list_of_students!! len(obj)>2"); </script>');
	
	list = models.Student.objects.filter(section__section_name=stri.split(' ',1)[0].lower())
	form = forms.AttForm()
	#date_now = date(date_mark.year, date_mark.month, date_mark.day)
	context = {
		'data':list,
		'form':form,
		'stri':stri,
		'st':st,
		'date':date_mark,
	}
	return render(request, 'login/students.html', context)
	

def analyze(request, stri):
	
	if(not request.user.is_authenticated):
		return render(request, 'login/404.html')
	total=[]
	percentage=[]
	list_of_string = stri.lower().split(' ',1)
	list = models.Student.objects.filter(section__section_name=list_of_string[0])
	list_of_students=[]
	obj = models.Attendance_table.objects.get(section__section_name=list_of_string[0], subject__subject_name = list_of_string[1])
	for i in list:
		data = obj.attendance.filter(student=i);
		list_of_students.append(data)
		s=0
		c=0
		for j in data:
			s+=j.att
			c+=1
		total.append(s)
		if c!=0:
			percentage.append(s*100/c)
		else:
			return render(request, 'login/404.html')
	context = {
		'stri': stri,
		'list': list_of_students,
		'total':total,
		'percentage':percentage,
	}
	return render(request, 'login/analyze.html', context)
	
	
def add(request, stri, st):
	# if this is a POST request we need to process the form data
	#if request.method == 'POST':
	# create a form instance and populate it with data from the request:
	'''
	list_of_string = stri.lower().split(' ',1)
	if(len(models.Attendance_table.objects.filter(section__section_name=list_of_string[0], subject__subject_name=list_of_string[1],attendance__date=date.today()))>0):
		alert = 'alert("You can not mark attendance today !!");';
		return HttpResponse('<script> alert("You can not mark attendance today !!"); </script>');
	'''
	if(st[0]!='-'):
		time= int(st[1])
		day=int(st[0])
	else:
		time=int(st[2])
		day=-1*int(st[1])
	date_mark=datetime(date.today().year,date.today().month,date.today().day,8,15,0)+timedelta(minutes=55*(time-1))-timedelta(days=(date.today().weekday()-day))
	
	if(time>3):
		date_mark=date_mark+timedelta(minutes=30)
	
	form = forms.AttForm(request.POST)
	# check whether it's valid:
	if form.is_valid():
		# process the data in form.cleaned_data as required
		# ...
		# redirect to a new URL:
		j=0
		list_of_string = stri.lower().split(' ',1)
		for i in models.Student.objects.filter(section__section_name=list_of_string[0]):
			boolean = form.cleaned_data['your_att%s' %j]
			if(boolean):
				attendance = models.Attendance_cell.objects.create(student=i, date=date_mark, att=1)
				models.Attendance_table.objects.get(section__section_name=list_of_string[0],subject__subject_name=list_of_string[1]).attendance.add(attendance)
			else:
				attendance = models.Attendance_cell.objects.create(student=i, date=date_mark, att=0)
				models.Attendance_table.objects.get(section__section_name=list_of_string[0],subject__subject_name=list_of_string[1]).attendance.add(attendance)
			print(models.Attendance_cell.objects.filter(student=i, date=date_mark))
			j+=1;

	return HttpResponseRedirect('../../../home/')


def update(request):

	for i in models.Section.objects.all():
		for j in models.Subject.objects.filter(semester=i.semester):
			if(len(models.Attendance_table.objects.filter(section=i, subject=j))>0):
				continue
			joe = models.Attendance_table.objects.create(section=i, subject=j)
			print(joe)
	
	return HttpResponse('<h2> +1')


def ChangePassword(request):
	if request.method == 'POST':
		ur=request.user.username
		u = User.objects.get(username=ur)
		form = forms.ChangePassword(request.POST)
		if form.is_valid():
			ch=form.cleaned_data['newPassword']
			u.set_password(ch)
			u.save()
			return HttpResponseRedirect('../../../')
	else:
		form = ChangePassword(request.POST)

	return render(request, 'login/changepassword.html', {'form': form})

def CP(request):
	form = forms.ChangePassword(request.POST)
	return render(request, 'login/changpassword.html', {'form': form})