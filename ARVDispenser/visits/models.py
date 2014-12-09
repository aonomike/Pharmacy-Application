from __future__ import unicode_literals

from datetime import date

from django.db import models


from parent_app.Commons import MetaData
from patients.models import ARTPatient

class VisitType(MetaData):
    visittype = models.CharField(db_column='visitType', max_length=45, blank=True) 

    def __unicode__(self):
        return self.visittype
        
    
    class Meta:
        db_table = 'tblVisitType'

class Visits(MetaData):
    eventdate = models.DateTimeField(db_column='eventDate', blank=True, null=True)
    ART_patient = models.ForeignKey(ARTPatient, db_column='ART_patient_id')
    dateofnextappointment = models.DateTimeField(db_column='dateOfNextAppointment', blank=True, null=True)
    days_to_TCA = models.IntegerField(db_column='days_to_TCA', blank=True, null=True) 
    visittype = models.ForeignKey(VisitType, db_column='visitType')
    comment = models.TextField(blank=True,  null=True)

    #use this in template to display days_to_next_appointment
    #{{ date.today()|timesince:dateofnextappointment }}
    def calculate_days_to_tca(self, *args, **kwargs):
        if self.dateofnextappointment:
            today = date.today()
            return today.year - self.dateofnextappointment.year - (
                (today.month, today.day) < (self.dateofnextappointment.month, self.dateofnextappointment.day))
        else:
            return 'Not Specified!'

    class Meta:
        db_table = 'tblVisits'

class appointments_tracker(models.Model):
    appointment_date = models.DateField(db_column='appointment_date', primary_key=True)
    slots_taken = models.IntegerField(db_column='slots_taken')

    class Meta:
        db_table = 'appointments_tracker'

class Slot_size(models.Model):
    slot_size = models.IntegerField(db_column='slot_size')
    last_updated_on = models.DateTimeField(db_column='last_updated_on')

    class Meta:
        db_table = 'tblslot_size'