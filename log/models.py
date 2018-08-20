from django.db import models

# Create your models here.
class Log(models.Model):
	gene = models.CharField('Gene', max_length=255, null=False, blank=False)
	tf_id = models.CharField('ID', max_length=255, null=False, blank=False)
	name = models.CharField('Nome', max_length=255, null=False, blank=False)
	motifs = models.CharField('Motivos', max_length=10000, null=False, blank=False)
	reverseComplement = models.CharField('Complemento reverso', max_length=10000, null=False, blank=False)
	upstream = models.TextField('Upstream', max_length=10000)
	downstream = models.TextField('Downstream', max_length=10000)
	mean = models.FloatField('Média')
	sumatory = models.IntegerField('Somatório')

	class Meta:
		verbose_name='Log'
		verbose_name_plural='Logs'
		ordering=['gene', 'tf_id', 'name']

	def __str__(self):
		return self.gene + ' ' + self.tf_id

class Background(models.Model):
	id = models.CharField('ID', primary_key=True, max_length=255)
	name = models.CharField('Nome', max_length=255, null=False, blank=False)
	matrix = models.TextField('Matriz', max_length=10000, null=False, blank=False)
	motifs = models.CharField('Motivos', max_length=10000, null=False, blank=False)
	reverseComplement = models.CharField('Complemento reverso', max_length=10000, null=False, blank=False)
	genome = models.IntegerField('Genoma')

	class Meta:
		verbose_name='Background'
		verbose_name_plural='Backgrounds'
		ordering=['id', 'name']

	def __str__(self):
		return self.id