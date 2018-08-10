from django.db import models

# Create your models here.
class Family(models.Model):
	name = models.CharField('Nome', max_length=255, unique=True)

	class __Meta__:
		verbose_name='Família'
		verbose_name_plural='Famílias'
		ordering=['name']

	def __str__(self):
		return self.name


class Promoter(models.Model):
	id = models.CharField('ID', max_length=, unique=True)
	family = models.ForeignKey(Family, on_delete=models.CASCADE, verbose_name='Família')
	size = models.IntegerField('Tamanho')
	way = models.CharField('Sentido', max_length=12)
	promoter = models.CharField('Promotor', max_length=5001)

	class __Meta__:
		verbose_name='Promotor'
		verbose_name_plural='Promotores'
		ordering=['family']

	def __str__(self):
		return self.id