from datetime import date, timedelta, datetime
#import dateutil.parser
import json

from django.shortcuts import render
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.db.models import Q


from .forms import VisitForm, RetrospectiveVisitForm
from .models import VisitType, Visits, appointments_tracker, Slot_size
from patients.models import ARTPatient, WeightHeightBSAHistory
from user_account.views import LoginRequest
from transactions.views import dispense
from transactions.models import PatientTransaction
from patients.views import homepage

MAX_SLOT_SIZE = Slot_size.objects.get(pk = 1)

def get_appointment_dates(request):
	if request.is_ajax():
                now = datetime.now()
		try:
                        appointment_dates = appointments_tracker.objects.filter(Q(appointment_date = now.date())|Q(appointment_date__gt = now.date()))

                except appointments_tracker.DoesNotExist:
			appointment_dates = None
		
		
		
		
		response_data = {}
		batchNos_list = []

		if appointment_dates == None:
			response_data['appointment_dates'] = 'None Found!'

		else:
			one_batch = {}
			for batch in appointment_dates:
				one_batch[batch.appointment_date] = batch.appointment_date
				batchNos_list.append(batch.appointment_date.strftime('%Y-%m-%d'))

			response_data['batches'] = batchNos_list

		return HttpResponse(json.dumps(response_data), content_type="application/json")

def patients_scheduled(request):
	'''
	gets all  the patients scheduled for visit on a given date
	'''
	template_name='patients_scheduled.html'
	page_title = 'Patients Scheduled'
	visits = Visits.objects.filter(dateofnextappointment = datetime.today())
	patients = []
	for visit in visits:
		patient = visit.ART_patient
		patients.append(patient) 

	return render_to_response(template_name, locals(),
		context_instance=RequestContext(request))


def create_visit(request, pk):
	if not request.user.is_authenticated:
		return redirect(LoginRequest)

	patient = ARTPatient.objects.get(pk = pk)
	todays_date = date.today()
	try:
		last_visit = Visits.objects.filter(ART_patient = patient).latest("eventdate")
	except Visits.DoesNotExist:
		last_visit = None

	try:
                dispensed_today = PatientTransaction.objects.filter(visit = last_visit)
        except PatientTransaction.DoesNotExist:
                dispensed_today = None


	#last_drugs_dispensed = PatientTransaction.objects.filter(visit = last_visit)
	

	template_name = 'visits/_snippets/visits_modal.html'
	context = {'patient':patient, 'template_name':template_name}

	if request.method == 'POST':
			form = VisitForm(request.POST, patient_id = pk)
			context.update({'form': form})

			if request.POST.get('cancel', None):
				return redirect(homepage)
				
			newly_enrolled = 1
			if date(patient.date_therapy_started.year,patient.date_therapy_started.month,patient.date_therapy_started.day) == date(datetime.now().year,datetime.now().month,datetime.now().day):
				newly_enrolled = 2
			updated_data = request.POST.copy()

			if request.POST.get('visittype') == u"":
				updated_data.update({'visittype':2})
				form = VisitForm(data=updated_data, patient_id = pk) 

			if request.POST.get('weight') == u"":
				messages.warning(request,
                                ("Please indicate the weight of the patient!"))
				return render_to_response(template_name, locals(),
					context_instance=RequestContext(request))


			if request.POST.get('weight') != u"" and request.POST.get('height') != u"":
				weight_height_details = WeightHeightBSAHistory(eventdate = date.today(),
				 weight = request.POST.get('weight'), height = request.POST.get('height'),
				 ART_patient = patient )

				weight_height_details.save()

			elif request.POST.get('weight') != u"" and request.POST.get('height') == u"":
				weight_height_details = WeightHeightBSAHistory(eventdate = date.today(),
				 weight = request.POST.get('weight'),
				 ART_patient = patient )

				weight_height_details.save()



			if form.is_valid():
				visit = form.save(commit = False)
				visit.eventdate = date.today()
				visit.ART_patient = patient
				visit.modified_at = date.today()
				visit.created_at = date.today()
				visit.dateofnextappointment = date.today() + timedelta(days=form.cleaned_data['days_to_TCA'])
				visit.is_active = True
				visit.save()

				appointments, created = appointments_tracker.objects.get_or_create(
					appointment_date = date(visit.dateofnextappointment.year,
						visit.dateofnextappointment.month,visit.dateofnextappointment.day),
					defaults={'slots_taken': 1})
				if not created:
					#if created is false, then there was already a record for that appointment date. So we just increment slots_taken.
					#check if we have not reached the upper limit set
					if appointments.slots_taken < MAX_SLOT_SIZE:
						appointments.slots_taken = appointments.slots_taken + 1
						appointments.save()


				return redirect(dispense, pk = pk, visit_id = visit.pk)
			else:
				return render_to_response(template_name, locals(),
					context_instance=RequestContext(request))

	else:
		form=VisitForm(patient_id = patient.pk)
		return render_to_response(template_name, locals(),
			context_instance=RequestContext(request))

