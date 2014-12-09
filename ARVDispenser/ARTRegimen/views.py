from datetime import date, datetime
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.contrib import messages
from django.template import RequestContext
from django.views.decorators.cache import never_cache

from .forms import RegimenHistoryForm, AddDrugToRegimenForm, RegimenForm
from .models import RegimenHistory, RegimenChangeReasons, Regimen, DrugsInRegimen
from user_account.views import LoginRequest
from patients.models import ARTPatient
from patients.views import homepage
from transactions.views import dispense_drugs, dispense
from visits.models import Visits
from commodities.models import PhysicalDrug

@never_cache
def get_regimen_change_reasons(request):
	if request.is_ajax():
		try:
			regimen_change_reasons = RegimenChangeReasons.objects.filter(is_active = True)

			
		except RegimenChangeReasons.DoesNotExist:
			regimen_change_reasons = None
		
		
		response_data = {}
		regimen_change_reasons_list = []
		if regimen_change_reasons == None:
			response_data['none'] = 'None Specified!'

		
		else:
			
			for reason in regimen_change_reasons:
                                one_batch = {}
                                one_batch['id'] = reason.reasonforchange
				one_batch['label'] = reason.reasonforchange
				one_batch['value'] = reason.reasonforchange
				regimen_change_reasons_list.append(one_batch)

			

		return HttpResponse(json.dumps(regimen_change_reasons_list), content_type="application/json")

@never_cache
def regimen_history(request, pk):
	if not request.user.is_authenticated:
		return redirect(LoginRequest)

	template_name='transactions/regimen_change.html'
	page_title = 'Regimen Change'
	patient = ARTPatient.objects.get(pk = pk)
	todays_visit = Visits.objects.filter(ART_patient = patient).latest('eventdate')
	try:
		previous_regimen = RegimenHistory.objects.filter(ART_patient = patient)
		current_regimen_details = RegimenHistory.objects.filter(ART_patient = patient).order_by("-pk")[0]
		current_regimen = Regimen.objects.get(regimencode = current_regimen_details.regimen)
		drugs_in_regimen = DrugsInRegimen.objects.filter(regimencode = current_regimen)
	except RegimenHistory.DoesNotExist:
		previous_regimen = None
		current_regimen = None
		current_regimen_details = None

	except IndexError:
			previous_regimen = None
			current_regimen = None
			current_regimen_details = None



	if request.method == 'POST':
			form = RegimenHistoryForm(request.POST, patient_id = pk)

			if request.POST.get('cancel', None):
				return redirect(dispense, pk = pk, visit_id = todays_visit.pk)

			if form.is_valid():
				new_regimen = form.save(commit = False)
				new_regimen.eventdate = date.today()
				new_regimen.ART_patient = patient
				new_regimen.modified_at = date.today()
				new_regimen.created_at = date.today()
				new_regimen.is_active = True
				new_regimen.save()
				messages.info(request, ("{0}'s Regimen Updated To {1} Successfully!").format(patient, new_regimen.regimen.regimen))
				return redirect(dispense, pk = pk, visit_id = todays_visit.pk)
				#pk, visit_id, transaction_id = None

			else:
				messages.warning(request, 
					"Ooops! Please correct the highlighted fields, then try again.")
				return render_to_response(template_name, locals(),
					context_instance=RequestContext(request))
	else:
			form=RegimenHistoryForm(patient_id = pk)
			return render_to_response(template_name, locals(),
				context_instance=RequestContext(request))

#def get_regimen(changetype):

def registered_regimen(request):
	if not request.user.is_authenticated:
		return redirect(LoginRequest)

	template_name = 'ARTRegimen/regimen.html'
	page_title = 'Registered Regimen'

	regimen_list = Regimen.objects.all()

	return render_to_response(template_name, locals(),
				context_instance=RequestContext(request))


def regimen_details(request, pk):
	if not request.user.is_authenticated:
		return redirect(LoginRequest)

	template_name = 'ARTRegimen/regimen_details.html'
	page_title = 'Regimen Details'

	regimen = get_object_or_404(Regimen, pk = pk)
	drugs = []

	try:
		drugs_in_regimen = DrugsInRegimen.objects.filter(regimencode = regimen.regimencode)

		for drug in drugs_in_regimen:
			physical_drug = PhysicalDrug.objects.get(arvdrug = drug.combinations)
			if physical_drug:
				drugs.append(physical_drug)

	except DrugsInRegimen.DoesNotExist:
		drugs_in_regimen = None
	except PhysicalDrug.DoesNotExist:
		physical_drug = None

	return render_to_response(template_name, locals(),
				context_instance=RequestContext(request))


