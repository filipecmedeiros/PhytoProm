from django import forms
import numpy as np
import pandas as pd
import scipy.stats as stats

from .models import Specie, Log, Background, Transcriptor
import json

class AnalyzeForm(forms.Form):
    specie = forms.ModelChoiceField(
        label='Specie', queryset=Specie.objects.all(), widget=forms.Select())
    cluster = forms.CharField(label='Cluster', widget=forms.Textarea())
    cutoff = forms.FloatField(label='Cut off')

    def analyze(self):
        cluster = self.cleaned_data['cluster']
        cutoff = self.cleaned_data['cutoff']
        cluster = cluster.split('\r\n')

        df = pd.DataFrame(list(Background.objects.all().values(
            'id', 'name', 'family', 'motifs', 'reverseComplement', 'vigna_genome')))
        df['cluster'] = 0

        queryset = Log.objects.filter(promoter_id__in=cluster)
        log = pd.DataFrame(list(queryset.values(
            'promoter_id', 'tf', 'upstream', 'downstream', 'mean', 'sumatory')))

        log.to_json(r'ecr/templates/data/analysis.json', orient='records')


        enrichment = log.groupby('tf').sum().reset_index()

        tf = Transcriptor.objects.all().exclude(id__in=enrichment.tf)
        tf = pd.DataFrame(list(tf.values('id')))
        tf.rename(columns={'id': 'tf'}, inplace=True)
        tf['mean'] = 0
        tf['sumatory'] = 0

        enrichment = pd.concat([enrichment, tf])
        enrichment = enrichment.sort_values(by='tf')
        enrichment = enrichment.reset_index(drop=True)

        df = df.sort_values(by='id')
        df = df.reset_index(drop=True)

        df['cluster'] = enrichment['sumatory']

        vigna_genome = df.vigna_genome.sum()
        cluster = df.cluster.sum()

        df['p-value'] = 0
        df['p-value'] = df.apply(lambda x: stats.fisher_exact(
            [[x['vigna_genome'], x['cluster']], [vigna_genome, cluster]])[1], axis=1)


        enrichment = df.copy()

        enrichment = enrichment.loc[enrichment['p-value'] <= cutoff]

        context = {
            'success': True,
            'dataframe':df.values.tolist(),
            'specie': self.cleaned_data['specie'],
            'log': list(queryset),
            'enrichment':enrichment.values.tolist(),
        }
        return context
