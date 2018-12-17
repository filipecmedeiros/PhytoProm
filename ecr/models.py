from django.db import models

# Create your models here.


class Family (models.Model):
    id = models.CharField('Nome', primary_key=True, max_length=255)

    class Meta:
        verbose_name = 'Família de fator de transcrição'
        verbose_name_plural = 'Famílias de fatores de transcrição'
        ordering = ['id']

    def __str__(self):
        return self.id


class Transcriptor(models.Model):
    id = models.CharField('ID', primary_key=True, max_length=255)
    name = models.CharField('Nome', max_length=255)
    family = models.ForeignKey(
        Family, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Família')
    matrix = models.TextField(
        'Matriz', max_length=10000, null=False, blank=False)
    motifs = models.CharField(
        'Motivos', max_length=10000, null=False, blank=False)
    reverseComplement = models.CharField(
        'Complemento reverso', max_length=10000, null=False, blank=False)

    class Meta:
        verbose_name = 'Fator de transcrição'
        verbose_name_plural = 'Fatores de transcrição'
        ordering = ['family', 'id']

    def __str__(self):
        return self.id


class Specie(models.Model):
    id = models.CharField('Espécie', primary_key=True, max_length=255)

    class Meta:
        verbose_name = 'Espécie'
        verbose_name_plural = 'Espécies'
        ordering = ['id']

    def __str__(self):
        return self.id


class Promoter(models.Model):
    locus = models.CharField('Locus', max_length=255)
    specie = models.ForeignKey(
        Specie, on_delete=models.CASCADE, verbose_name='Espécie')
    size = models.IntegerField('Tamanho', null=False, blank=False)
    direction = models.CharField(
        'Direção', max_length=255, null=False, blank=False)
    promoter = models.TextField(
        'Promotor', max_length=5001, null=False, blank=False)

    class Meta:
        verbose_name = 'Promotor'
        verbose_name_plural = 'Promotores'
        ordering = ['specie', 'locus', 'direction']

    def __str__(self):
        return self.locus


class Log(models.Model):
    promoter_id = models.CharField('Promotor', null=True, max_length=255)
    tf = models.ForeignKey(
        Transcriptor, on_delete=models.CASCADE, verbose_name='Fator de transcrição')
    upstream = models.TextField('upstream', null=True, blank=True)
    downstream = models.TextField('downstream', null=True, blank=True)
    mean = models.FloatField('Média', null=True, blank=True)
    sumatory = models.IntegerField('Somatório', null=True, blank=True)

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
        ordering = ['promoter_id', 'tf']

    def __str__(self):
        return self.promoter_id + ' ' + self.tf_id


class Background(models.Model):
    id = models.CharField('ID', primary_key=True, max_length=255)
    name = models.CharField('Nome', max_length=255, null=False, blank=False)
    family = models.ForeignKey(
        Family, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Família')
    matrix = models.TextField(
        'Matriz', max_length=10000, null=False, blank=False)
    motifs = models.CharField(
        'Motivos', max_length=10000, null=False, blank=False)
    reverseComplement = models.CharField(
        'Complemento reverso', max_length=10000, null=False, blank=False)
    vigna_genome = models.IntegerField('Genoma de Vigna')

    class Meta:
        verbose_name = 'Background'
        verbose_name_plural = 'Backgrounds'
        ordering = ['id']

    def __str__(self):
        return self.id
