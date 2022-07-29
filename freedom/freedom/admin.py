from django.contrib import admin
from .models import *


@admin.register(Ticket)
class AdmTicket(admin.ModelAdmin):
    list_display = ('id', 'address', 'rooms', 'date', 'name', 'phone_number')

    def get_queryset(self, request):
        return self.model.objects_unfiltered.all()
