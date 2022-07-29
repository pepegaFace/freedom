from rest_framework import generics, status, views, viewsets, mixins
from .permissions import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated


class TicketViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                    mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = ()
        else:
            self.permission_classes = (IsAuthenticated, IsManager)

        return super().get_permissions()

    def get_serializer_class(self):
        self.serializer_class = TicketSerializer
        return self.serializer_class
