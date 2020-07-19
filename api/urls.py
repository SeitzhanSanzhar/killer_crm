from django.contrib import admin
from django.urls import path
from api.views import purchase_request_handler

urlpatterns = [
    path('purchase_request/', purchase_request_handler),
]
