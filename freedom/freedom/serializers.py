from rest_framework import serializers
from .models import *


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer для работы с заявками.
    """
    class Meta:
        model = Ticket
        fields = '__all__'
