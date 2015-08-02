from django.contrib import admin
from nhlhockey.models import Conference, Division, Team

class DivisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'conference')
    
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'abbreviation', 'location', 'name', 'division')

admin.site.register(Conference)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Team, TeamAdmin)