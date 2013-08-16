from django.contrib import admin
from phtc.logic_model.models import Column, Scenario, GamePhase
from phtc.logic_model.models import ActivePhase, BoxColor


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',
                    'order_rank',
                    'flavor')
admin.site.register(Column, ColumnAdmin)


class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',
                    'order_rank')
admin.site.register(Scenario, ScenarioAdmin)


class GamePhaseAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',
                    'order_rank')
admin.site.register(GamePhase, GamePhaseAdmin)


class ActivePhaseAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
admin.site.register(ActivePhase, ActivePhaseAdmin)


class BoxColorAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
admin.site.register(BoxColor, BoxColorAdmin)
