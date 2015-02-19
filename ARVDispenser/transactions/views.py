from datetime import date
import json

from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.forms.formsets import formset_factory
from django.utils.functional import curry
from django.forms.models import inlineformset_factory

from .models import PatientTransaction, Indication, Dosage
from .forms import make_form, PatientTransactionForm
from visits.models import Visits, VisitType
from patients.models import ARTPatient, WeightHeightBSAHistory
from user_account.views import LoginRequest
from patients.views import patient_profile, homepage
from ARTRegimen.models import Regimen, RegimenHistory, DrugsInRegimen
from ARTRegimen.forms import RegimenHistoryForm
from commodities.models import PhysicalDrug, StockTransactionType, DrugDhysicalTran
from AuditTrail.models import DrugFlowTracker

def edit_dispensed(request, visit_id):
    if not request.user.is_authenticated():
        return redirect(LoginRequest)

    visit = Visits.objects.get(pk = visit_id)
    transactions = PatientTransaction.objects.filter(visit = visit)
    art_patient = visit.ART_patient

    try:
        current_regimen = RegimenHistory.objects.filter(ART_patient = art_patient).order_by("-pk")[0]
        regimen= Regimen.objects.get(regimencode = current_regimen.regimen)

    except RegimenHistory.DoesNotExist:
        current_regimen = None
        regimen = None
    except IndexError:
        current_regimen = None
        regimen = None

    try:
        bsa_details = WeightHeightBSAHistory.objects.filter(ART_patient = art_patient).order_by("-pk")[0]
    except IndexError:
        bsa_details = None
    except WeightHeightBSAHistory.DoesNotExist:
        bsa_details = None

    template_name ='transactions/edit_dispensed.html'

    transaction_inline_fact = inlineformset_factory(Visits, PatientTransaction,form = make_form(patient_id = art_patient.pk, visit_id = visit_id))

    if request.method == "POST":
        formset = transaction_inline_fact(request.POST, request.FILES, instance=visit)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return redirect(dispense, transactions.visit.ART_patient.pk, transactions.visit.pk)
    else:
        if transactions:
            formset = transaction_inline_fact(instance=visit)
            for  t in transactions:
                #reverse the transaction by adding back what had been deducted
                update_transaction = DrugDhysicalTran.objects.filter(
                    arvdrug = t.physicalDrug).filter(
                                    tranbatch = t.batchNo).latest('transactiondate')
                update_transaction.quantity = (
                                update_transaction.quantity + t.arvquantity)
                update_transaction.save()
            try:
                current_regimen = RegimenHistory.objects.filter(
                    ART_patient = art_patient).order_by("-pk")[0]
            except RegimenHistory.DoesNotExist:
                current_regimen = None
            except IndexError:
                current_regimen = None
            if current_regimen:
                drugs =[]
                for t in transactions:
                    drug = DrugsInRegimen.objects.filter(regimencode = current_regimen.regimen).get(combinations = t.physicalDrug.arvdrug)
                    drug_dict = {}
                    drug_dict['physicalDrug'] = drug
                    drugs.append(drug)
            else:
                drug = DrugsInRegimen.objects.filter(
                    combinations = edit_transaction.physicalDrug.arvdrug).get(
                        regimencode = Regimen.objects.get(regimencode = 'OI'))
            if drugs:
                #Use the enumerate() function to generate the index along with the elements of the drugs sequence
                for idx, drug in enumerate(drugs):
                    formset.forms[idx].initial['physicalDrug'] = drug
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def dispense(request, pk, visit_id):
    if not request.user.is_authenticated():
        return redirect(LoginRequest)

    template_name='transactions/dispense.html'
    page_title = 'Dispense Drugs'
    initial = [{'patient_id': pk,'visit_id':visit_id}]

    regimen = None
    art_patient = get_object_or_404(ARTPatient, pk = pk)

    try:
        current_regimen = RegimenHistory.objects.filter(ART_patient = art_patient).order_by("-pk")[0]
        regimen= Regimen.objects.get(regimencode = current_regimen.regimen)

    except RegimenHistory.DoesNotExist:
        current_regimen = None
        regimen = None
    except IndexError:
        current_regimen = None
        regimen = None

    try:
        bsa_details = WeightHeightBSAHistory.objects.filter(ART_patient = art_patient).order_by("-pk")[0]
    except IndexError:
        bsa_details = None
    except WeightHeightBSAHistory.DoesNotExist:
        bsa_details = None

    try:
        todays_visit = Visits.objects.get(pk = visit_id)
        dispensed_today = PatientTransaction.objects.filter(visit = todays_visit)
    except PatientTransaction.DoesNotExist:
        dispensed_today = None
    
    formset_cls = formset_factory(make_form(pk, visit_id), max_num = 100)
    
    
    
    if request.method == 'POST':
        formset = formset_cls(request.POST)
        
        if request.POST.get('cancel', None):
            return redirect(homepage)
        if formset.is_valid():
            
            for form in formset.forms:
                if not formset.forms[0].has_changed():
                    messages.warning(request,
                                     ("Ooops! Atleast One Record Is Required."))
                    return render_to_response(template_name, locals(),
                                              context_instance=RequestContext(request))
                    
                if form.is_valid() and form.has_changed():
                    transaction = form.save(commit = False)
                    transaction.visit = Visits.objects.get(pk = visit_id)
                    transaction.modified_at = date.today()
                    transaction.created_at = date.today()
                    transaction.is_active = True
                    try:
                        drug_in_regimen = form.cleaned_data['physicalDrug']
                        physical_drug = PhysicalDrug.objects.get(arvdrug = drug_in_regimen.combinations)
                    except PhysicalDrug.DoesNotExist:
                        physical_drug = None

                    if form.cleaned_data['batchNo'] == None:
                        messages.warning(request,
                            ("No batch Selected!"))
                        return render_to_response(template_name, locals(),
                            context_instance=RequestContext(request))

                    if form.cleaned_data['physicalDrug'] == None:
                        messages.warning(request,
                            ("No Drug Selected!"))
                        return render_to_response(template_name, locals(),
                            context_instance=RequestContext(request))

                    

                    if physical_drug:
                        transaction.physicalDrug = physical_drug
                    else:
                        messages.warning(request,
                            ("Ooops! Looks Like The Drug Was Never Registered. Please Register It First."))
                        return render_to_response(template_name, locals(),
                            context_instance=RequestContext(request))


                    transaction.batchNo = form.cleaned_data['batchNo']
                    
                    transaction.operator = request.user
                    update_transaction = DrugDhysicalTran.objects.filter(
                        arvdrug = transaction.physicalDrug).filter(
                            tranbatch = transaction.batchNo).latest('transactiondate')
                    
                    new_qty = transaction.save(drug_qty = update_transaction.quantity)

                    update_transaction.quantity = new_qty
                    update_transaction.save()
                    
                    audit_trail = DrugFlowTracker(transactiontype = StockTransactionType.objects.get(pk = 6),
                                                  transactiondate = transaction.created_at,
                                                  tranbatch = transaction.batchNo,
                                                  arvdrug = transaction.physicalDrug.arvdrug,
                                                  expirydate = update_transaction.expirydate,
                                                  remarks = 'Dispensed To Patient: '+art_patient.CCC_Number,
                                                  quantity = transaction.arvquantity,
                                                  operator = request.user)
                    audit_trail.save()
                
                    
            messages.info(request, ("Drug(s) Dispensed Successfully!"))
            return redirect(homepage)
        else:
            messages.warning(request,"Ooops! Please correct the highlighted fields, then try again.")
            return render_to_response(template_name, locals(), context_instance=RequestContext(request))
            
    else:
        formset = formset_cls()
        return render_to_response(template_name, locals(), context_instance=RequestContext(request))



