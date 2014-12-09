from __future__ import unicode_literals

import math
from datetime import date

from django.db import models
from django.template.defaultfilters import slugify


from parent_app.Commons import MetaData
from sourceOrDestination.models import ClientSource
from ARTRegimen.models import Regimen




class ClientSupportDetails(MetaData):
    clientsupportid = models.AutoField(db_column='clientSupportId', primary_key=True) 
    clientsupport = models.CharField(db_column='clientSupport', max_length=45, blank=True) 
    
    def __unicode__(self):
        return self.clientsupport

    class Meta:
        db_table = 'tblclientsupportdetails'

class CurrentStatus(MetaData):
    currentstatusid = models.AutoField(db_column='currentStatusID', primary_key=True) 
    currentstatus = models.CharField(db_column='currentStatus', max_length=45, blank=True) 

    def __unicode__(self):
        return self.currentstatus
    
    class Meta:
        db_table = 'tblcurrentstatus'


class ARTPatient(MetaData):
    CCC_Number=models.CharField(unique=True,db_column='cccNumber', max_length=45, blank=True)
    first_name = models.CharField(db_column='firstName', max_length=45, blank=True)
    middle_name = models.CharField(db_column='middleName', max_length=45, blank=True, null=True) 
    surname = models.CharField(max_length=45, blank=True)
    sex = models.CharField(max_length=10, blank=True)
    date_therapy_started = models.DateTimeField(db_column='dateTherapyStarted', blank=True, null=True) 
    other_disease_conditions = models.TextField(db_column = 'otherDiseaseConditions', blank = True)
    adr_or_side_effects = models.TextField(db_column='ADRorSideEffects', blank=True)
    pregnant = models.BooleanField(default=False)
    other_drugs = models.TextField(db_column='otherDrugs', blank=True) 
    type_of_service = models.CharField(max_length=10, blank=True, db_column='typeOfService')
    address = models.CharField(max_length=45, blank=True)
    client_source = models.ForeignKey(ClientSource, db_column='clientSourceId',blank=True, null=True) 
    TB = models.BooleanField(default=False)
    ART_start_date = models.DateTimeField(db_column='artStartDate', blank=True, null=True) 
    date_of_birth = models.DateTimeField(db_column='dateOfBirth', blank=True, null=True) 
    place_of_birth = models.CharField(db_column='placeOfBirth', max_length=45, blank=True) 
    cellphone_no = models.CharField(db_column='cellPhone', max_length=45, blank=True)
    alternate_contact = models.CharField(db_column='alternateContact', max_length=45, blank=True)
    smokes = models.BooleanField(default=False)
    drinks = models.BooleanField(default=False) 
    client_supported_by = models.ForeignKey(ClientSupportDetails, db_column='clientSupportedBy',blank=True, null=True) 
    current_status = models.ForeignKey(CurrentStatus, db_column='currentStatus',blank=True, null=True)
    regimen = models.CharField(max_length=10, blank=True, db_column='regimen', null=True) 


    def __unicode__(self):
        return self.first_name + ' '  + self.middle_name + ' '  + self.surname

    def calculate_age(self, *args, **kwargs):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        else:
            return 'Not Specified!'

    def get_regimen(self):
        regimen = Regimen.objects.get(regimencode = self.regimen)
        return regimen.regimencode + ' | '+regimen.regimen

    def save(self,*args,**kwargs):
        full_name = self.first_name + ' '+ self.middle_name + ' ' + self.surname
        self.slug=slugify(full_name)
        self.first_name = self.first_name.upper()
        self.middle_name = self.middle_name.upper()
        self.surname = self.surname.upper()
        self.address = self.address.upper()
        self.other_drugs = self.other_drugs.upper()
        self.adr_or_side_effects = self.adr_or_side_effects.upper()
        self.other_disease_conditions = self.other_disease_conditions.upper()
        super(ARTPatient, self).save(*args,**kwargs)
        

    class Meta:
        db_table = 'tblartpatientmasterinformation'
        ordering=['-created_at']

class WeightHeightBSAHistory(MetaData):
    bsacode = models.AutoField(db_column='bsaCode', primary_key=True) 
    eventdate = models.DateTimeField(db_column='eventDate', blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    ART_patient = models.ForeignKey(ARTPatient, db_column='artID') 

    #bsa will be calculated by this formula: =Sqr([Weightonstart]*[StartHeight]/3600).
    def calculate_BSA(self):
        if self.height is None:
            return 0.1 * math.pow(self.weight, (2 / 3))
        else:
            return math.sqrt((self.weight * self.height)/3600)
        

    def __unicode__(self):
        return self.ART_patient + ' = '+self.calculate_BSA

    class Meta:
        db_table = 'tblweightheightbsahistory'



