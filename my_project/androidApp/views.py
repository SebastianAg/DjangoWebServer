# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
