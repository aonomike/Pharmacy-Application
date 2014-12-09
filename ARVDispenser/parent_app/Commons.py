from django.db import models
from django.contrib.auth.models import User


class MetaData(models.Model):
    created_at=models.DateTimeField(auto_now_add=True, editable=False)
    modified_at=models.DateTimeField(auto_now=True, editable=False)
    #had problems adding created_by and modified_by, will refactor later
    #created_by=models.ForeignKey(User, related_name='mycreations')
    #createdOrModified_by=models.ForeignKey(User,related_name='myModifiedModels', null=True)
    is_active=models.BooleanField(default=True)

    def convertDatetimeToString(o):
    	DATE_FORMAT = "%Y-%m-%d"
    	TIME_FORMAT = "%H:%M:%S"

    	if isinstance(o, datetime.date):
    		return o.strftime(DATE_FORMAT)
    	elif isinstance(o, datetime.time):
    		return o.strftime(TIME_FORMAT)
    	elif isinstance(o, datetime.datetime):
    		return o.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT))

    class Meta:
        abstract=True

