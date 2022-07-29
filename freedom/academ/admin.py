from django.contrib import admin
from .models import *


@admin.register(User)
class AdmUser(admin.ModelAdmin):
    list_display = ('id', 'email', 'username')
    filter_horizontal = ('groups', 'user_permissions')

    def get_queryset(self, request):
        return self.model.objects_unfiltered.all()


@admin.register(Building)
class AdmBuilding(admin.ModelAdmin):
    list_display = ('id', 'address', 'floors', 'sections', 'types')


@admin.register(Apartment)
class AdmApartment(admin.ModelAdmin):
    list_display = ('id', 'building', 'number', 'floor', 'section', 'type', 'area', 'reserved', 'cost')


@admin.register(Reservation)
class AdmReservation(admin.ModelAdmin):
    list_display = ('id', 'apartment', 'date_added', 'expiration_date')


@admin.register(Appointment)
class AdmAppointment(admin.ModelAdmin):
    list_display = ('id', 'manager', 'client', 'date', 'time', 'building', 'apartment')


@admin.register(FixatedClient)
class AdmFixatedClient(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'patronymic', 'phone_number', 'apartment', 'info')


@admin.register(Favorite)
class AdmFavorites(admin.ModelAdmin):
    list_display = ('id', 'user', 'apartment')


@admin.register(SupportTicket)
class AdmSupport(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'topic_type', 'message')


@admin.register(ImageGallery)
class AdmImageGallery(admin.ModelAdmin):
    list_display = ('id', 'building', 'image')
