from django.shortcuts import render
from django.http import HttpResponse
from .models import Subject
import json

def index(request):
    subject_list = Subject.objects.filter(playing=1).order_by('daily_rank')

    lst = []
    for i in subject_list:
        lst.append([i.pk, i.title, i.original_title, i.history_rating])

    return render(request, 'history/index.html', context={'lst':lst})

def about(request):
    return render(request, 'history/about.html')

def search(request):
    q = request.GET.get('q')
    if q == None or q == '':
        return render(request, 'history/search.html', context={'query':q, 'lst':[]})

    subject_list = Subject.objects.filter(title__icontains=q)

    lst = []
    for i in subject_list:
        lst.append([i.pk, i.title, i.original_title, i.history_rating])

    return render(request, 'history/search.html', context={'query':q, 'lst':lst})