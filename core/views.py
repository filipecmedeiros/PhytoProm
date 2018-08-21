from django.shortcuts import render
from django.views.generic.edit import FormView

from log.forms import AnalysisForm
from log.models import Log
# Create your views here.
class Index (FormView):
	template_name = 'index.html'

	def get(self, request, *args, **kwargs):
		self.context = {'genes':Log.objects.filter(gene='Vigun01g000200')}
		print (self.context)
		self.success = True
		form = AnalysisForm(self.request.GET or None)
		if form.is_valid():
			self.success = True
			self.context = Log.objects.filter(gene__icontains=form.cleaned_data['query'])[:10]
		
		return self.render_to_response(self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(Index, self).get_context_data(**kwargs)
		context.update({
			'context':self.context
			})
		return context
	
index = Index.as_view()