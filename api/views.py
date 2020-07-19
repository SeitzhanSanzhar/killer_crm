from django.shortcuts import render
from xml.etree import cElementTree as ElementTree
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from api.models import KillerManager
from rest_framework.views import APIView
import xmltodict


class PurchaseRequestHandler(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        xml_body = xmltodict.parse(request.body)
        killer_manager = KillerManager.load()
        res = killer_manager.process_order(xml_body['order']['targets']['target'], request.user)
        return JsonResponse(res)