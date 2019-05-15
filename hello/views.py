import requests
from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Create your views here.
def index(request):
	file = open('html.txt','r')
	response = HttpResponse()
	text = file.read()
	return HttpResponse(text)
def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


