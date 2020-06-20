from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse
from django.http import JsonResponse, Http404, HttpResponse

from .forms import AnalyzeForm, PromoterMiningForm, MiningForm, SuggestionsForm
import json

# Create your views here.
def index(request):
    return render(request, 'ecr/index.html')


def analyze(request):
    success = False

    form = AnalyzeForm(request.POST or None, initial={'cutoff':0.05})
    context = {
        'title': 'Exploratory Analysis',
        'form':form,
        'success':success
    }

    if form.is_valid():
        context['key'] = request.session._get_or_create_session_key()
        context = form.analyze(context['key'])

    return render(request, 'ecr/analyze.html', context)


def api(request, key=None):
    json_file = 'ecr/templates/data/{}.json'.format(key)
    json_data=open(json_file)
    data = json.load(json_data)
    return JsonResponse(data, safe=False)


def promoter(request):
    success = False

    form = PromoterMiningForm(request.POST or None, initial={'size':1000})
    context = {
        'title':'Promoter Download',
        'form':form,
        'success':success,
    }

    if form.is_valid():
        context['promoters'] = form.mine()
        context['success'] = True

    return render(request, 'ecr/promoter.html', context)


def protein(request):
    success = False

    form = MiningForm(request.POST or None)
    context = {
        'title':'Protein Download',
        'form':form,
        'success':success,
    }

    if form.is_valid():
        context['output'] = form.mine(category="Protein")
        context['success'] = True

    return render(request, 'ecr/mining.html', context)


def transcript(request):
    success = False

    form = MiningForm(request.POST or None)
    context = {
        'title':'Transcript Download',
        'form':form,
        'success':success,
    }

    if form.is_valid():
        context['output'] = form.mine(category="Transcript")
        context['success'] = True
    
    return render(request, 'ecr/mining.html', context)

def documentation(request):
    return render(request, 'ecr/documentation.html')

def suggestions(request):
    success = False
    form = SuggestionsForm(request.POST or None)

    context = {
        'title': 'Suggestions',
        'form': form,
        'success': success,
    }

    if form.is_valid():
        context['success'] = form.send_mail()
        context['output'] = 'Your message was sent. Thank you!'
    return render(request, 'ecr/suggestions.html', context)
