from datetime import date, timedelta

from django import forms
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.forms.formsets import BaseFormSet
from django.forms.formsets import formset_factory
from django.forms.widgets import TextInput

from .models import PatientTransaction, Dosage, Indication
from commodities.models import PhysicalDrug
from ARTRegimen.models import Regimen, DrugsInRegimen, RegimenHistory
from patients.models import ARTPatient
from visits.models import VisitType

class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass


class NumberInput(TextInput):
    input_type = 'number'
    
class PatientTransactionForm(forms.ModelForm):

        def __init__(self, *args, **kwargs):
            patient_id = kwargs.pop('patient_id')
            super(PatientTransactionForm, self).__init__(*args,**kwargs)
            regimen_history = RegimenHistory.objects.filter(ART_patient = get_object_or_404(ARTPatient, pk = patient_id))


            if regimen_history:
                current_regimen = RegimenHistory.objects.filter(ART_patient = get_object_or_404(ARTPatient, pk = patient_id)).order_by("-pk")[0]
                self.fields['physicalDrug'] = forms.ModelChoiceField(
                    queryset = DrugsInRegimen.objects.filter(Q(
                        regimencode = Regimen.objects.filter(regimencode = current_regimen.regimen)) | Q(regimencode = 'OI')),
                        widget=forms.Select(attrs={'class':'formset-control form-control physicalDrug lastrow','id':'physical_drug'}),
                        required=False, empty_label='<Drugs In Regimen>')
            else:
                    self.fields['physicalDrug'] = forms.ModelChoiceField(
                    queryset = DrugsInRegimen.objects.filter(regimencode = 'OI'),
                    widget=forms.Select(attrs={'class':'formset-control form-control physicalDrug lastrow','id':'physical_drug'}),
                    required=False, empty_label='<Drugs In Regimen>')


        arvquantity=forms.IntegerField(widget=NumberInput(
            attrs={'class':'form-control formset-control drugqty' ,'min':0}))

        dosage=forms.CharField(widget=forms.TextInput(
            attrs={'placeholder':'dose',
            'class':'form-control formset-control dose'}))

        duration=forms.CharField(widget=NumberInput(
            attrs={'placeholder':'duration',
            'class':'form-control formset-control' ,'min':0}))

        comment=forms.CharField(widget=forms.Textarea(
            attrs={'placeholder':'comment','rows':1,
            'class':'form-control formset-control'}),required=False)

        indication=forms.ModelChoiceField(
            queryset=Indication.objects.exclude(indicationname__isnull=True).exclude(indicationname__exact=''),
            widget=forms.Select(attrs={'class':'form-control formset-control'}),
             required=False, empty_label='<Indication>')

        
        pillcount = forms.IntegerField(widget=NumberInput(
            attrs={'class':'form-control formset-control','min':0}), required=False)

        batchNo = forms.CharField(widget=forms.HiddenInput(
            attrs={'class':'form-control formset-control selectedbatch'}))


        
        class Meta:
                model=PatientTransaction
                exclude = ('created_at','modified_at','is_active','physicalDrug','operator','visit')
                
def make_form(patient_id, visit_id):
    class PatientTransactionForm(forms.ModelForm):

        def __init__(self, *args, **kwargs):
            super(PatientTransactionForm, self).__init__(*args,**kwargs)
            #self.fields['physicalDrug'].initial = None
            regimen_history = RegimenHistory.objects.filter(ART_patient = get_object_or_404(ARTPatient, pk = patient_id))


            if regimen_history:
                current_regimen = RegimenHistory.objects.filter(ART_patient = get_object_or_404(ARTPatient, pk = patient_id)).order_by("-pk")[0]
                self.fields['physicalDrug'] = forms.ModelChoiceField(
                    queryset = DrugsInRegimen.objects.filter(Q(
                        regimencode = Regimen.objects.filter(regimencode = current_regimen.regimen)) | Q(regimencode = 'OI')),
                        widget=forms.Select(attrs={'class':'formset-control form-control physicalDrug lastrow'}),
                        required=False, empty_label='<Drugs In Regimen>')
            else:
                    self.fields['physicalDrug'] = forms.ModelChoiceField(
                    queryset = DrugsInRegimen.objects.filter(regimencode = 'OI'),
                    widget=forms.Select(attrs={'class':'formset-control form-control physicalDrug lastrow'}),
                    required=False, empty_label='<Drugs In Regimen>')


        arvquantity=forms.IntegerField(widget=NumberInput(
            attrs={'class':'form-control formset-control drugqty' ,'min':0}))

        dosage=forms.CharField(widget=forms.TextInput(
            attrs={'placeholder':'dose',
            'class':'form-control formset-control dose'}))

        duration=forms.CharField(widget=NumberInput(
            attrs={'placeholder':'duration',
            'class':'form-control formset-control' ,'min':0}))

        comment=forms.CharField(widget=forms.Textarea(
            attrs={'placeholder':'comment','rows':1,
            'class':'form-control formset-control'}),required=False)

        indication=forms.ModelChoiceField(
            queryset=Indication.objects.exclude(indicationname__isnull=True).exclude(indicationname__exact=''),
            widget=forms.Select(attrs={'class':'form-control formset-control'}),
             required=False, empty_label='<Indication>')

        
        pillcount = forms.IntegerField(widget=NumberInput(
            attrs={'class':'form-control formset-control','min':0}), required=False)

        batchNo = forms.CharField(widget=forms.HiddenInput(
            attrs={'class':'form-control formset-control selectedbatch'}))


        
        class Meta:
                model=PatientTransaction
                exclude = ('created_at','modified_at','is_active','physicalDrug','operator','visit')
    return PatientTransactionForm



class DosageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DosageForm, self).__init__(*args,**kwargs)

    dose = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Dose',
        'class':'form-control','id':'dose'}),required=False)

    value = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Value',
        'class':'form-control','type':'number'}),required=False)

    frequency = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Frequency',
        'class':'form-control','type':'number'}),required=False)

    class Meta:
            model=Dosage
            exclude = ('created_at','modified_at','is_active','upsize_ts')
