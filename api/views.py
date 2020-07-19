from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from api.models import KillerManager, Contract
from rest_framework.views import APIView
from api.serializers import ContractSerializer, VictimSerializer
from django.db import models
import json
import xmltodict


class SuccessPaymentListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ContractSerializer

    def get_queryset(self):
        return Contract.objects.filter(payed=True).filter(user=self.request.user)


class PayContractView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        json_body = json.loads(request.body)
        contract_id = json_body['contract_id']
        amount = json_body['amount']
        try:
            contract = Contract.objects.get(id = contract_id)
        except models.ObjectDoesNotExist:
            return JsonResponse({'result': 'contract_id does not exist'})
        return JsonResponse(contract.pay(amount), safe=False)

class ContractListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        res = []
        queryset = Contract.objects.filter(user=user)
        for contract in queryset:
            cur_contract = ContractSerializer(contract).data
            victims = contract.get_victim_list()
            for victim in victims:
                cur_contract[victim.username] = VictimSerializer(victim).data
            res.append(cur_contract)
        return JsonResponse(res, safe=False)


class PurchaseRequestHandler(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        xml_body = xmltodict.parse(request.body)
        killer_manager = KillerManager.load()
        res = killer_manager.process_order(xml_body['order']['targets']['target'], request.user)
        return JsonResponse(res)