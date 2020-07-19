from django.contrib import admin
from django.urls import path
from api.views import PurchaseRequestHandler, ContractListView, PayContractView, SuccessPaymentListView
from api.auth_view import logout, login

urlpatterns = [
    path('purchase_request/', PurchaseRequestHandler.as_view()),
    path('login/', login),
    path('logout/', logout),
    path('contract_list/', ContractListView.as_view()),
    path('pay_contract/', PayContractView.as_view()),
    path('get_success_payments/', SuccessPaymentListView.as_view())
]
