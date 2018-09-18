from django import forms
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

from .models import Specie, Log, Background


class AnalyzeForm(forms.Form):
    specie = forms.ModelChoiceField(
        label='Specie', queryset=Specie.objects.all(), widget=forms.Select())
    cluster = forms.CharField(label='Cluster', widget=forms.Textarea())
    cutoff = forms.IntegerField(label='Cut off')

    def analyze(self):
        cluster = self.cleaned_data['cluster']
        cutoff = self.cleaned_data['cutoff']
        cluster = cluster.split('\r\n')

        queryset = Log.objects.filter(promoter_id__in=cluster)
        df = pd.DataFrame(list(Background.objects.all().values(
            'id', 'name', 'family', 'motifs', 'reverseComplement', 'vigna_genome')))
        df['cluster'] = 0
        analyze = pd.DataFrame(list(queryset.values(
            'promoter_id', 'tf', 'upstream', 'downstream', 'mean', 'sumatory')))
        i = analyze.groupby('promoter_id').count()
        
        #df['cluster'] = i['sumatory']


        context = {
            'success': True,
            'specie': self.cleaned_data['specie'],
            'table': list(queryset),
            'dataframe': df.to_html(classes=['table', 'table-striped', 'table-bordered', 'table-hover']),
        }

        return context
