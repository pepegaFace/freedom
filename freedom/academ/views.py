from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework import generics, status, views, viewsets, mixins
from rest_framework.response import Response
from freedom.permissions import *
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework.views import APIView


# Additional functions
def get_table_fields_by_id(index, table):
    """
    Получение данных полей rows из таблицы table по index
    SQL запрос: SELECT * FROM "academ_table" WHERE "academ_table"."id" = index
    @param table: таблица в базе данных
    @param index: идентификатор
    @return: значения из всех столбцов
    """
    query = table.objects.filter(
        id=index)
    result = []
    if query.values():
        result = query.values()[0]
    return result


# Create your views here.

class UploadAvatarViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    parser_classes = (MultiPartParser, )
    serializer_class = UserUploadAvatarSerializer
    queryset = User.objects.all()

    def perform_update(self, serializer):
        serializer.save()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.filter(pk=self.request.user.pk)

    def get_permissions(self):
        self.permission_classes = (IsSelf, )
        return super().get_permissions()

    def get_serializer_class(self):
        self.serializer_class = UserUploadAvatarSerializer
        return self.serializer_class


class BuildingViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                      mixins.CreateModelMixin, viewsets.GenericViewSet):

    """
    ViewSet для работы с моделью 'Building'
    """
    parser_classes = (MultiPartParser,)
    serializer_class = BuildingSerializer
    queryset = Building.objects.all()

    def get_queryset(self):
        return Building.objects.all()

    def get_permissions(self):
        self.permission_classes = (IsAuthenticated, IsManager)
        return super().get_permissions()

    def get_serializer_class(self):
        self.serializer_class = BuildingSerializer
        return self.serializer_class


class ApartmentViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                       mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    """
    ViewSet для работы с моделью 'Apartment'
    """

    serializer_class = ApartmentSerializer
    queryset = Apartment.objects.all()

    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = request.data

        """
        Получение данных полей из таблицы Building
        SQL запрос: SELECT * FROM "academ_building" WHERE "academ_building"."id" = building.id
        """
        field_values = get_table_fields_by_id(data['building'], Building)

        if data['floor'] > field_values['floors'] or data['section'] > field_values['sections'] \
                or data['type'] > field_values['types']:
            print(f"FLOOR FIELD {data['floor']} > {field_values['floors']} "
                  f"or {data['type']} > {field_values['types']}:")
            return Response(serializer.errors, status=422)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        data = request.data

        """
        Получение данных полей из таблицы Building
        SQL запрос: SELECT * FROM "academ_building" WHERE "academ_building"."id" = building.id
        """
        field_values = get_table_fields_by_id(instance.building.id, Building)

        for i in data:
            if str(i) + 's' in field_values:
                #  Если значение поля 'field_values' - 'integer', тогда проверяем,
                #  что оно больше соответсвующего значения в 'data'
                if isinstance(field_values[str(i) + 's'], int) and data[str(i)] > field_values[str(i) + 's']:
                    return HttpResponse(f'{i} > {field_values[str(i) + "s"]}!', status=422)

                #  Если значение поля 'field_values' - 'string', тогда проверяем,
                #  что оно содержит соответсвующее значение в 'data'
                elif isinstance(field_values[str(i) + 's'], str) and data[str(i)] not in field_values[str(i) + 's']:
                    return HttpResponse(f'{i} > {field_values[str(i) + "s"]}!', status=422)
                else:
                    print(f'{i} is in field_values and its value is alright!')
            else:
                print(f"{str(i)} is not in field_values")

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def get_queryset(self):
        return Apartment.objects.all()

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = ()
        else:
            self.permission_classes = (IsAuthenticated, IsManager)
        return super().get_permissions()

    def get_serializer_class(self):
        self.serializer_class = ApartmentSerializer
        return self.serializer_class


class AppointmentViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                         mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    """
    ViewSet для работы с моделью 'Appointment'
    """

    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        data['manager'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        return Appointment.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_superuser or instance.manager == self.request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def get_permissions(self):
        if self.action == 'update':
            self.permission_classes = (IsAuthenticated, IsAdmin)
        elif self.action == 'partial_update':
            self.permission_classes = (IsAuthenticated, IsAdmin)
        else:
            self.permission_classes = (IsAuthenticated, IsManager)

        return super().get_permissions()

    def get_serializer_class(self):
        self.serializer_class = AppointmentSerializer
        return self.serializer_class


class SupportTicketViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                           mixins.CreateModelMixin, viewsets.GenericViewSet):

    """
    ViewSet для работы с моделью 'SupportTicket'
    """

    serializer_class = SupportTicketSerializer
    queryset = SupportTicket.objects.all()

    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        data = request.data
        if request.user.is_authenticated:
            data['user'] = request.user.id
        else:
            data['user'] = ""

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        return SupportTicket.objects.filter(user=self.request.user.id)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = ()
        else:
            self.permission_classes = (IsAuthenticated, )

        return super().get_permissions()

    def get_serializer_class(self):
        self.serializer_class = SupportTicketSerializer
        return self.serializer_class


class FixatedClientViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                           mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    """
    ViewSet для работы с моделью 'FixatedClient'
    """

    serializer_class = FixatedClientSerializer
    queryset = FixatedClient.objects.all()

    def get_queryset(self):
        return FixatedClient.objects.all()

    def get_permissions(self):
        self.permission_classes = (IsAuthenticated, IsManager)
        return super().get_permissions()

    def get_serializer_class(self):
        self.serializer_class = FixatedClientSerializer
        return self.serializer_class


class ReservationViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                         mixins.CreateModelMixin, viewsets.GenericViewSet):

    """
    ViewSet для работы с моделью 'Reservation'
    """

    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    def get_queryset(self):
        return Reservation.objects.all()

    def get_permissions(self):
        self.permission_classes = (IsAuthenticated, IsManager)
        return super().get_permissions()

    def get_serializer_class(self):
        self.serializer_class = ReservationSerializer
        return self.serializer_class


class FavoritesViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                       mixins.CreateModelMixin, viewsets.GenericViewSet):

    """
    ViewSet для работы с моделью 'Favorite'
    """

    serializer_class = FavoritesSerializer
    queryset = Favorite.objects.all()

    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user.id)

    def get_permissions(self):
        self.permission_classes = (IsAuthenticated, )
        return super().get_permissions()

    def get_serializer_class(self):
        self.serializer_class = FavoritesSerializer
        return self.serializer_class


class ImageGalleryViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                          mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet для работы с моделью 'ImageGallery'
    """

    parser_classes = (MultiPartParser, )
    serializer_class = ImageGallerySerializer
    queryset = ImageGallery.objects.all()

    def get_permissions(self):
        self.permission_classes = ()
        return super().get_permissions()

    def get_serializer_class(self):
        self.serializer_class = ImageGallerySerializer
        return self.serializer_class