def add_drug_to_regimen(request, pk):
	if not request.user.is_authenticated:
		return redirect(LoginRequest)

	template_name = 'ARTRegimen/drug_to_regimen.html'
	page_title = 'Add Drug To Regimen'

	regimen = get_object_or_404(Regimen, pk = pk)

	drugs = []

	try:
		drugs_in_regimen = DrugsInRegimen.objects.filter(regimencode = regimen.regimencode)

		for drug in drugs_in_regimen:
			physical_drug = PhysicalDrug.objects.get(arvdrug = drug.combinations)
			if physical_drug:
				drugs.append(physical_drug)

	except DrugsInRegimen.DoesNotExist:
		drugs_in_regimen = None

	except PhysicalDrug.DoesNotExist:
		physical_drug = None

	if request.method == 'POST':
                form = AddDrugToRegimenForm(request.POST, pk = pk)

                if request.POST.get('cancel', None):
                        return redirect(homepage)
                
                if form.is_valid():
                        new_drug_in_regimen = form.save(commit = False)
                        new_drug_in_regimen.regimencode = regimen
                        new_drug_in_regimen.modified_at = date.today()
                        new_drug_in_regimen.created_at = date.today()
                        new_drug_in_regimen.is_active = True
                        new_drug_in_regimen.save()
                        messages.info(request, ("{0} Added To {1} Successfully!")
                                      .format(new_drug_in_regimen.combinations, new_drug_in_regimen.regimencode))

                        return redirect(regimen_details, pk = pk)
                else:
                        messages.warning(request, 
					"Ooops! Please correct the highlighted fields, then try again.")
                        return render_to_response(template_name, locals(),
                                                  context_instance=RequestContext(request))
        else:
                form=AddDrugToRegimenForm(pk = pk)
                return render_to_response(template_name, locals(),
                                          context_instance=RequestContext(request))

def remove_from_regimen(request, pk, drug_id):
	if not request.user.is_authenticated:
		return redirect(LoginRequest)

	regimen = get_object_or_404(Regimen, pk = pk)

	drug = get_object_or_404(PhysicalDrug, pk = drug_id)

	try:
		drug_in_regimen = DrugsInRegimen.objects.filter(
			combinations = drug.arvdrug).filter(regimencode = regimen)

	except DrugsInRegimen.DoesNotExist:
		drug_in_regimen = None

	if drug_in_regimen:
		drug_in_regimen.delete()
		messages.info(request, ("{0} Successfully Removed From '{1}' Regimen!")
                              .format(drug.arvdrug, regimen.regimen))
	else:
                messages.info(request, ("Seems Like The Drug Has Already Been Removed From The Regimen. Just Refresh The Page. If This Persists Please Contact The Admin.")
        	.format(drug.arvdrug, regimen.regimen))

        return redirect(regimen_details, pk = pk)


def new_regimen(request, pk = None):
	if not request.user.is_authenticated:
		return redirect(LoginRequest)

	template_name='ARTRegimen/new_regimen.html'
	page_title = 'New Regimen'

	if pk:
                regimen = Regimen.objects.get(pk = pk)
        else:
                regimen = None

        if request.method == 'POST':
                form = RegimenForm(request.POST, request.FILES, instance = regimen )

		if request.POST.get('cancel', None):
				return redirect(homepage)

		if form.is_valid():
                        if regimen:
                                edited_regimen = form.save(commit = False)
                                edited_regimen.modified_at = datetime.now()
                                edited_regimen.save()
                                pk = edited_regimen.pk
                                messages.info(request, ("{0} Updated Successfully!").format(edited_regimen))
			else:
                                saved_regimen = form.save(commit = False)
                                if form.cleaned_data['type_of_service'] is None:
                                	form.cleaned_data['type_of_service'] = 6
                                if form.cleaned_data['type_of_service'] =='':
                                	form.cleaned_data['type_of_service'] = 6
                                saved_regimen.created_at = datetime.now()
                                saved_regimen.modified_at = datetime.now()
                                saved_regimen.is_active = True
                                saved_regimen.status = 'New'
                                saved_regimen.save()
                                pk = saved_regimen.pk
                                messages.info(request, ("{0} Regimen Created Successfully!").format(saved_regimen))

			return redirect(regimen_details, pk = pk)
		else:
                        messages.warning(request,
                                         "Ooops! Please correct the highlighted fields, then try again.")
                        return render_to_response(template_name, locals(),
                                                  context_instance=RequestContext(request))
	else:
                form=RegimenForm(instance = regimen)
                return render_to_response(template_name, locals(),
				context_instance=RequestContext(request))

def activate_regimen(request, pk, activate):
    try:
        regimen = Regimen.objects.get(pk = pk)
    except Regimen.DoesNotExist:
        regimen = None
    if activate == "yes":
        if regimen:
            regimen.is_active = True
            regimen.save()
            messages.info(request, ("{0} Activated Successfully!").format(regimen))
            return redirect(registered_regimen)
    elif activate == "no":
        if regimen:
            regimen.is_active = False
            regimen.save()
            messages.info(request, ("{0} De-activated Successfully!").format(regimen))
            return redirect(registered_regimen)
