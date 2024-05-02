# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.shortcuts import render

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Data
from django.forms.models import model_to_dict

# Create your views here.

def run(request):
    if 'action' in request.GET:
        action = request.GET['action']
	    #Start button
        if action == 'start':
            print("start")
        #stop button
        elif action == 'stop':
            print("stop")
        #send button
        elif action == 'send':
            print("send")
    return HttpResponse('')

def upload(request):
    if 'upload' in request.GET:
        upload = request.GET['upload']
	    #test button
        if upload == 'test':
            print("uploading")
    return HttpResponse('')
    
def text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition']= 'attachment; filename=routes.txt'
    
    lines =["This is line 1\n",
    "This is line 2\n"]
    #add link to jennie's route file
    
    #write to txt
    response.writelines(lines)
    return response
    
def all_data(request):
    data_list = Data.objects.all()
    for i in data_list:
        print(model_to_dict(i))
    return HttpResponse('')
    

