from __future__ import unicode_literals

from django.db import models

from parent_app.Commons import MetaData


class ClientSource(MetaData): 
    sourcename = models.CharField(db_column='sourceName',max_length=45, blank=True, null=True)
    description = models.CharField(max_length=45, blank=True)

    def __unicode__(self):
        return self.sourcename
    
    class Meta:
        db_table = 'tblclientsource'

class DrugSource(MetaData):
    sourcecode = models.AutoField(db_column='sourceCode',primary_key=True)
    sourcename = models.CharField(db_column='sourceName', max_length=45, blank=True) 
    
    class Meta:
        db_table = 'tbldrugsource'
        
class DrugDestination(MetaData):
    destination_name = models.CharField(db_column='Name', max_length=45, blank=True) 

    class Meta:
        db_table = 'tbldrugdestination'

class Region(MetaData):
    regioncode = models.AutoField(db_column='regionCode', primary_key=True) 
    region = models.CharField(max_length=45, blank=True)
    
    class Meta:
        db_table = 'tblregion'

class Districts(MetaData):
    districtcode = models.AutoField(db_column='districtCode', primary_key=True)
    districtname = models.CharField(db_column='districtName', max_length=45, blank=True) 
    regionid = models.ForeignKey(Region, db_column='regionId') 
    
    class Meta:
        db_table = 'tbldistricts'

class HealthFacility(MetaData):
    mflcode = models.IntegerField(db_column='mflCode', unique=True)
    facilityname = models.CharField(db_column='facilityName', max_length=45, blank=True) 
    districtcode = models.ForeignKey(Districts, db_column='districtCode')
    
    class Meta:
        db_table = 'tblhealthfacility'
        unique_together=('mflcode','facilityname')

class Organization(MetaData):
    organizationcode = models.AutoField(db_column='organizationCode', primary_key=True) 
    organization = models.CharField(max_length=45, blank=True)
    adultage = models.IntegerField(db_column='adultAge', blank=True, null=True)
    maxpatients = models.IntegerField(db_column='maxPatients', blank=True, null=True) 
    districtcode = models.ForeignKey(Districts, db_column='districtCode')
    goksupport = models.BooleanField(db_column='gokSupport', default=False) 
    msfsupport = models.BooleanField(db_column='msfSupport', default=False) 
    pepfarsupport = models.BooleanField(db_column='pepfarSupport', default=False) 
    artservices = models.BooleanField(db_column='artServices', default=False) 
    pmtctservices = models.BooleanField(db_column='pmtctServices', default=False) 
    pepservices = models.BooleanField(db_column='pepServices', default=False) 

    class Meta:
        db_table = 'tblorganization'