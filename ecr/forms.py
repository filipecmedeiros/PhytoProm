from django import forms
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

from .models import Specie, Log, Background, LogTable


class AnalyzeForm(forms.Form):
    specie = forms.ModelChoiceField(
        label='Specie', queryset=Specie.objects.all(), widget=forms.Select())
    cluster = forms.CharField(label='Cluster', widget=forms.Textarea())
    cutoff = forms.IntegerField(label='Cut off')

    def analyze(self):
        cluster = self.cleaned_data['cluster']
        cutoff = self.cleaned_data['cutoff']


        cluster = cluster.split('\r\n')
        context = {
            'success':True,
            'specie':self.cleaned_data['specie'],
            'table':LogTable(Log.objects.filter(promoter_id__in=cluster)),
        }

        return context

