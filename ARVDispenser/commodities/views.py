import json
from datetime import date, datetime

from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.formsets import formset_factory


from .models import PhysicalDrug, DrugDhysicalTran
from .forms import make_forms, DrugRegistrationForm
from ARTRegimen.models import Regimen
from user_account.views import LoginRequest
from patients.views import homepage

def get_drug_unit(request):
	if request.is_ajax():
		try:
			if request.POST.get('arv') != u"":
				drug = PhysicalDrug.objects.get(arvdrug = request.POST.get('arv'))
				batchNos = DrugDhysicalTran.objects.filter(arvdrug = drug.arvdrug).filter(
					quantity__gt = 0).order_by('expirydate')
			
		except PhysicalDrug.DoesNotExist:
			drug = None

		except DrugDhysicalTran.DoesNotExist:
			batchNos = None
		
		
		
		
		response_data = {}
		batchNos_list = []
		if drug == None:
			response_data['unit'] = 'None Specified!'
			response_data['packsize'] = 'None Specified!'
			response_data['std_dose'] = 'None Specified!'

		else:
			#remove leading and ending spaces with strip
			response_data['unit'] = drug.drugunit.strip()
			response_data['packsize'] = drug.packsize.strip()
			response_data['std_dose'] = drug.std_dose.strip()

		if batchNos == None:
			response_data['batch_no'] = 'None Specified!'

		else:
			one_batch = {}
			for batch in batchNos:
				one_batch[batch.tranbatch] = batch.tranbatch
				batchNos_list.append(batch.tranbatch)

			response_data['batches'] = batchNos_list

		return HttpResponse(json.dumps(response_data), content_type="application/json")

def get_batch_details(request):
	if request.is_ajax():
		try:
			if request.POST.get('arv') != u"" and request.POST.get('batch_no') != u"":
				drug = PhysicalDrug.objects.get(arvdrug = request.POST.get('arv'))
				transaction = DrugDhysicalTran.objects.filter(
					arvdrug = drug.arvdrug).filter(tranbatch = request.POST.get('batch_no')).latest('transactiondate')
			
		except PhysicalDrug.DoesNotExist:
			drug = None

		except DrugDhysicalTran.DoesNotExist:
			transaction = None
		

		response_data = {}
		transaction_list = []


		if transaction == None:
			response_data['expiry_date'] = 'None Specified!'
			response_data['quantity'] = 'None Specified!'

		else:
			response_data['expiry_date'] = transaction.expirydate.strftime('%Y-%m-%d')
			
			response_data['quantity'] = transaction.quantity
		return HttpResponse(json.dumps(response_data), content_type="application/json")


def drug_transactions(request):
	if not request.user.is_authenticated:
		return redirect(LoginRequest)
	template_name = 'commodities/drug_transactions.html'
	page_title = 'Drug Transactions'

	drug_transactions = DrugDhysicalTran.objects.all().order_by('-created_at')
	
	return render_to_response(template_name, locals(),
		context_instance=RequestContext(request))

def drug_registration(request, pk = None):
	if not request.user.is_authenticated:
		return redirect(LoginRequest)

	template_name = 'commodities/drug_registration.html'
	page_title = 'Registered Drugs'

	if pk:
		drug = PhysicalDrug.objects.get(pk = pk)
	else:
		drug = None

	if request.method == 'POST':
			form = DrugRegistrationForm(request.POST, request.FILES, instance = drug )

			if request.POST.get('cancel', None):
				return redirect(homepage)

			if form.is_valid():
				if drug:
					edited_drug = form.save(commit = False)
					edited_drug.modified_at = datetime.now()
					edited_drug.save()
					pk=edited_drug.pk
					messages.info(request, ("{0}'s Updated Successfully!").format(edited_drug))
				else:
					saved_drug = form.save(commit = False)
					saved_drug.modified_at = datetime.now()
					saved_drug.created_at = datetime.now()
					saved_drug.is_active = True
					saved_drug.save()
					pk=saved_drug.pk
					messages.info(request, ("{0}'s Created Successfully!").format(saved_drug))
				return redirect(drug_details, pk = pk)

			else:
				messages.warning(request, 
					"Ooops! Please correct the highlighted fields, then try again.")
				return render_to_response(template_name, locals(),
					context_instance=RequestContext(request))

	else:
			form=DrugRegistrationForm(instance = drug)
			return render_to_response(template_name, locals(),
				context_instance=RequestContext(request))

def drug_details(request, pk):
	if not request.user.is_authenticated:
		return redirect(LoginRequest)

	template_name = 'commodities/drug_details.html'
	page_title = 'Drug Details'

	drug = get_object_or_404(PhysicalDrug, pk = pk)

	return render_to_response(template_name,locals(),
                              context_instance=RequestContext(request))

