from __future__ import absolute_import
import re

import datetime
import json
from datetime import date

from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views import generic
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Q



from .forms import ARTPatientForm, WeightHeightBSAHistoryForm, search_patient_form
from .models import ARTPatient, WeightHeightBSAHistory, CurrentStatus
from user_account.views import LoginRequest
from visits.models import Visits
from visits.forms import VisitForm
from ARTRegimen.models import Regimen, RegimenHistory, RegimenChangeReasons
from commodities.models import DrugDhysicalTran
from transactions.models import PatientTransaction
from sourceOrDestination.models import DrugSource, DrugDestination

def homepage(request):
	if request.user.is_authenticated():
		template_name='home.html'
		#patients=ARTPatient.objects.filter(first_name = 'Njoroge')
		page_title = 'Patient Repository'
		
		return render_to_response(template_name,locals(),
                              context_instance=RequestContext(request))
	else:
                return redirect(LoginRequest)


def search_patient(request, search_text):
	if search_text:
		if re.search(r'[\s]', search_text):
			persons_full_names =  ARTPatient.objects.extra(select={'full_name': "concat( firstName, middleName, surname) "} )
			choices = persons_full_names.values_list('id', 'full_name')
			patients = ARTPatient.objects.raw(
				"select * from tblartpatientmasterinformation where concat_ws(' ',firstName,middleName, surname) like '%%"+ search_text+"%%';")
			patients_length = len(list(patients))
			if patients_length <= 0:
				patients =None

		else:
			patients=ARTPatient.objects.filter(Q(first_name__icontains = search_text) 
			| Q(CCC_Number__icontains = search_text) | Q(middle_name__icontains = search_text)
			| Q(surname__icontains = search_text)
			| (Q(surname__icontains = search_text) & Q(first_name__icontains = search_text)
			 & Q(middle_name__icontains = search_text)))

		response_data = {}
		patients_list = []
		if not patients:
			response_data['data'] = 'Sorry, no patient matching this criteria! Create a new patient?'
			

		else:
			#remove leading and ending spaces with strip
			for p in patients:
				patient_data = []
				patient_data.append(p.CCC_Number)
				full_name = p.first_name.upper() + " " + p.middle_name.upper() + " " +p.surname.upper()
				patient_data.append(full_name)
				patient_data.append(p.sex.upper())
				patient_data.append(p.is_active)
				patient_data.append(p.pk)
				if p.type_of_service == '1':
					patient_data.append('ART')
				elif p.type_of_service == '2':
					patient_data.append('PEP')
				elif p.type_of_service == '5':
					patient_data.append('OI Only')
				elif p.type_of_service == '3':
					patient_data.append('PMTCT')

				patients_list.append(patient_data)

			response_data['data'] = patients_list

		return HttpResponse(json.dumps(response_data), content_type="application/json")

def activate_patient(request, pk):
    try:
        patient = ARTPatient.objects.get(pk = pk)
    except ARTPatient.DoesNotExist:
        patient = None
    if patient:
    	patient.current_status = CurrentStatus.objects.get(pk = 1)
    	patient.save()
    	messages.info(request, ("{0} Activated Successfully!").format(patient))
    	return redirect(homepage)
    

#create new or edit existing. If patient_id is None, create new, else edit this patient
def patient_registration_view(request, pk = None):
	if request.user.is_authenticated():
		template_name='patients/patientRegistration.html'
		page_title = 'Patient Registration'

		if pk:
			patient = ARTPatient.objects.get(pk = pk)
		else:
			patient = None

		if request.method == 'POST':
			form = ARTPatientForm(request.POST, request.FILES, instance = patient )
			context={'form':form,'page_title':page_title}
			if request.POST.get('cancel', None):
				return redirect(homepage)

			if request.POST.get('weight') == u"":
				messages.warning(request,
                                ("Please indicate the weight of the patient!"))
				return render_to_response(template_name, locals(),
					context_instance=RequestContext(request))


			

			if form.is_valid():
				
				if patient:
					edited_patient = form.save(commit = False)
					edited_patient.modified_at = datetime.datetime.now()
					edited_patient.save()
					if edited_patient.regimen:
						 rh = RegimenHistory(ART_patient = edited_patient,
						  regimen = Regimen.objects.get(regimencode = edited_patient.regimen), 
						  eventdate = edited_patient.created_at,
						  reasonforchange = RegimenChangeReasons.objects.get(pk = 12),
						  regimen_change_type = 'Regimen Start',
						  modified_at = edited_patient.modified_at,
						  created_at = edited_patient.created_at,
						  is_active = True)
						 rh.save()
					messages.info(request, ("{0}'s Patient Record Updated Successfully!").format(edited_patient))
				else:
					saved_patient = form.save(commit = False)
					if(form.cleaned_data['regimen'] != ''):
						saved_patient.regimen = form.cleaned_data['regimen']
					saved_patient.save()
					if saved_patient.regimen:
						 rh = RegimenHistory(ART_patient = saved_patient,
						  regimen = Regimen.objects.get(regimencode = saved_patient.regimen),  
						  eventdate = saved_patient.created_at,
						  reasonforchange = RegimenChangeReasons.objects.get(pk = 12),
						  regimen_change_type = 'Regimen Start',
						  modified_at = saved_patient.modified_at,
						  created_at = saved_patient.created_at,
						  is_active = True)
						 rh.save()
					pk = saved_patient.pk
					if request.POST.get('weight') != u"" and request.POST.get('height') != u"":
						weight_height_details = WeightHeightBSAHistory(eventdate = date.today(),
							weight = request.POST.get('weight'), height = request.POST.get('height'),
							ART_patient = saved_patient )
						weight_height_details.save()

					elif request.POST.get('weight') != u"" and request.POST.get('height') == u"":
						weight_height_details = WeightHeightBSAHistory(eventdate = date.today(),
							weight = request.POST.get('weight'),
							ART_patient = saved_patient )
						weight_height_details.save()
						
					messages.info(request, ("{0}'s Patient Record Created Successfully!").format(saved_patient))
				return redirect(patient_profile, pk = pk)
			else:
				messages.warning(request, 
					"Ooops! Please correct the highlighted fields, then try again.")
				return render_to_response(template_name, context,
					context_instance=RequestContext(request))
		else:
			form=ARTPatientForm(instance = patient, initial = {'current_status': 1 },)
			context={'form':form,'page_title':page_title}
			return render_to_response(template_name, context,
				context_instance=RequestContext(request))

	else:
		return redirect(LoginRequest)

