__author__ = 'shaked'

from django.template import Template, Context
from django.http import HttpResponse
from django.template import RequestContext, loader


from django.shortcuts import render

def index(request):
    user = Person()
    user.nickname = 'shaked'
    context = {'title': 'My Web Title',
               'is_authenticated': True
    }
    return render(request, 'templates/core/index.html', context)

def login(request):
    return HttpResponse("Hello, world. You're at the login!!")
