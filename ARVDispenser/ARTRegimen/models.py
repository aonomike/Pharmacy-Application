from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify

from parent_app.Commons import MetaData


class RegimenCategory(MetaData):
    categoryname = models.CharField(db_column='categoryName', max_length=45, blank=True)

    def __unicode__(self):
        return self.categoryname

    def save(self, *args, **kwargs):
        self.slug = slugify(self.categoryname)
        super(RegimenCategory, self).save(*args,**kwargs)

    class Meta:
        db_table = 'tblregimencategory'

class Status(MetaData):
    status = models.CharField(max_length=45, blank=True)
    slug = models.SlugField(max_length=45) 

    def __unicode__(self):
        return self.status

    def save(self,*args,**kwargs):
        self.slug = slugify(self.status)
        super(Status, self).save(*args, **kwargs)

    class Meta:
        db_table = 'tblstatus'

class Regimen(MetaData):
    regimencode = models.CharField(db_column='regimenCode', primary_key=True, max_length=10) 
    regimen = models.CharField(max_length=255, blank=True)
    line = models.IntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True)
    show = models.NullBooleanField(blank=True, null=True) 
    regimencategory = models.ForeignKey(RegimenCategory, db_column='regimenCategory')
    status = models.CharField(max_length=10, blank=True, db_column='status')
    type_of_service = models.CharField(max_length=10, blank=True, db_column='type_of_service')

    def __unicode__(self):
        return self.regimencode

    class Meta:
        db_table = 'tblregimen'

class RegimenChangeReasons(MetaData):
    reasonforchange = models.CharField(db_column='reasonForChange', max_length=100, blank=True) 

    def __unicode__(self):
        return self.reasonforchange

    class Meta:
        db_table = 'tblregimechangereasons'

class RegimenHistory(MetaData):
    ART_patient = models.ForeignKey('patients.ARTPatient', db_column='artID') 
    regimen = models.ForeignKey(Regimen, db_column='tblRegimenId') 
    eventdate = models.DateTimeField(db_column='eventDate', blank=True, null=True) 
    reasonforchange = models.CharField(max_length=45, db_column='reasonForChange', blank=True, null=True) 
    regimen_change_type = models.CharField(max_length=20, blank=True,null=True, db_column='regimen_change_type')

    def __unicode__(self):
        return self.regimen

    class Meta:
        db_table = 'tblregimenhistory'



class DrugsInRegimen(MetaData):
    combinations = models.CharField(max_length=45, blank=True)
    regimencode = models.ForeignKey(Regimen, db_column='regimenCode') 


    def __unicode__(self):
        return self.combinations

    class Meta:
        db_table = 'tbldrugsinregimen'





