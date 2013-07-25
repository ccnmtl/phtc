from django.contrib import admin
from phtc.logic_model.models import Column, Scenario

class ColumnAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',
    				'order_rank',
                    'flavor')



admin.site.register(Column, ColumnAdmin)

class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',
    				'order_rank')



admin.site.register(Scenario, ScenarioAdmin)
