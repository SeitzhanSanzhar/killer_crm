from django.contrib import admin
from api.models import KillerManager, Victim, Link, ContractToVictim, Contract
# Register your models here.

admin.site.register(KillerManager)
admin.site.register(Victim)
admin.site.register(Link)
admin.site.register(ContractToVictim)
admin.site.register(Contract)