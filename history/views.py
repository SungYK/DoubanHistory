from django.shortcuts import render
from django.http import HttpResponse
from .models import Subject
import json

def index(request):
    subject_list = Subject.objects.filter(playing=1).order_by('daily_rank')

    lst = []
    for i in subject_list:
        lst.append([i.pk, i.title, i.original_title, i.history_rating])

    return render(request, 'history/index.html', context={'subject_list':subject_list, 'lst':lst})
