from django.contrib import admin
from django.urls import path
from api.views import PurchaseRequestHandler
from api.auth_view import logout, login

urlpatterns = [
    path('purchase_request/', PurchaseRequestHandler.as_view()),
    path('login/', login),
    path('logout/', logout),
]
