from django.contrib import admin

# Register your models here.
from .models import Family, Transcriptor, Specie, Promoter, Log, Background

class FamilyAdmin (admin.ModelAdmin):
	list_display = ['id']
	search_display = ['id']
	list_filter = ['id']

class TranscriptorAdmin (admin.ModelAdmin):
	list_display = ['id', 'name', 'family', 'motifs', 'reverseComplement']
	search_display = ['id', 'name', 'family', 'motifs', 'reverseComplement']
	list_filter = ['family']

class SpecieAdmin(admin.ModelAdmin):
	list_display = ['id']
	search_display = ['id']
	list_filter = ['id']

class PromoterAdmin(admin.ModelAdmin):
	list_display = ['locus', 'specie', 'size', 'direction']
	search_display = ['locus', 'specie', 'size', 'direction']
	list_filter = ['specie']
	search_fields = ['locus']

class LogAdmin(admin.ModelAdmin):
	list_display = ['promoter_id', 'tf_id', 'mean', 'sumatory']
	search_list = ['promoter_id', 'tf_id', 'mean', 'sumatory']
	filter_list = ['promoter_id', 'tf_id']

class BackgroundAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'motifs', 'reverseComplement', 'vigna_genome', 'glycine_genome',
                    'vitis_genome']
	search_list = ['id', 'name', 'motifs', 'reverseComplement']
	filter_list = ['id', 'name']

admin.site.register(Family, FamilyAdmin)
admin.site.register(Transcriptor, TranscriptorAdmin)
admin.site.register(Specie, SpecieAdmin)
admin.site.register(Promoter, PromoterAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Background, BackgroundAdmin)