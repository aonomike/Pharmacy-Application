import json

from django.http import HttpResponse

from .models import DrugSource, DrugDestination


def get_drug_source_or_destination(request):
	if request.is_ajax():
		drug_sources = None
		drug_desinations = None

		if request.POST.get('act') == u"source":
			drug_sources = DrugSource.objects.all()

		if request.POST.get('act') == u"destination":
			drug_desinations = DrugDestination.objects.all()
			
		print "ACT: " + request.POST.get('act')
		response_data = {}
		batchNos_list = []
		if drug_sources:
			one_batch = {}
			for batch in drug_sources:
				one_batch[batch.sourcename] = batch.sourcename
				batchNos_list.append(batch.sourcename)

		if drug_desinations:
			one_batch = {}
			for batch in drug_desinations:
				one_batch[batch.destination_name] = batch.destination_name
				batchNos_list.append(batch.destination_name)

		

		response_data['batches'] = batchNos_list
		return HttpResponse(json.dumps(response_data), content_type="application/json")