from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


#when the server gets the request, return http response hello world
def myView(request):
    return HttpResponse('Hello, World')