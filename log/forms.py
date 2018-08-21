from django import forms

from django.core.mail import send_mail
from django.conf import settings


class AnalysisForm (forms.Form):

	gene = forms.CharField(label='dataset', widget=forms.Textarea())

	def returnLog(self):
		locus = self.cleaned_data['dataset']
		locus.split('\n')

		return (True, locus)