def patient_profile(request,pk):
	template_name='patients/patient_profile.html'

	
	if request.user.is_authenticated():
		patient = get_object_or_404(ARTPatient, pk=pk)
		try:
			visits = Visits.objects.filter(ART_patient = patient)
		except Visits.DoesNotExist:
			visits = None
		if visits:
			drugs_dispensed = PatientTransaction.objects.filter(visit__in = visits)
			latest_visit = visits.latest('eventdate')
		else:
			drugs_dispensed = None
		page_title = 'Patient Profile'
		
		try:
			patient_past_bsa = WeightHeightBSAHistory.objects.filter(ART_patient = patient).order_by("-pk")[0]
		except WeightHeightBSAHistory.DoesNotExist:
			patient_past_bsa = None
		except IndexError:
			patient_past_bsa = None

		try:
			current_regimen = RegimenHistory.objects.filter(ART_patient = patient).order_by("-pk")[0]
		except RegimenHistory.DoesNotExist:
			current_regimen = None
		except IndexError:
			current_regimen = None


		return render_to_response(template_name,locals(),
                              context_instance=RequestContext(request))

	else:
		return redirect(LoginRequest)

def patient_bsa(request,pk):
	template_name='patients/patient_bsa.html'
	
	if request.user.is_authenticated():
		patient = get_object_or_404(ARTPatient, pk=pk)
		page_title = 'Patient BSA Details'
		patient_past_bsa = WeightHeightBSAHistory.objects.filter(ART_patient = patient)

		if request.method == 'POST':
			form = WeightHeightBSAHistoryForm(request.POST, request.FILES)
			context={'form':form,'page_title':page_title,'patient_past_bsa':patient_past_bsa}

			if form.is_valid():
				bsa_details = form.save(commit = False)
				bsa_details.ART_patient = patient
				bsa_details.save()
				messages.info(request, 
					("{0}'s Weight And Height Updated Successfully!").format(patient))
				return redirect(patient_profile, pk = pk)

			else:
				messages.warning(request, 
					"Ooops! Please correct the highlighted fields, then try again.")
				return render_to_response(template_name, context,
					context_instance=RequestContext(request))

		else:
			form = WeightHeightBSAHistoryForm()
			context={'form':form,'page_title':page_title,'patient_past_bsa':patient_past_bsa}
			return render_to_response(template_name,locals(),
                              context_instance=RequestContext(request))

	else:
		return redirect(LoginRequest)

def get_regimen_in_service(request, type_of_service):
	if request.is_ajax():
		try:
			regimen = Regimen.objects.filter(type_of_service = type_of_service)
			
		except Regimen.DoesNotExist:
			regimen = None
		
		response_data = {}
		regimen_list = []

		if regimen == None:
			response_data['regimencode'] = 'None Specified!'
			response_data['regimen'] = 'None Specified!'

		else:
			for r in regimen:
				individual_regimen = {}
				individual_regimen['regimen'] = r.regimen
				individual_regimen['regimencode'] = r.regimencode
				regimen_list.append(individual_regimen)
			response_data['Options'] = regimen_list
				
			
		return HttpResponse(json.dumps(regimen_list), content_type="application/json")

		'''
		Create dict/json that looks like this
		{ "Options": [
		    { "regimen":"MyText","regimencode":"MyValue"},
		    { "regimen":"MyText2","regimencode":"MyValue2"}
		   ]
		}
		'''


def check_if_CCCNumber_exists(request):
	if request.is_ajax():
		try:
			if request.POST.get('ccc') != u"":
				patient = ARTPatient.objects.get(CCC_Number = request.POST.get('ccc'))
			
		except ARTPatient.DoesNotExist:
			patient = None
		
		response_data = {}

		if patient == None:
			response_data['patient'] = 'None'

		else:
			response_data['patient'] = 'Exists'

		
		return HttpResponse(json.dumps(response_data), content_type="application/json")


def settings(request):
	template_name = 'Settings/settings.html'
	page_title = 'Application Settings'

	drug_sources = DrugSource.objects.filter(is_active = True)
	drug_destination = DrugDestination.objects.filter(is_active = True)

	return render_to_response(template_name,locals(),
                              context_instance=RequestContext(request))






