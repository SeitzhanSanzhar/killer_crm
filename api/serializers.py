from rest_framework import serializers
from api.models import Contract

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'