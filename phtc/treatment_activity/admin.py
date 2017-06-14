from django.contrib import admin
from phtc.treatment_activity.models import TreatmentNode, TreatmentPath
from treebeard.admin import TreeAdmin

admin.site.register(TreatmentNode, TreeAdmin)


class TreatmentPathAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',
                    'drug_choice',
                    'treatment_status',
                    'cirrhosis',
                    'tree')


admin.site.register(TreatmentPath, TreatmentPathAdmin)
