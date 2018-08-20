from django.contrib import admin

from .models import Log, Background
# Register your models here.
class LogAdmin(admin.ModelAdmin):
	list_display = ['gene', 'tf_id', 'name', 'motifs', 'reverseComplement', 'upstream', 'downstream', 'mean', 'sumatory']
	search_list = ['gene', 'tf_id', 'name', 'motifs', 'reverseComplement', 'mean', 'sumatory']
	filter_list = ['gene', 'tf_id', 'name']

class BackgroundAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'motifs', 'reverseComplement', 'genome']
	search_list = ['id', 'name', 'motifs', 'reverseComplement']
	filter_list = ['id', 'name']

admin.site.register(Log, LogAdmin)
admin.site.register(Background, BackgroundAdmin)