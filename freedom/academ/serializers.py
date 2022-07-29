from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import UserDeleteSerializer as BaseUserDeleteSerializer
from rest_framework import serializers
from .models import *


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    """
    Serializer для регистрации пользователей.
    """
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('username', 'email', 'password')


class UserUploadAvatarSerializer(serializers.ModelSerializer):
    """
    Serializer для загрузки аватара пользователя.
    """

    class Meta(BaseUserRegistrationSerializer.Meta):
        model = User
        fields = ('avatar', )


class Test(BaseUserSerializer):
    """
    Serializer для тестирования данных пользователя.
    """
    class Meta(BaseUserSerializer.Meta):
        fields = '__all__'


class MyUserSerializer(BaseUserSerializer):
    """
    Основной serializer для работы с пользователями.
    """
    class Meta(BaseUserSerializer.Meta):
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'is_superuser', 'avatar', 'phone_number')
        read_only_fields = ('username', 'email', 'role', 'is_superuser', )


class BuildingSerializer(serializers.ModelSerializer):
    """
    Serializer для работы с домами.
    """
    class Meta:
        model = Building
        fields = '__all__'


class ApartmentSerializer(serializers.ModelSerializer):
    """
    Serializer для работы с квартирами.
    """
    class Meta:
        model = Apartment
        fields = '__all__'


class FixatedClientSerializer(serializers.ModelSerializer):
    """
    Serializer для работы с зафиксированными клиентами.
    """
    class Meta:
        model = FixatedClient
        fields = '__all__'


class FavoritesSerializer(serializers.ModelSerializer):
    """
    Serializer для работы с зафиксированными клиентами.
    """
    class Meta:
        model = Favorite
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    """
    Serializer для работы с бронью.
    """
    class Meta:
        model = Reservation
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer для работы с записью клиента.
    """
    class Meta:
        model = Appointment
        fields = '__all__'


class SupportTicketSerializer(serializers.ModelSerializer):
    """
    Serializer для работы с записью тикетами в техподдержку.
    """
    class Meta:
        model = SupportTicket
        fields = '__all__'
        # exclude = ('user',)


class ImageGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageGallery
        fields = '__all__'



