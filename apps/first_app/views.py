# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from models import User
from django.core.urlresolvers import reverse
from django.views.generic.edit import View
import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import Q
import math
from datetime import datetime
from pytz import timezone
import pytz
utc = pytz.utc
utc.zone
'UTC'
central = timezone('US/Central')
totalUsers = {}
usersCount = {}

def index(request):
    global searchName, totalUsers, usersCount
    totalUsers = User.objects.all()
    usersCount = (totalUsers.count() / 8) + (totalUsers.count() % 8 > 0)
    context = {
		'users': User.objects.all()[:8],
		'usersCount': usersCount * "x"
	}
    return render(request, 'first_app/index.html', context)

def new(request):
    return render(request, 'first_app/new.html')

def create(request):
    print('entered create')
    new_user = User.objects.create(
        first_name=request.POST['first_name'], 
        last_name=request.POST['last_name'], 
        email=request.POST['email'])
    print(new_user.first_name)
    print(new_user.last_name)
    print(new_user.email)
    print(new_user.id)
    return redirect('/')

userStart = {}
userEnd = {}

class ChangePage(View):
	def get(self, request):
		context = {
			'users': totalUsers[userStart: userEnd],
			'usersCount': usersCount * "x"
		}
		return render(request, 'first_app/changePageAjax.html', context)
	def post(self, request):
		global userStart, userEnd, usersCount
		userStart = int(request.POST['pageNumber']) * 8
		userEnd = int(request.POST['pageNumber']) * 8 + 8
		usersCount = (totalUsers.count() / 8) + (totalUsers.count() % 8 > 0)
		return redirect(reverse('first_app:changePage'))

searchName = {}

class SearchName(View):
	def get(self, request):
		context = {
			'users': searchName,
			'usersCount': usersCount * "x"
		}
		return render(request, 'first_app/changePageAjax.html', context)
	def post(self, request):
		global searchName, totalUsers, usersCount
		totalUsers = User.objects.filter( Q(first_name__icontains= request.POST['name']) | Q(last_name__icontains = request.POST['name']) )
		searchName = totalUsers[:8]
		usersCount = (totalUsers.count() / 8) + (totalUsers.count() % 8 > 0)
		return redirect(reverse('first_app:searchName'))

class StartDate(View):
	def get(self, request):
		context = {
			'users': searchName,
			'usersCount': usersCount * 'x'
		}
		return render(request, 'first_app/changePageAjax.html', context)
	def post(self, request):
		global searchName, totalUsers, usersCount
		start = central.localize( datetime.strptime(request.POST['startDate'], '%Y-%m-%d')  )
		end = central.localize( datetime.strptime(request.POST['endDate'], '%Y-%m-%d') )
		totalUsers = User.objects.filter(created_at__gte=start, created_at__lte=end)
		searchName = totalUsers[:10]
		usersCount = (totalUsers.count() / 8) + (totalUsers.count() % 8 > 0)
		return redirect(reverse('first_app:searchName'))
