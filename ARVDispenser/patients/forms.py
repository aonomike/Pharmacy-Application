from django import forms

import datetime

from .models import CurrentStatus, ClientSupportDetails, ARTPatient, WeightHeightBSAHistory
from sourceOrDestination.models import ClientSource
from ARTRegimen.models import Regimen

SEX_OPTIONS= [
    ('Male','Male'),
    ('Female','Female'),
    ('Unkown','Unkown'),
]

SEX_OPTIONS_AND_EMPTY = [('','<Gender>')] + SEX_OPTIONS

TYPE_OF_SERVICE = [
    ('ART','ART'),
    ('PEP','PEP'),
    ('OI Only','OI Only'),
]

TYPE_OF_SERVICE_AND_EMPTY = [('','<Type Of Service>')] + TYPE_OF_SERVICE


class search_patient_form(forms.Form):
    def __init__(self, *args, **kwargs):
        super(search_patient_form, self).__init__(*args,**kwargs)

    search_term = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Search By Name Or CCC Number','class':'form-control',
        'autofocus':'true', 'type':'search'}))

class TransitPatientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransitPatientForm, self).__init__(*args,**kwargs)

    CCC_Number=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'CCC Number','class':'form-control',
        'autofocus':'true','id':'cccNumber'}))
    first_name=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'First Name','class':'form-control'}))
    middle_name=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Middle Name','class':'form-control'}), required=False)
    surname=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Surname','class':'form-control'}))

    sex=forms.ChoiceField(widget=forms.Select(
        attrs={'placeholder':'Gender','class':'form-control', 'id':'sex'}),
         choices=SEX_OPTIONS_AND_EMPTY, required=False)

    date_of_birth=forms.DateTimeField(widget=forms.TextInput(
        attrs={'placeholder':'Date Of Birth','class':'form-control', 'id':'dob'}),
    required=False)
    pregnant=forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'placeholder':'Pregnant','class':'checkbox-inline hidden','id':'pregnant'}),required=False)
    cellphone_no=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Mobile Number','class':'form-control'}),required=False)


    class Meta:
            model=ARTPatient
            exclude = ('address','date_therapy_started','other_disease_conditions','adr_or_side_effects','current_status','regimen'
                'TB','smokes','drinks','type_of_service','client_source','ART_start_date','alternate_contact','created_at',
                'modified_at','is_active','slug','client_supported_by')

class ARTPatientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ARTPatientForm, self).__init__(*args,**kwargs)

    CCC_Number=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'CCC Number','class':'form-control',
        'autofocus':'true','id':'cccNumber'}))
    first_name=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'First Name','class':'form-control'}))
    middle_name=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Middle Name','class':'form-control'}), required=False)
    surname=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Surname','class':'form-control'}))

    sex=forms.ChoiceField(widget=forms.Select(
        attrs={'placeholder':'Gender','class':'form-control', 'id':'sex'}),
         choices=SEX_OPTIONS_AND_EMPTY, required=False)

    address=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Address','class':'form-control'}),required=False)
    date_of_birth=forms.DateTimeField(widget=forms.TextInput(
        attrs={'placeholder':'Date Of Birth','class':'form-control', 'id':'dob'}),
    required=False)
    date_therapy_started=forms.DateTimeField(widget=forms.TextInput(
        attrs={'placeholder':'Date Enrolled','class':'form-control','id':'date_enrolled'}))
    other_disease_conditions=forms.CharField(widget=forms.Textarea(
        attrs={'placeholder':'Other Disease Conditions','class':'form-control',
        'rows':'3'}),required=False)
    adr_or_side_effects=forms.CharField(widget=forms.Textarea(
        attrs={'placeholder':'ADR Or Side Effects','class':'form-control',
        'rows':3}),required=False)
    TB=forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'placeholder':'TB'}),required=False)
    pregnant=forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'placeholder':'Pregnant','class':'checkbox-inline hidden','id':'pregnant'}),required=False)
    smokes=forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'placeholder':'Smokes','class':'checkbox-inline'}),required=False)
    drinks=forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'placeholder':'Drinks','class':'checkbox-inline'}),required=False)
    type_of_service=forms.ChoiceField(widget=forms.Select(
        attrs={'placeholder':'<Type Of Service>','class':'form-control','id':'type_of_service'}),
         choices=TYPE_OF_SERVICE_AND_EMPTY, required=False)
    client_source=forms.ModelChoiceField(
        queryset=ClientSource.objects.filter(is_active=True),
        widget=forms.Select(attrs={'placeholder':'Client Source','class':'form-control'}),
         required=False, empty_label='<Select Client Source>')
    ART_start_date=forms.DateTimeField(widget=forms.TextInput(
        attrs={'placeholder':'ART Start Date','class':'form-control hidden',
        'id':'ARTStart'}), required = False)
    cellphone_no=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Mobile Number','class':'form-control'}),required=False)
    alternate_contact=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Alternate Contact','class':'form-control'}),required=False)
    current_status=forms.ModelChoiceField(
        queryset=CurrentStatus.objects.filter(is_active=True),
        widget=forms.Select(attrs={'placeholder':'Current Status','class':'form-control'}), 
        required=False, empty_label='<Select Current Status>')
    regimen=forms.ModelChoiceField(queryset=Regimen.objects.filter(is_active=True),
        widget=forms.Select(
        attrs={'placeholder':'<Start Regimen>','class':'form-control hidden', 'id':'start_regimen'}),
         required=False)


    class Meta:
            model=ARTPatient
            exclude = ('created_at','modified_at','is_active','slug','client_supported_by')

    #change string inputs to upper case
    #def clean(self):
     #   return dict((k, v.strip().upper()) for k, v in 
      #      self.cleaned_data.iteritems() if isinstance(v, basestring))

class WeightHeightBSAHistoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WeightHeightBSAHistoryForm, self).__init__(*args,**kwargs)

    weight=forms.FloatField(widget=forms.TextInput(
        attrs={'placeholder':'weight','class':'form-control',
        'autofocus':'true','type':'number'}))
    height=forms.FloatField(widget=forms.TextInput(
        attrs={'placeholder':'height','class':'form-control','type':'number'}))
    eventdate=forms.DateTimeField(widget=forms.TextInput(
        attrs={'placeholder':'Date Taken','class':'form-control datepicker'}),
    required=False)

    class Meta:
            model=WeightHeightBSAHistory
            exclude = ('created_at','modified_at','is_active','ART_patient')











