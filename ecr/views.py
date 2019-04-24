from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse
from django.http import JsonResponse, Http404

from .forms import AnalyzeForm
import json

# Create your views here.
def index(request):
    success = False

    form = AnalyzeForm(request.POST or None)
    context = {
        'form':form,
        'success':success,
    }

    if form.is_valid():
        context = form.analyze()
    
    return render (request, 'ecr/index.html', context)

def api(request):
    json_file = 'ecr/templates/data/analysis.json'
    json_data=open(json_file)
    data = json.load(json_data)
    return JsonResponse(data, safe=False)