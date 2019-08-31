# Generated by Django 2.1.2 on 2019-06-26 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecr', '0002_auto_20190625_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='background',
            name='vitis_genome',
            field=models.IntegerField(default=0, verbose_name='Genoma de Glycine'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='background',
            name='glycine_genome',
            field=models.IntegerField(verbose_name='Genoma de Glycine'),
        ),
    ]