from django.contrib import admin
from .models import *

class ScrapeAdmin(admin.ModelAdmin):
    list_display = ('user', 'borough', 'startdate', 'enddate', 'results_number', 'date_added')
    

admin.site.register(Scrape, ScrapeAdmin)

admin.site.register(Word)
admin.site.register(Date)
