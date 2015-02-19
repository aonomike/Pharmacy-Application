from django.db import models
from django.contrib.auth.models import User

from parent_app.Commons import MetaData
from commodities.models import StockTransactionType
# Create your models here.

class DrugFlowTracker(MetaData):
	transactiontype = models.ForeignKey(StockTransactionType, db_column='transactionType' ,blank=True, null=True) 
	transactiondate = models.DateTimeField(db_column='transactionDate', blank=True, null=True)
	tranbatch = models.CharField(db_column='tranBatch', max_length=20)
	arvdrug = models.CharField(db_column='arvDrugId' ,max_length=50, blank=True, null=True)
	expirydate = models.DateTimeField(db_column='expiryDate', blank=True, null=True)
	remarks = models.CharField(max_length=255, blank=True, null=True)
	quantity = models.IntegerField(db_column='quantity', blank=True, null=True)
	operator = models.ForeignKey(User, related_name='myActions')

	class Meta:
                db_table = 'DrugFlowTracker'