def dispense_drugs(request, pk, visit_id, transaction_id = None):
	if request.user.is_authenticated():
		template_name='transactions/dispense_drugs.html'
		page_title = 'Dispense Drugs'
		dispensed_today = None


		regimen = None
		art_patient = get_object_or_404(ARTPatient, pk = pk)

		try:
			current_regimen = RegimenHistory.objects.filter(ART_patient = art_patient).order_by("-pk")[0]
			regimen= Regimen.objects.get(regimencode = current_regimen.regimen)
			
		except RegimenHistory.DoesNotExist:
			current_regimen = None
			regimen = None
		except IndexError:
                        current_regimen = None
			regimen = None
                        
	        try:
                        todays_visit = Visits.objects.get(pk = visit_id)
	        	dispensed_today = PatientTransaction.objects.filter(visit = todays_visit)
	        except PatientTransaction.DoesNotExist:
	        	dispensed_today = None

	        try:
                        bsa_details = WeightHeightBSAHistory.objects.filter(ART_patient = art_patient).order_by("-pk")[0]
                except IndexError:
                        bsa_details = None
                except WeightHeightBSAHistory.DoesNotExist:
                        bsa_details = None

	        if transaction_id:
	        	edit_transaction = PatientTransaction.objects.get(transactioncode = transaction_id)
	        else:
	        	edit_transaction = None

	        if request.method == 'POST':
                        form = PatientTransactionForm(request.POST, patient_id = art_patient.pk, instance = edit_transaction )
                        
                        updated_data = request.POST.copy()

                        if request.POST.get('cancel', None):
                            return redirect(homepage)

                        if request.POST.get('batchNo') == u"":
                            messages.warning(request,
                                ("No Batch specified!"))
                            return render_to_response(template_name, locals(),
                                                          context_instance=RequestContext(request))

                        otherDose = None
                        if request.POST.get('otherDose') != u"":
                            otherDose = request.POST.get('otherDose')

                        old_qty = None
                        if request.POST.get('old_qty') != u"":
                            old_qty = request.POST.get('old_qty')


                        
                        if request.POST.get('physicalDrug') == u"":
                            messages.warning(request,
                                ("No Drug specified!"))
                            return render_to_response(template_name, locals(),
                                                          context_instance=RequestContext(request))
                        try:
                            drug_in_regimen = DrugsInRegimen.objects.get(pk = request.POST.get('physicalDrug'))
                            drug = PhysicalDrug.objects.get(arvdrug = drug_in_regimen.combinations)
                        except PhysicalDrug.DoesNotExist:
                            drug = None
                        if not drug:
                            messages.warning(request,
                                    ("{0}, Drug = {1}, Drugs In Regimen = {2} This Drug Has Not Been Registered! Please Register It First")
                                             .format(request.POST.get('physicalDrug')), drug, drug_in_regimen)
                            return render_to_response(template_name, locals(),
                                    context_instance=RequestContext(request))
                        
			if form.is_valid():
                                if edit_transaction:
                                        editted = form.save(commit = False)
                                        editted.visit = Visits.objects.get(pk = visit_id)
                                        editted.modified_at = date.today()
                                        editted.created_at = date.today()
                                        editted.is_active = True
                                        if otherDose != None:
                                            transaction.other_dosage = otherDose
                                        physical_drug = form.cleaned_data['physicalDrug']
                                        if form.cleaned_data['batchNo'] == None:
                                            messages.warning(request,
                                                                 ("No batch Selected!"))
                                            return render_to_response(template_name, locals(),
                                                          context_instance=RequestContext(request))

                                        editted.batchNo = form.cleaned_data['batchNo']
                                        editted.physicalDrug = drug
                                        editted.operator = request.user
                                        
                                        update_transaction = DrugDhysicalTran.objects.filter(
                                                arvdrug = editted.physicalDrug).filter(
                                                tranbatch = editted.batchNo).latest('transactiondate')

                                        new_qty = editted.save_edit(drug_qty = int(update_transaction.quantity), old_qty = int(old_qty))

                                        update_transaction.quantity = new_qty
                                        update_transaction.save()
                                        
                                        audit_trail = DrugFlowTracker(transactiontype = StockTransactionType.objects.get(pk = 6),
                                                  transactiondate = editted.created_at,
                                                  tranbatch = editted.batchNo,
                                                  arvdrug = editted.physicalDrug.arvdrug,
                                                  expirydate = update_transaction.expirydate,
                                                  remarks = 'An Update To Dispensed Drug: '+art_patient.CCC_Number,
                                                  quantity = editted.arvquantity,
                                                  operator = request.user)
                                        audit_trail.save()

                                        messages.info(request, ("Dispensed Drug Editted Successfully!"))
                                        return redirect(dispense, pk = pk,visit_id = visit_id)
                                else:
                                        transaction = form.save(commit = False)
                                        transaction.visit = Visits.objects.get(pk = visit_id)
                                        transaction.modified_at = date.today()
                                        transaction.created_at = date.today()
                                        transaction.is_active = True
                                        if otherDose != None:
                                            transaction.other_dosage = otherDose
                                        physical_drug = form.cleaned_data['physicalDrug']
                                        if form.cleaned_data['batchNo'] == None:
                                            messages.warning(request,
                                                                 ("No batch Selected!"))
                                            return render_to_response(template_name, locals(),
                                                          context_instance=RequestContext(request))

                                        transaction.batchNo = form.cleaned_data['batchNo']
                                        

                                        transaction.physicalDrug = drug
                                        transaction.operator = request.user

                                        update_transaction = DrugDhysicalTran.objects.filter(
                                                arvdrug = transaction.physicalDrug).filter(
                                                tranbatch = transaction.batchNo).latest('transactiondate')

                                        new_qty = transaction.save(drug_qty = update_transaction.quantity)
                                        
                                        
                                        update_transaction.quantity = new_qty
                                        update_transaction.save()

                                        messages.info(request, ("Drug(s) Dispensed Successfully!"))
                                        return HttpResponseRedirect('/patients/dispense-drugs/'+pk+'/'+visit_id)
                        else:
                                messages.warning(request,
                                                 "Ooops! Please correct the highlighted fields, then try again.")
                                return render_to_response(template_name, locals(),
                                                          context_instance=RequestContext(request))

		else:
                        if edit_transaction:

                            try:
                                current_regimen = RegimenHistory.objects.filter(
                                    ART_patient = art_patient).order_by("-pk")[0]
                            except RegimenHistory.DoesNotExist:
                                current_regimen = None
                            except IndexError:
                                current_regimen = None

                            if current_regimen:
                                drug = DrugsInRegimen.objects.filter(
                                    regimencode = current_regimen.regimen).get(
                                        combinations = edit_transaction.physicalDrug.arvdrug)
                            else:
                                drug = DrugsInRegimen.objects.filter(
                                    combinations = edit_transaction.physicalDrug.arvdrug).get(
                                        regimencode = Regimen.objects.get(regimencode = 'OI'))
                            if drug:
                                form=PatientTransactionForm(patient_id = art_patient.pk, instance = edit_transaction,
                                                            initial ={'physicalDrug': drug},)
                        else:
                                form=PatientTransactionForm(patient_id = art_patient.pk, instance = edit_transaction)

			
			return render_to_response(template_name, locals(),
				context_instance=RequestContext(request))


	else:
		return redirect(LoginRequest)

