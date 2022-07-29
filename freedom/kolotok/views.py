from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.views.generic import TemplateView

from .models import *
from rest_framework import generics, status, views, viewsets, mixins
from rest_framework.decorators import action

from rest_framework.parsers import JSONParser
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from freedom.permissions import *


class ProductViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                     mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = ProductSerializer
    queryset = []

    def get_permissions(self):
        self.permission_classes = [IsManager]
        return super().get_permissions()

    def get_queryset(self):
        if self.action == 'coverings':
            category_id = Category.objects.get(name='Напольные покрытия')
            subcategory = SubCategory.objects.filter(category=category_id)
            if subcategory:
                self.queryset = Product.objects.filter(sub_category__in=subcategory).distinct()
            return self.queryset
        elif self.action == 'doors':
            category_id = Category.objects.get(name='Двери и арки')
            subcategory = SubCategory.objects.filter(category=category_id)
            if subcategory:
                self.queryset = Product.objects.filter(sub_category__in=subcategory).distinct()
            return self.queryset
        elif self.action == 'tile':
            category_id = Category.objects.get(name='Плитка')
            subcategory = SubCategory.objects.filter(category=category_id)
            if subcategory:
                self.queryset = Product.objects.filter(sub_category__in=subcategory.id).distinct()
            return self.queryset
        elif self.action == 'lighting':
            category_id = Category.objects.get(name='Освещения')
            subcategory = SubCategory.objects.filter(category=category_id)
            if subcategory:
                self.queryset = Product.objects.filter(sub_category__in=subcategory.id).distinct()
            return self.queryset
        elif self.action == 'wall_decor':
            category_id = Category.objects.get(name='Декор стен')
            subcategory = SubCategory.objects.filter(category=category_id)
            if subcategory:
                self.queryset = Product.objects.filter(sub_category__in=subcategory.id).distinct()
            return self.queryset
        elif self.action == 'plumbing':
            category_id = Category.objects.get(name='Сантехника')
            subcategory = SubCategory.objects.filter(category=category_id)
            if subcategory:
                self.queryset = Product.objects.filter(sub_category__in=subcategory.id).distinct()
            return self.queryset
        elif self.action == 'furniture':
            category_id = Category.objects.get(name='Мебель')
            subcategory = SubCategory.objects.filter(category=category_id)
            if subcategory:
                self.queryset = Product.objects.filter(sub_category__in=subcategory.id).distinct()
            return self.queryset
        elif self.action == 'garden':
            category_id = Category.objects.get(name='Садовые конструкции')
            subcategory = SubCategory.objects.filter(category=category_id)
            if subcategory:
                self.queryset = Product.objects.filter(sub_category__in=subcategory.id).distinct()
            return self.queryset

        self.queryset = Product.objects.all()
        return self.queryset

    def get_serializer_class(self):
        if self.action == 'tile':
            return TileSerializer
        elif self.action == 'coverings':
            return FloorCoveringsSerializer
        elif self.action == 'lighting':
            return LightingSerializer
        elif self.action == 'doors':
            return DoorsSerializer
        elif self.action == 'furniture':
            return FurnitureSerializer
        elif self.action == 'plumbing':
            return PlumbingSerializer
        elif self.action == 'garden':
            return GardenConstructionSerializer
        elif self.action == 'wall_decor':
            return WallDecorSerializer

        return self.serializer_class

    @action(["get", "post"], detail=False)
    def tile(self, request, *args, **kwargs):
        """
        Плитка
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        if request.method == "GET":
            return self.list(request, *args, **kwargs)
        elif request.method == "POST":
            return self.create(request, *args, **kwargs)

    @action(["get", "post"], detail=False)
    def coverings(self, request, *args, **kwargs):
        """
        Напольные покрытия
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        if request.method == "GET":
            return self.list(request, *args, **kwargs)
        elif request.method == "POST":
            return self.create(request, *args, **kwargs)

    @action(["get", "post"], detail=False)
    def doors(self, request, *args, **kwargs):
        """
        Двери
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        if request.method == "GET":
            return self.list(request, *args, **kwargs)
        elif request.method == "POST":
            return self.create(request, *args, **kwargs)

    @action(["get", "post"], detail=False)
    def lighting(self, request, *args, **kwargs):
        """
        Освещение
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        if request.method == "GET":
            return self.list(request, *args, **kwargs)
        elif request.method == "POST":
            return self.create(request, *args, **kwargs)

    @action(["get", "post"], detail=False)
    def furniture(self, request, *args, **kwargs):
        """
        Фурнитура
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        if request.method == "GET":
            return self.list(request, *args, **kwargs)
        elif request.method == "POST":
            return self.create(request, *args, **kwargs)

    @action(["get", "post"], detail=False)
    def plumbing(self, request, *args, **kwargs):
        """
        plumbing
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        if request.method == "GET":
            return self.list(request, *args, **kwargs)
        elif request.method == "POST":
            return self.create(request, *args, **kwargs)

    @action(["get", "post"], detail=False)
    def garden(self, request, *args, **kwargs):
        """
        plumbing
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        if request.method == "GET":
            return self.list(request, *args, **kwargs)
        elif request.method == "POST":
            return self.create(request, *args, **kwargs)

    @action(["get", "post"], detail=False)
    def wall_decor(self, request, *args, **kwargs):
        """
        plumbing
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        if request.method == "GET":
            return self.list(request, *args, **kwargs)
        elif request.method == "POST":
            return self.create(request, *args, **kwargs)


class SubCategoryViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()

    def get_permissions(self):
        self.permission_classes = [IsManager]
        return super().get_permissions()

    def get_serializer_class(self):
        self.serializer_class = SubCategorySerializer
        return self.serializer_class


class CategoryViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        self.permission_classes = [IsManager]
        return super().get_permissions()

    def get_serializer_class(self):
        self.serializer_class = CategorySerializer
        return self.serializer_class