def registered_drugs(request):
	if not request.user.is_authenticated:
		return redirect(LoginRequest)
	template_name = 'commodities/registered_drugs.html'
	page_title = 'Register Drugs'

	physical_drug = PhysicalDrug.objects.all()	

	return render_to_response(template_name, locals(),
		context_instance=RequestContext(request))


def activate_drug(request, pk, activate):
    try:
        physicalDrug = PhysicalDrug.objects.get(pk = pk)
    except PhysicalDrug.DoesNotExist:
        physicalDrug = None
    if activate == "yes":
    	if physicalDrug:
    		physicalDrug.is_active = True
    		physicalDrug.modified_at =  date.today()
    		physicalDrug.save()
    		messages.info(request, ("{0} Activated Successfully!").format(physicalDrug.arvdrug))
    		return redirect(registered_drugs)
    elif activate == "no":
    	if physicalDrug:
    		physicalDrug.is_active = False
    		physicalDrug.modified_at =  date.today()
    		physicalDrug.save()
    		messages.info(request, ("{0} De-activated Successfully!").format(physicalDrug.arvdrug))
    		return redirect(registered_drugs)

def new_transaction(request):
        if not request.user.is_authenticated:
                return redirect(LoginRequest)
        template_name='commodities/receive_drugs.html'
        page_title = 'Receive Drugs'
        drug_transactions = DrugDhysicalTran.objects.all().order_by('-created_at')

        formset_cls = formset_factory(make_forms(), max_num = 100)

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
                            transaction.modified_at = date.today()
                            transaction.created_at = date.today()
                            transaction.is_active = True
                            transaction.save()
                        
                            
                    messages.info(request, ("Transactions Saved Successfully!"))
                    return redirect(homepage)
                else:
                        messages.warning(request,"Ooops! Please correct the highlighted fields, then try again.")
                        return render_to_response(template_name, locals(), context_instance=RequestContext(request))
        else:
                formset = formset_cls()
                return render_to_response(template_name, locals(), context_instance=RequestContext(request))
        
def receive_drugs(request, pk = None):
	if request.user.is_authenticated():
		template_name='commodities/receiv_drugs.html'
		page_title = 'Receive Drugs'
		drug_transactions = DrugDhysicalTran.objects.all().order_by('-created_at')


		if pk:
			drugs = DrugDhysicalTran.objects.get(pk = pk)
		else:
			drugs = None

		if request.method == 'POST':
			form = DrugDhysicalTranForm(request.POST, request.FILES, instance = drugs)
			if request.POST.get('cancel', None):
				return redirect(homepage)

			
			if form.is_valid():
				
				if drugs:
					edited_drug = form.save(commit = False)
					edited_drug.modified_at = date.today()
					edited_drug.created_at = date.today()
					edited_drug.is_active = True
					if request.POST.get('src_or_dst') != u"":
						edited_drug.source_or_destination = request.POST.get('src_or_dst')
					edited_drug.save()
					messages.info(request, 
						("{0} Transaction Updated Successfully!")
						.format(edited_drug.arvdrug))
				else:
					saved_drug = form.save(commit = False)
					saved_drug.modified_at = date.today()
					saved_drug.created_at = date.today()
					saved_drug.is_active = True
					if request.POST.get('src_or_dst') != u"":
						saved_drug.source_or_destination = request.POST.get('src_or_dst')
					saved_drug.save()
					pk = saved_drug.pk
					messages.info(request, 
						("{0} Transaction Created Successfully!")
						.format(saved_drug.arvdrug))
				return HttpResponseRedirect('')
			else:
				messages.warning(request, 
					"Ooops! Please correct the highlighted fields, then try again.")
				return render_to_response(template_name, locals(),
					context_instance=RequestContext(request))
		else:
			if drugs:
				form=DrugDhysicalTranForm(instance = drugs, initial={'arvdrug': PhysicalDrug.objects.get(arvdrug = drugs.arvdrug)})
			else:
				form=DrugDhysicalTranForm(instance = drugs)
			return render_to_response(template_name, locals(),
				context_instance=RequestContext(request))

	else:
		return redirect(LoginRequest)

def delete_transaction(request, transaction_id):
    try:
        transaction = DrugDhysicalTran.objects.get(stocktransactionnumber = transaction_id)
    except DrugDhysicalTran.DoesNotExist:
        transaction = None

    if transaction:
    	transaction.delete()
        messages.info(request, ("Transaction Deleted Successfully!"))
    else:
    	messages.info(request, ("Ooops! Seems Like The Transaction Has Already Been Deleted. Just Refresh The Page. If This Persists Please Contact The Admin."))
    
    return redirect(receive_drugs)

