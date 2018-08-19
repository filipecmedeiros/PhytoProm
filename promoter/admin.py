from django.contrib import admin

from .models import Especie, Promoter
# Register your models here.
class EspecieAdmin(admin.ModelAdmin):
	list_display = ['name']
	search_display = ['name']
	list_filter = ['name']

class PromoterAdmin(admin.ModelAdmin):
	list_display = ['locus', 'especie', 'size', 'direction']
	search_display = ['locus', 'especie', 'size', 'direction']
	list_filter = ['especie']

admin.site.register(Promoter, PromoterAdmin)