from django.contrib import admin
from api.models import KillerManager, Victim, Link, OrdertoVictim, Order
# Register your models here.

admin.site.register(KillerManager)
admin.site.register(Victim)
admin.site.register(Link)
admin.site.register(OrdertoVictim)
admin.site.register(Order)