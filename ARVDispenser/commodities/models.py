from __future__ import unicode_literals

from django.db import models

from parent_app.Commons import MetaData
from django.core.exceptions import ValidationError

class Typeofcommodity(MetaData):
    commodityname = models.CharField(db_column='commodityName', max_length=45, blank=True)
    description = models.CharField(max_length=45, blank=True)
    
    class Meta:
        db_table = 'typeofcommodity'

class DrugUnit(MetaData):
    unitname = models.CharField(db_column='unitName', max_length=45, blank=True)

    class Meta:
        db_table = 'tbldrugunit'

class GenericName(MetaData):
    genericname = models.CharField(db_column='genericName', max_length=50, blank=True)

    def __unicode__(self):
        return self.genericname

    class Meta:
        db_table = 'tblgenericname' 

class StockTransactionType(MetaData):
    description = models.CharField(max_length=45, blank=True)
    reporttitle = models.CharField(db_column='reportTitle', max_length=45, blank=True) 

    def __unicode__(self):
        return self.description

    class Meta:
        db_table = 'tblstocktransactiontype'

class PhysicalDrug(MetaData):
    arvdrug = models.CharField(db_column='arvDrug', unique=True, max_length=50) 
    drugunit = models.CharField( db_column='drugUnit',  max_length=50) 
    packsize = models.CharField(db_column='packSize', max_length=45, blank=True)
    description = models.TextField(blank=True, null=True)
    minimumlevel = models.IntegerField(db_column='minimumLevel', blank=True, null=True) 
    maximumlevel = models.IntegerField(db_column='maximumLevel', blank=True, null=True) 
    reorderlevel = models.IntegerField(db_column='reorderLEvel', blank=True, null=True) 
    genericname = models.ForeignKey(GenericName, db_column='genericName') 
    std_dose = models.CharField(db_column='std_dose', max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.arvdrug

    class Meta:
        db_table = 'tblphysicaldrug'

 

class DrugBrandName(MetaData):
    arvdrugsid = models.CharField(db_column='arvDrugsID', primary_key=True, max_length=50) 
    brandname = models.CharField(db_column='brandName', max_length=50, blank=True) 
    
    class Meta:
        db_table = 'tbldrugbrandname' 

class DrugDhysicalTran(MetaData):
    stocktransactionnumber = models.AutoField(db_column='stockTransactionNumber', primary_key=True)
    tranbatch = models.CharField(db_column='tranBatch', max_length=20) 
    arvdrug = models.CharField(db_column='arvDrugId' ,max_length=50, blank=True, null=True) 
    transactiontype = models.ForeignKey(StockTransactionType, db_column='transactionType' ,blank=True, null=True) 
    transactiondate = models.DateTimeField(db_column='transactionDate', blank=True, null=True)
    packs = models.IntegerField(db_column='packs', blank=True, null=True) 
    expirydate = models.DateTimeField(db_column='expiryDate', blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(db_column='quantity', blank=True, null=True) 
    unitcost = models.DecimalField(db_column='unitCost', max_digits=10, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    source_or_destination = models.CharField(db_column='source_or_destination', max_length=45, blank=True, null=True) 
    ref_number = models.CharField(db_column='ref_number', max_length=45, blank=True, null=True)
    
    def validate_expirydate(self):
    	if self.expirydate < self.transactiondate:
    		raise ValidationError('Expiry Date Cannot Be Earlier Than Transaction Date')

    def getARVDrug(self):
        return PhysicalDrug.objects.get(arvdrug = self.arvdrug)

    class Meta:
        db_table = 'tbldrugphysicaltran'    

