from django import forms
import numpy as np
import pandas as pd
import scipy.stats as stats

from .models import Specie, Log, Background, Transcriptor
import json
from datetime import datetime

class AnalyzeForm(forms.Form):
    specie = forms.ModelChoiceField(
        label='Specie', queryset=Specie.objects.all(), widget=forms.Select())
    cluster = forms.CharField(label='Input locus ID', widget=forms.Textarea())
    cutoff = forms.FloatField(label='Cut off')

    #def __init__(self, *args, **kwargs):
    #    super(AnalyzeForm, self).__init__(*args, **kwargs)

    def analyze(self, key):
        specie = self.cleaned_data['specie']
        cluster = self.cleaned_data['cluster']
        cutoff = self.cleaned_data['cutoff']
        cluster = cluster.split('\r\n')
        size = len(cluster)
        specie = specie.id.split(' ')[0]
        specie = specie.lower()
        specie = specie+'_genome'

        file_name = 'ecr/templates/data/{}.json'.format(key)

        df = pd.DataFrame(list(Background.objects.all().values(
            'id', 'name', 'family', 'motifs', 'reverseComplement', specie)))

        df['cluster'] = 0

        queryset = Log.objects.filter(promoter_id__in=cluster)
        log = pd.DataFrame(list(queryset.values(
            'promoter_id', 'tf', 'upstream', 'downstream', 'mean', 'sumatory')))

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

        if (specie == 'vigna_genome'):
            genome = df.vigna_genome.sum()
        elif (specie == 'glycine_genome'):
            genome =df.glycine_genome.sum()
        elif (specie == 'vitis_genome'):
            genome =df.vitis_genome.sum()

        cluster = df.cluster.sum()

        df['p-value'] = 0
        df['p-value'] = df.apply(lambda x: stats.fisher_exact(
            [[x[specie], x['cluster']], [genome, cluster]])[1], axis=1)


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
            'log': list(queryset),
            'enrichment':enrichment.values.tolist(),
            'size':size,
            'now':now,
        }
        return context


class PromoterMiningForm(forms.Form):
    promoter = forms.CharField(label='PhytoMine Locus ID', widget=forms.Textarea())
    size = forms.IntegerField(label='Promoter size (Max. 5000)', max_value=5000, min_value=1)


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
    locus_id = forms.CharField(label='PhytoMine Locus ID', widget=forms.Textarea())

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