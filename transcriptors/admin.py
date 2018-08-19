from django.contrib import admin

# Register your models here.
from .models import Transcriptor

class TranscriptorAdmin (admin.ModelAdmin):
	list_display = ['id', 'name', 'family', 'motifs', 'reverseComplement']
	search_display = ['id', 'name', 'family', 'motifs', 'reverseComplement']
	list_filter = ['family']

admin.site.register(Transcriptor, TranscriptorAdmin)