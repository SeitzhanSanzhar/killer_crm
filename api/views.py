from django.shortcuts import render
from xml.etree import cElementTree as ElementTree
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import KillerManager
import xmltodict

@csrf_exempt
def purchase_request_handler(request):
    xml_body = xmltodict.parse(request.body)
    killer_manager = KillerManager.load()
    res = killer_manager.process_order(xml_body['order']['targets']['target'])
    return JsonResponse(res)