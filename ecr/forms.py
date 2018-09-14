from django import forms

from .models import Specie, Log, Background, BackgroundTable


class AnalyzeForm(forms.Form):
    specie = forms.ModelChoiceField(
        label='Specie', queryset=Specie.objects.all(), widget=forms.Select())
    cluster = forms.CharField(label='Cluster', widget=forms.Textarea())
    cutoff = forms.IntegerField(label='Cut off')

    def analyze(self):
        context = {
            'success':True,
            'specie':self.cleaned_data['specie'],
            'cluster':self.cleaned_data['cluster'],
            'cutoff':self.cleaned_data['cutoff'],
            'log': Log.objects.filter(promoter=cluster),
            'table':BackgroundTable(Background.objects.all()),
        }

        return context