def delete_transaction(request, transaction_id):
    try:
        transaction = PatientTransaction.objects.get(transactioncode = transaction_id)
    except PatientTransaction.DoesNotExist:
        transaction = None

    if transaction:
        update_transaction = DrugDhysicalTran.objects.filter(
                                                arvdrug = transaction.physicalDrug).filter(
                                                tranbatch = transaction.batchNo).latest('pk')
        update_transaction.quantity =  transaction.arvquantity + update_transaction.quantity
        update_transaction.save()                                     
        transaction.delete()
        audit_trail = DrugFlowTracker(transactiontype = StockTransactionType.objects.get(pk = 4),
                                      transactiondate = transaction.created_at,
                                      tranbatch = transaction.batchNo,
                                      arvdrug = transaction.physicalDrug.arvdrug,
                                      expirydate = update_transaction.expirydate,
                                      remarks = 'Transaction Reversed',
                                      quantity = transaction.arvquantity,
                                      operator = request.user)
        audit_trail.save()
        messages.info(request, ("Transaction Deleted Successfully!"))
    else:
        messages.info(request, ("Ooops! Seems Like The Transaction Has Already Been Deleted. Just Refresh The Page. If This Persists Please Contact The Admin."))
        
    return redirect(dispense, transaction.visit.ART_patient.pk, transaction.visit.pk)


