from django.contrib import admin

from django.contrib import admin

from .models import ARTPatient, ClientSupportDetails, CurrentStatus, WeightHeightBSAHistory

class ARTPatientAdmin(admin.ModelAdmin):
	date_hierarchy='created_at'
	fields=('first_name','middle_name','sex', 'date_therapy_started')
	list_display=['first_name','middle_name','sex', 'date_therapy_started']
	list_display_links=['first_name']
	#list_editable=['published']
	list_filter=['modified_at','sex']
	#prepopulated_fields={'slug':('title',)}
	#search_fields=['title','content']



admin.site.register(ARTPatient, ARTPatientAdmin)