def create_visit_retrospectively(request, pk):
	if not request.user.is_authenticated:
		return redirect(LoginRequest)

	patient = ARTPatient.objects.get(pk = pk)
	todays_date = date.today()
	try:
		last_visit = Visits.objects.filter(ART_patient = patient).latest("eventdate")
	except Visits.DoesNotExist:
		last_visit = None

	try:
                dispensed_today = PatientTransaction.objects.filter(visit = last_visit)
        except PatientTransaction.DoesNotExist:
                dispensed_today = None


	#last_drugs_dispensed = PatientTransaction.objects.filter(visit = last_visit)
	

	template_name = 'visits/_snippets/retrospective_visits.html'
	context = {'patient':patient, 'template_name':template_name}

	if request.method == 'POST':
			form = RetrospectiveVisitForm(request.POST, patient_id = pk)
			context.update({'form': form})

			if request.POST.get('cancel', None):
				return redirect(homepage)
				
			newly_enrolled = 1
			if date(patient.date_therapy_started.year,patient.date_therapy_started.month,patient.date_therapy_started.day) == date(datetime.now().year,datetime.now().month,datetime.now().day):
				newly_enrolled = 2
			updated_data = request.POST.copy()

			if request.POST.get('visittype') == u"":
				updated_data.update({'visittype':2})
				form = VisitForm(data=updated_data, patient_id = pk) 

			if request.POST.get('weight') == u"":
				messages.warning(request,
                                ("Please indicate the weight of the patient!"))
				return render_to_response(template_name, locals(),
					context_instance=RequestContext(request))


			if request.POST.get('weight') != u"" and request.POST.get('height') != u"":
				weight_height_details = WeightHeightBSAHistory(eventdate = date.today(),
				 weight = request.POST.get('weight'), height = request.POST.get('height'),
				 ART_patient = patient )

				weight_height_details.save()

			elif request.POST.get('weight') != u"" and request.POST.get('height') == u"":
				weight_height_details = WeightHeightBSAHistory(eventdate = date.today(),
				 weight = request.POST.get('weight'),
				 ART_patient = patient )

				weight_height_details.save()



			if form.is_valid():
				visit = form.save(commit = False)
				visit.ART_patient = patient
				visit.modified_at = date.today()
				visit.created_at = date.today()
				visit.dateofnextappointment = date.today() + timedelta(days=form.cleaned_data['days_to_TCA'])
				visit.is_active = True
				visit.save()

				appointments, created = appointments_tracker.objects.get_or_create(
					appointment_date = date(visit.dateofnextappointment.year,
						visit.dateofnextappointment.month,visit.dateofnextappointment.day),
					defaults={'slots_taken': 1})
				if not created:
					#if created is false, then there was already a record for that appointment date. So we just increment slots_taken.
					#check if we have not reached the upper limit set
					if appointments.slots_taken < MAX_SLOT_SIZE:
						appointments.slots_taken = appointments.slots_taken + 1
						appointments.save()


				return redirect(dispense, pk = pk, visit_id = visit.pk)
			else:
				return render_to_response(template_name, locals(),
					context_instance=RequestContext(request))

	else:
		form=RetrospectiveVisitForm(patient_id = patient.pk)
		return render_to_response(template_name, locals(),
			context_instance=RequestContext(request))
	
def get_patients_booked(request, tca):
	if tca == 'undefined':
		tca = date.today() + timedelta(days=28)
	if request.is_ajax():
		#tca_date = dateutil.parser.parse(tca)
		slot_size = Slot_size.objects.get(pk = 1)
		try:
			slots_taken = appointments_tracker.objects.get(appointment_date = tca)
			
		except appointments_tracker.DoesNotExist:
			slots_taken = None

		response_data = {}
		if slots_taken == None:
			response_data['slots_taken'] = '0'
			response_data['slot_size'] = slot_size.slot_size


		else:
			response_data['slots_taken'] = slots_taken.slots_taken
			response_data['slot_size'] = slot_size.slot_size

		return HttpResponse(json.dumps(response_data), content_type="application/json")