def get_drugs_dispensed_today(request, visitid):
	if not request.user.is_authenticated():
		return redirect(LoginRequest)
	if request.is_ajax:
		visit = Visits.objects.filter(pk = visitid).latest('eventdate')
		patient_transactions = PatientTransaction.objects.filter(visit = visit)
		response_data = {}
		if patient_transactions != None:
			for patient_transaction in patient_transactions:
				response_data['physicalDrug'] = patient_transaction.physicalDrug.arvdrug
				response_data['arvquantity'] = patient_transaction.arvquantity
				response_data['dosage'] = patient_transaction.dosage.dose
				response_data['duration'] = patient_transaction.duration
				response_data['indication'] = patient_transaction.indication.indicationname
				response_data['operator'] = patient_transaction.operator.last_name +' '+patient_transaction.operator.first_name
				response_data['pillcount'] = patient_transaction.pillcount
				response_data['batchNo'] = patient_transaction.batchNo
				#response_data['expiry_date'] = patient_transaction.expiry_date
				response_data['adherence'] = patient_transaction.adherence
				#response_data['tca'] = patient_transaction.visit.dateofnextappointment


		return HttpResponse(json.dumps(response_data), content_type="application/json")


def add_new_dosage(request):
    if request.is_ajax():
        dosage = Dosage(dose = request.POST.get('dose'), value = request.POST.get('value'),
         frequency = request.POST.get('frequency'), upsize_ts = date.today())
        
        dosage.save()

        response_data = {}
        dose_list =[]


        if dosage == None:
            response_data['dosage'] = 'None Specified!'

        else:
            response_data['dosage'] = dosage.dose

        return HttpResponse(json.dumps(response_data), content_type="application/json")

