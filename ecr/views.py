from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse

from .forms import AnalyzeForm

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