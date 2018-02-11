from django.shortcuts import render
from django.http import HttpResponse
from .models import Subject
import json

def index(request):
    subject_list = Subject.objects.filter(playing=1).order_by('daily_rank')

    return render(request, 'history/index.html', context={'subject_list':subject_list})
