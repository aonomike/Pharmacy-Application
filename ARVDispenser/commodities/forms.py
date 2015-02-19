from datetime import date

from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import TextInput

from .models import DrugDhysicalTran, PhysicalDrug, StockTransactionType, GenericName
from ARTRegimen.models import Regimen, DrugsInRegimen


DRUG_UNIT_OPTIONS= [
    ('Tablet','Tablet'),
    ('Bottle','Bottle'),
    ('Capsule','Capsule'),
    ('Pack','Pack'),
    ('Ppack','Ppack'),
]

DRUG_UNIT_OPTIONS_AND_EMPTY = [('','<Drug Unit>')] + DRUG_UNIT_OPTIONS

class ModelChoiceFieldNoValidation(forms.ModelChoiceField):
    def validate(self, value):
        pass
class NumberInput(TextInput):
    input_type = 'number'
    
def make_forms():
    class DrugDhysicalTranForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super(DrugDhysicalTranForm, self).__init__(*args,**kwargs)
            
        tranbatch = forms.CharField(widget=forms.TextInput(
            attrs={'placeholder':'Batch No.','class':'form-control formset-control'}))

        arvdrug = forms.ModelChoiceField(
            queryset=PhysicalDrug.objects.filter(is_active=True),
            widget=forms.Select(attrs={'class':'form-control formset-control lastrow physicalDrug'}),required = True, empty_label='<Select Drug>')

        transactiontype = forms.ModelChoiceField(
            queryset=StockTransactionType.objects.filter(is_active=True),
            widget=forms.Select(attrs={'class':'form-control formset-control transactiontype'}), empty_label='<Transaction Type>')

        transactiondate = forms.DateTimeField(widget=forms.TextInput(
            attrs={'placeholder':'Transaction Date','class':'form-control transactiondate formset-control'}),
        required=True, initial = date.today())

        quantity = forms.IntegerField(widget=NumberInput(
            attrs={'class':'form-control formset-control qty','placeholder':'quantity'
            ,'type':'number'}),required=True)

        expirydate = forms.DateTimeField(widget=forms.TextInput(
            attrs={'placeholder':'Expiry Date','class':'form-control expdate formset-control'}))

        remarks = forms.CharField(widget=forms.Textarea(
            attrs={'placeholder':'remarks','rows':1,
            'class':'form-control formset-control'}),required=False)

        packs = forms.IntegerField(widget=NumberInput(
            attrs={'class':'form-control formset-control packs', 'placeholder':'packs'}))

        unitcost = forms.DecimalField(widget=NumberInput(
            attrs={'class':'form-control formset-control unit_cost', 'placeholder':'unit cost'
            ,'type':'number'}),initial = 0.00, required=False)

        ref_number = forms.CharField(widget=forms.TextInput(
            attrs={'placeholder':'Ref No.','class':'form-control formset-control'}))

        source_or_destination = forms.CharField(widget=forms.HiddenInput(
            attrs={'class':'form-control formset-control source_or_destination'}), required=False)

        class Meta:
                model = DrugDhysicalTran
                exclude = ('created_at','modified_at','is_active')
    return DrugDhysicalTranForm

class DrugDhysicalTranForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super(DrugDhysicalTranForm, self).__init__(*args,**kwargs)
            
        tranbatch = forms.CharField(widget=forms.TextInput(
            attrs={'placeholder':'Batch No.','class':'form-control formset-control'}))

        arvdrug = forms.ModelChoiceField(
            queryset=PhysicalDrug.objects.filter(is_active=True),
            widget=forms.Select(attrs={'class':'form-control formset-control lastrow','id':'physicalDrugs'}),required = True, empty_label='<Select Drug>')

        transactiontype = forms.ModelChoiceField(
            queryset=StockTransactionType.objects.filter(is_active=True),
            widget=forms.Select(attrs={'class':'form-control formset-control','id':'transactiontype'}), empty_label='<Transaction Type>')

        transactiondate = forms.DateTimeField(widget=forms.TextInput(
            attrs={'placeholder':'Transaction Date','class':'form-control transactiondate formset-control'}),
        required=True, initial = date.today())

        quantity = forms.IntegerField(widget=NumberInput(
            attrs={'class':'form-control formset-control','id':'qty','placeholder':'quantity'
            ,'type':'number'}),required=True)

        expirydate = forms.DateTimeField(widget=forms.TextInput(
            attrs={'placeholder':'Expiry Date','class':'form-control expdate formset-control'}))

        remarks = forms.CharField(widget=forms.Textarea(
            attrs={'placeholder':'remarks','rows':1,
            'class':'form-control formset-control'}),required=False)

        packs = forms.IntegerField(widget=NumberInput(
            attrs={'class':'form-control formset-control','id':'packs', 'placeholder':'packs'}))

        unitcost = forms.DecimalField(widget=NumberInput(
            attrs={'class':'form-control formset-control unit_cost', 'placeholder':'unit cost'
            ,'type':'number'}),initial = 0.00, required=False)

        ref_number = forms.CharField(widget=forms.TextInput(
            attrs={'placeholder':'Ref No.','class':'form-control formset-control'}))

        source_or_destination = forms.CharField(widget=forms.HiddenInput(
            attrs={'class':'form-control formset-control source_or_destination'}), required=False)

        class Meta:
                model = DrugDhysicalTran
                exclude = ('created_at','modified_at','is_active')

class DrugRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DrugRegistrationForm, self).__init__(*args,**kwargs)
        
    arvdrug = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Drug','class':'form-control'}))

    drugunit = forms.ChoiceField(widget=forms.Select(
        attrs={'class':'form-control'}),
         choices=DRUG_UNIT_OPTIONS_AND_EMPTY, required=False)

    packsize = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Pack Size','class':'form-control'}))

    description =forms.CharField(widget=forms.Textarea(
        attrs={'placeholder':'description','rows':4,
        'class':'form-control'}),required=False)

    minimumlevel = forms.IntegerField(widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Min. Level'
        ,'type':'number'}), required = False)

    maximumlevel = forms.IntegerField(widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Max. Level'
        ,'type':'number'}), required = False) 

    reorderlevel = forms.IntegerField(widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Reorder Level'
        ,'type':'number'}), required = False) 

    genericname = forms.ModelChoiceField(
        queryset=GenericName.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class':'form-control'})
        , empty_label='<Generic Name>')

    class Meta:
            model = PhysicalDrug
            exclude = ('created_at','modified_at','is_active')
