import requests
from django.shortcuts import render
from django.http import HttpResponse
import os
from .models import Greeting

# Create your views here.
def index(request):
	# file = open(os.path.r,'r')
	# response = HttpResponse()
	# text = file.read()
	return HttpResponse(str(os.os.getcwd()))
def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


