from django import forms

from django.core.mail import send_mail
from django.conf import settings

import numpy as np
import pandas as pd
import scipy.stats as stats

from .models import Specie, Log, Background, Transcriptor
import json
from datetime import datetime


class AnalyzeForm(forms.Form):
    specie = forms.ModelChoiceField(
        label='Specie', queryset=Specie.objects.all(), widget=forms.Select())
    cluster = forms.CharField(label='Input Phytozome v12.1 Locus ID', widget=forms.Textarea())
    cutoff = forms.FloatField(label='Cut off ≤')

    def analyze(self, key):
        specie = self.cleaned_data['specie']
        cluster = self.cleaned_data['cluster']
        cutoff = self.cleaned_data['cutoff']
        cluster = cluster.split('\r\n')
        size = len(cluster)
        specie = specie.id
        specie_ = specie.lower().replace(' ', '_')

        file_name = 'ecr/templates/data/{}.json'.format(key)

        df = pd.DataFrame(list(Background.objects.all().values(
            'id', 'name', 'family', 'motifs', 'reverseComplement', specie_)))

        df['cluster'] = 0

        log = pd.read_csv('ecr/logs/{} genome.csv'.format(specie),
            sep=',', index_col=0)
        log.drop(columns=['name', 'family_id', 'motifs', 'reverseComplement'],
            axis=1, inplace=True)
        log = log[log.promoter_id.isin(cluster)]
        
        enrichment = log.groupby('tf').sum().reset_index()

        tf = Transcriptor.objects.all().exclude(id__in=enrichment.tf)
        tf = pd.DataFrame(list(tf.values('id')))
        tf.rename(columns={'id': 'tf'}, inplace=True)
        tf['mean'] = 0
        tf['sum'] = 0

        enrichment = pd.concat([enrichment, tf])
        enrichment = enrichment.sort_values(by='tf')
        enrichment = enrichment.reset_index(drop=True)

        df = df.sort_values(by='id')
        df = df.reset_index(drop=True)

        df['cluster'] = enrichment['sum']

        genome = df[specie_].sum()

        cluster = df.cluster.sum()

        df['p-value'] = 0
        df['p-value'] = df.apply(lambda x: stats.fisher_exact(
            [[x[specie_], x['cluster']], [genome, cluster]])[1], axis=1)
        df['p-value'] = df['p-value'].apply(lambda x: round(x,4))
        enrichment = df.copy()

        enrichment = enrichment.loc[enrichment['p-value'] <= cutoff]
        
        now = datetime.now()
        now = now.strftime('%Y%m%d%H%M%S')
        graphic = pd.merge(log, enrichment, left_on='tf', right_on='id', how='inner')
        graphic.to_json(file_name, orient='records')

        context = {
            'title': 'Exploratory Analysis',
            'success': True,
            'dataframe':df.values.tolist(),
            'specie': self.cleaned_data['specie'],
            'log': log.values.tolist(),
            'enrichment':enrichment.values.tolist(),
            'size':size,
            'now':now,
            'key':key
        }
        return context


class PromoterMiningForm(forms.Form):
    promoter = forms.CharField(label='Phytozome v12.1 Locus ID', widget=forms.Textarea())
    size = forms.IntegerField(label='Promoter size (Max. 5000 nt)', max_value=5000, min_value=1)


    def mine (self):
        promoters = self.cleaned_data['promoter']
        size = self.cleaned_data['size']
        promoters = promoters.split('\r\n')
        promoters = {'id':promoters}
        df = pd.DataFrame(promoters)
        
        from intermine.webservice import Service
        service = Service("https://phytozome.jgi.doe.gov/phytomine/service")

        query = service.new_query("Gene")

        query.add_view(
            "name", "primaryIdentifier", "secondaryIdentifier", "length",
            "flankingRegions.length", "flankingRegions.includeGene",
            "flankingRegions.direction", "flankingRegions.primaryIdentifier",
            "flankingRegions.sequence.length", "flankingRegions.sequence.residues"
        )

        query.add_constraint("flankingRegions.length", "=", "5000", code = "A")
        query.add_constraint("flankingRegions.includeGene", "=", "false", code = "B")
        query.add_constraint("flankingRegions.direction", "=", "upstream", code = "C")
        
        output = ''
        for i in df['id']:
            query.add_constraint("name", "=", i, code = "D")
            for row in query.rows():
                output = output + (">"+str(row["primaryIdentifier"])+'\n'+\
                                    str(row["flankingRegions.sequence.residues"][5000-size:])+'\n')

        return output


class MiningForm(forms.Form):
    locus_id = forms.CharField(label='Phytozome v12.1 Locus ID', widget=forms.Textarea())

    def mine (self, category):
        locus_id = self.cleaned_data['locus_id']
        locus_id = locus_id.split('\r\n')
        locus_id = {'id':locus_id}
        df = pd.DataFrame(locus_id)
        
        from intermine.webservice import Service
        service = Service("https://phytozome.jgi.doe.gov/phytomine/service")

        query = service.new_query(category)

        query.add_view(
            "name", "primaryIdentifier", "secondaryIdentifier", "sequence.residues"
        )
        
        output = ''
        for i in df['id']:
            query.add_constraint("name", "=", i, code = "D")
            for row in query.rows():
                output = output + (">"+str(row["primaryIdentifier"])+'\n'+\
                                    row["sequence.residues"]+'\n')

        return output

class SuggestionsForm (forms.Form):

    name = forms.CharField(label='Name')
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Message', widget=forms.Textarea())

    def send_mail(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        message = 'Name: {0}\nEmail: {1}\n{2}'.format(name, email, message)
        send_mail('PhytoProm suggestions', message,
            settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
        return True
