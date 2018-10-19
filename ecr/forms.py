from django import forms
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

from .models import Specie, Log, Background, Transcriptor


class AnalyzeForm(forms.Form):
    specie = forms.ModelChoiceField(
        label='Specie', queryset=Specie.objects.all(), widget=forms.Select())
    cluster = forms.CharField(label='Cluster', widget=forms.Textarea())
    cutoff = forms.IntegerField(label='Cut off')

    def analyze(self):
        cluster = self.cleaned_data['cluster']
        cutoff = self.cleaned_data['cutoff']
        cluster = cluster.split('\r\n')

        df = pd.DataFrame(list(Background.objects.all().values(
            'id', 'family_id', 'motifs', 'reverseComplement', 'vigna_genome')))
        


        i = df.groupby('tf_id').sum()
        df = df.groupby('tf_id')
        df['vigna_genome'] = i['sumatory'].values.copy()
        df['Cluster'] = 0

        context = {
            'success': True,
            'dataframe': df.to_html(classes=['table', 'table-striped', 'table-bordered', 'table-hover']),
            'specie': self.cleaned_data['specie'],
            #'table': list(queryset),
            #'log': log.to_html(classes=['table', 'table-striped', 'table-bordered', 'table-hover']),
        }

        return context
