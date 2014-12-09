from django import forms

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from patients.models import ARTPatient
from .models import RegimenHistory, RegimenChangeReasons, Regimen, DrugsInRegimen, RegimenCategory
from commodities.models import PhysicalDrug

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.regimen + ' | '+ obj.regimencode

TYPE_OF_REGIMEN_CHANGE_OPTIONS= [
    ('Line Change','Line Change'),
    ('Drug Substitution','Drug Substitution'),
]

TYPE_OF_REGIMEN_CHANGE_OPTIONS_AND_EMPTY = [('','<Regimen Change Type>')] + TYPE_OF_REGIMEN_CHANGE_OPTIONS

TYPE_OF_SERVICE = [
    ('1','ART'),
    ('2','PEP'),
    ('3','PMTCT'),
    ('5','OI Only'),
]

TYPE_OF_SERVICE_AND_EMPTY = [('','<Type Of Service>')] + TYPE_OF_SERVICE

class RegimenHistoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        patient_id = kwargs.pop('patient_id')
        super(RegimenHistoryForm, self).__init__(*args,**kwargs)
        regimen_history = RegimenHistory.objects.filter(ART_patient = get_object_or_404(ARTPatient, pk = patient_id))

        if regimen_history:
            current_regimen = RegimenHistory.objects.filter(ART_patient = get_object_or_404(ARTPatient, pk = patient_id)).latest('eventdate')
            self.fields['regimen']  = UserModelChoiceField(
                queryset=Regimen.objects.filter(is_active=True).exclude(regimencode = current_regimen.regimen).exclude(show = False),
                widget=forms.Select(attrs={'class':'form-control', 'id':'cmbRegimenChange'}),
                required=True, empty_label='<Select Regimen>')


        else:
            self.fields['regimen']  = UserModelChoiceField(
                queryset=Regimen.objects.filter(is_active=True).exclude(show = False),
                widget=forms.Select(attrs={'class':'form-control', 'id':'cmbRegimenChange'}),
                required=True, empty_label='<Select Regimen>')

    reasonforchange = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Reason For Change','class':'form-control reasonforchange'}), required=False)

    regimen_change_type =forms.ChoiceField(widget=forms.Select(
        attrs={'class':'form-control', 'id':'changeType'}),
         choices=TYPE_OF_REGIMEN_CHANGE_OPTIONS_AND_EMPTY, required=False)

    class Meta:
            model = RegimenHistory
            exclude = ('created_at','modified_at','is_active','ART_patient','eventdate')


class AddDrugToRegimenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        super(AddDrugToRegimenForm, self).__init__(*args,**kwargs)
        regimen = Regimen.objects.get(pk = pk)

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
        


        if drugs:
            arvdrugs = [o.arvdrug for o in drugs] 
            
            self.fields['combinations']  = forms.ModelChoiceField(
                queryset = PhysicalDrug.objects.filter(is_active = True).exclude(
            arvdrug__in = arvdrugs),
                widget=forms.Select(attrs={'class':'form-control', 'id':'cmbRegimenChange'}),
                required=True, empty_label='<Select Drug>')
        else:
            self.fields['combinations']  = forms.ModelChoiceField(
                queryset = PhysicalDrug.objects.filter(is_active = True),
                widget=forms.Select(attrs={'class':'form-control', 'id':'cmbRegimenChange'}),
                required=True, empty_label='<Select Drug>')

    class Meta:
            model = DrugsInRegimen
            exclude = ('created_at','modified_at','is_active','regimencode')

class RegimenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegimenForm, self).__init__(*args,**kwargs)

    regimencode = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Regimen Code','class':'form-control'}))

    regimen = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Regimen','class':'form-control'}))

    line = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Line','class':'form-control','type':'number'}))

    remarks = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder':'Remarks','class':'form-control','rows':'3'}),
    required=False,)

    regimencategory = forms.ModelChoiceField(
        queryset = RegimenCategory.objects.filter(is_active = True),
        widget=forms.Select(attrs={'class':'form-control'}),
        required=True, empty_label='<Select Category>')

    type_of_service = forms.ChoiceField(widget=forms.Select(
        attrs={'placeholder':'<Type Of Service>','class':'form-control','id':'type_of_service'}),
         choices=TYPE_OF_SERVICE_AND_EMPTY, required=False)

    class Meta:
            model = Regimen
            exclude = ('created_at','modified_at','is_active','status')
