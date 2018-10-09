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
            'id', 'name', 'family', 'motifs', 'reverseComplement', 'vigna_genome')))
        df['cluster'] = 0
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
        df = df.sort_values(by='id')

        base = Log.objects.filter(promoter_id__lte=999)
        queryset = Log.objects.filter(promoter_id__in=cluster)
        base = pd.DataFrame(list(base.values('tf', 'mean', 'sumatory')))
        log = pd.DataFrame(list(queryset.values('tf', 'mean', 'sumatory')))
        log = pd.concat([base, log]).reset_index()
=======
>>>>>>> Stashed changes

        queryset = Log.objects.filter(promoter_id__in=cluster)
        log = pd.DataFrame(list(queryset.values(
            'promoter_id', 'tf', 'upstream', 'downstream', 'mean', 'sumatory')))
<<<<<<< Updated upstream

        enrichment = log.groupby('tf').sum().reset_index()

        tf = Transcriptor.objects.all().exclude(id__in=enrichment.tf)
        tf = pd.DataFrame(list(tf.values('id')))
                                
        tf.rename(columns={'id':'tf'}, inplace=True)
        tf['mean'] = 0
        tf['sumatory'] = 0

        enrichment = pd.concat([enrichment, tf]).reset_index()
        enrichment = enrichment.sort_values(by='tf')
        df = df.sort_values(by='id')
        print (enrichment)
        df['cluster'] = enrichment['sumatory']
        print(df)
=======
>>>>>>> Stashed changes

        enrichment = log.groupby('tf').sum().reset_index()

        tf = Transcriptor.objects.all().exclude(id__in=enrichment.tf)
        tf = pd.DataFrame(list(tf.values('id')))
                                
        tf.rename(columns={'id':'tf'}, inplace=True)
        tf['mean'] = 0
        tf['sumatory'] = 0

        enrichment = pd.concat([enrichment, tf]).reset_index()
        enrichment = enrichment.sort_values(by='tf')
        df = df.sort_values(by='id')
        print (enrichment)
        df['cluster'] = enrichment['sumatory']
        print(df)
>>>>>>> 32996c2a7c02a00541f9c6c5b3783996dd527eb7

        print (log)
        log = log.groupby('tf').sum()

        enrichment = log.sort_values(by='tf')
        
        print (enrichment)
        df['cluster'] = enrichment['sumatory'].values.copy()
        print(df)
        

        context = {
            'success': True,
            'dataframe' : df.to_html(classes=['table', 'table-striped', 'table-bordered', 'table-hover']),
            'specie': self.cleaned_data['specie'],
            'table': list(queryset),
            'log': log.to_html(classes=['table', 'table-striped', 'table-bordered', 'table-hover']),
        }

        return context
