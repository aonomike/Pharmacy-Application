from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from parent_app.Commons import MetaData
from patients.models import ARTPatient
from visits.models import Visits
from commodities.models import PhysicalDrug

class Indication(MetaData):
    indicationcode = models.CharField(db_column='indicationCode', max_length=10, unique=True) 
    indicationname = models.CharField(db_column='indicationName', max_length=45, blank=True)

    def __unicode__(self):
        return self.indicationname


    class Meta:
        db_table = 'tblindication'
        unique_together=('indicationcode','indicationname')

class Dosage(MetaData):
    dose = models.CharField(primary_key=True, max_length=20)
    value = models.FloatField(blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)
    upsize_ts = models.DateTimeField(blank=True, null=True)#whats this field?

    def __unicode__(self):
        return self.dose
    
    class Meta:
        db_table = 'tbldosage'

class PatientTransaction(MetaData):
    transactioncode = models.AutoField(db_column='transactionCode', primary_key=True)
    visit= models.ForeignKey(Visits, db_column='visit_id') 
    physicalDrug = models.ForeignKey(PhysicalDrug, db_column='drugId') 
    arvquantity = models.IntegerField(db_column='arvQuantity', blank=True, null=True) 
    dosage = models.CharField(max_length=20, db_column='dosage', null=True)
    duration = models.CharField(max_length=45, blank=True)
    comment = models.TextField(blank=True)
    indication = models.ForeignKey(Indication, db_column='indicationCode', blank=True, null=True)
    operator = models.ForeignKey(User, db_column='operator')
    pillcount = models.IntegerField(db_column='pillCount', blank=True, null=True)
    batchNo = models.CharField(max_length=15)
    
    #everytime  we create a transaction, we also  deduct from the stocks
    def save(self, drug_qty, *args,**kwargs):
        super(PatientTransaction, self).save(*args, **kwargs)
        drug_qty = drug_qty - self.arvquantity
        return drug_qty

    def save_edit(self, drug_qty, old_qty, *args,**kwargs):
            super(PatientTransaction, self).save(*args, **kwargs)
            if old_qty == self.arvquantity:
                pass
            else:
                drug_qty = drug_qty +(old_qty - self.arvquantity)
            return drug_qty
            
    class Meta:
        db_table = 'tblpatienttransaction'

