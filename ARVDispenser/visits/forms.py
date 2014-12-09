from datetime import date, timedelta, datetime

from django import forms
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import VisitType, Visits
from commodities.models import PhysicalDrug
from ARTRegimen.models import Regimen, DrugsInRegimen, RegimenHistory
from patients.models import ARTPatient


class VisitForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        patient_id = kwargs.pop('patient_id')
        super(VisitForm, self).__init__(*args,**kwargs)
        patient = ARTPatient.objects.get(pk = patient_id)

        newly_enrolled = False

        if date(patient.created_at.year,
            patient.created_at.month,patient.created_at.day) == date(datetime.now().year,datetime.now().month,datetime.now().day):
            newly_enrolled = True



        if patient.calculate_age() < 15 or patient.calculate_age() == 15:

            self.fields['days_to_TCA'] = forms.IntegerField(widget=forms.TextInput(
                attrs={'class':'form-control', 'placeholder':'Days To TCA','id':'days_to_TCA','type':'number'}), initial = 28)

        elif newly_enrolled:

            self.fields['days_to_TCA'] = forms.IntegerField(widget=forms.TextInput(
                attrs={'class':'form-control', 'placeholder':'Days To TCA','id':'days_to_TCA','type':'number'}), initial = 14)

        elif not newly_enrolled and patient.calculate_age() > 15:

            self.fields['days_to_TCA'] = forms.IntegerField(widget=forms.TextInput(
                attrs={'class':'form-control', 'placeholder':'Days To TCA','id':'days_to_TCA','type':'number'}), initial = 84)


    visittype  = forms.ModelChoiceField(queryset=VisitType.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class':'form-control','name':'visittype'}),
         required=False, empty_label='<Visit Type>')



    class Meta:
    	model=Visits
    	exclude = ('created_at','modified_at','is_active','ART_patient','eventdate','dateofnextappointment')

class RetrospectiveVisitForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        patient_id = kwargs.pop('patient_id')
        super(RetrospectiveVisitForm, self).__init__(*args,**kwargs)
        patient = ARTPatient.objects.get(pk = patient_id)

        newly_enrolled = False

        if date(patient.created_at.year,
            patient.created_at.month,patient.created_at.day) == date(datetime.now().year,datetime.now().month,datetime.now().day):
            newly_enrolled = True



        if patient.calculate_age() < 15 or patient.calculate_age() == 15:

            self.fields['days_to_TCA'] = forms.IntegerField(widget=forms.TextInput(
                attrs={'class':'form-control', 'placeholder':'Days To TCA','id':'days_to_TCA','type':'number'}), initial = 28)

        elif newly_enrolled:

            self.fields['days_to_TCA'] = forms.IntegerField(widget=forms.TextInput(
                attrs={'class':'form-control', 'placeholder':'Days To TCA','id':'days_to_TCA','type':'number'}), initial = 14)

        elif not newly_enrolled and patient.calculate_age() > 15:

            self.fields['days_to_TCA'] = forms.IntegerField(widget=forms.TextInput(
                attrs={'class':'form-control', 'placeholder':'Days To TCA','id':'days_to_TCA','type':'number'}), initial = 84)


    visittype  = forms.ModelChoiceField(queryset=VisitType.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class':'form-control','name':'visittype'}),
         required=False, empty_label='<Visit Type>')

    eventdate = forms.DateTimeField(widget=forms.TextInput(
        attrs={'placeholder':'Visit Date','class':'form-control datepicker','required':'true'}),required=True, initial=datetime.now)

    comment=forms.CharField(widget=forms.Textarea(attrs={'placeholder':'comment','rows':3,
            'class':'form-control formset-control','required':'true'}),required=True)



    class Meta:
    	model=Visits
    	exclude = ('created_at','modified_at','is_active','ART_patient','dateofnextappointment')
