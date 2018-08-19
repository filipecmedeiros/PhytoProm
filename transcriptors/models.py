from django.db import models

# Create your models here.
class Family (models.Model):
	name = models.CharField('Nome', max_length=255)

	class Meta:
		verbose_name='Família de fator de transcrição'
		verbose_name_plural='Famílias de fatores de transcrição'
		ordering=['name']

	def __str__ (self):
		return self.name


class Transcriptor(models.Model):
	id = models.CharField('ID', primary_key=True, max_length=255)
	name = models.CharField('Nome', max_length=255)
	family = models.CharField('Família', max_length=255, null=True, blank=True)
	a = models.TextField('A', max_length=10000, null=False, blank=False)
	c = models.TextField('C', max_length=10000, null=False, blank=False)
	g = models.TextField('G', max_length=10000, null=False, blank=False)
	t = models.TextField('T', max_length=10000, null=False, blank=False)
	matrix = models.TextField('Matriz', max_length=10000, null=False, blank=False)
	motifs = models.CharField('Motivos', max_length=10000, null=False, blank=False)
	reverseComplement = models.CharField('Complemento reverso', max_length=10000, null=False, blank=False)

	class Meta:
		verbose_name='Fator de transcrição'
		verbose_name_plural='Fatores de transcrição'
		ordering=['family', 'id']

	def __str__(self):
		return self.id