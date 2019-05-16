from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse
from django.http import JsonResponse, Http404

from .forms import AnalyzeForm, PromoterMiningForm
import json

# Create your views here.
def index(request):
    success = False

    form = AnalyzeForm(request.POST or None, initial={'cutoff':0.05})
    context = {
        'title': 'Analyze',
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

def promoter(request):
    success = False

    form = PromoterMiningForm(request.POST or None, initial={'size':1000})
    context = {
        'title':'Promoter Mining',
        'form':form,
        'success':success,
    }

    if form.is_valid():
        context['promoters'] = form.mine()
        context['success'] = True
    
    return render (request, 'ecr/promoter.html', context)