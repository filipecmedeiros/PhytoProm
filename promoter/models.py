from django.db import models

# Create your models here.
class Especie(models.Model):
	name = models.CharField('Espécie', max_length=255)

	class Meta:
		verbose_name='Espécie'
		verbose_name_plural='Espécies'
		ordering=['name']

	def __str__(self):
		return self.name

class Promoter(models.Model):
	locus = models.CharField('Locus', max_length=255, null=False, blank=False)
	especie = models.CharField('Espécie', max_length=255, null=False, blank=False)
	size = models.IntegerField('Tamanho', null=False, blank=False)
	direction = models.CharField('Direção', max_length=255, null=False, blank=False)
	promoter = models.TextField('Promotor', max_length=5001, null=False, blank=False)

	class Meta:
		verbose_name='Promotor'
		verbose_name_plural='Promotores'
		ordering=['especie', 'locus', 'direction']

	def __str__(self):
		return self.locus
