from django.contrib import admin
#from phtc.logic_model.models import TreatmentNode, TreatmentPath
#from treebeard.admin import TreeAdmin

if 1 == 0:
	admin.site.register(TreatmentNode, TreeAdmin)


	class TreatmentPathAdmin(admin.ModelAdmin):
	    list_display = ('__unicode__',
	                    'drug_choice',
	                    'treatment_status',
	                    'cirrhosis',
	                    'tree')

	admin.site.register(TreatmentPath, TreatmentPathAdmin)
