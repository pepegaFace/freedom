from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer для работы с категориями.
    """
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Serializer для работы с саб-категориями.
    """
    class Meta:
        model = SubCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer для работы с Товарами.
    """
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer для работы с категориями.
    """
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Serializer для работы с под-категориями.
    """
    class Meta:
        model = SubCategory
        fields = '__all__'


class FloorCoveringsSerializer(serializers.ModelSerializer):
    """
    Serializer для работы с напольными покрытиями.
    """
    class Meta:
        model = Product
        fields = ('id', 'sub_category', 'name', 'article', 'brand', 'size', 'product_class', 'fire_class', 'price')


class DoorsSerializer(serializers.ModelSerializer):
    """
    Serializer для работы с Дверьми.
    """
    class Meta:
        model = Product
        fields = ('id', 'sub_category', 'name', 'series', 'loops', 'locks', 'material', 'blade_thickness', 'color',
                  'price')


class TileSerializer(serializers.ModelSerializer):
    """
    Serializer для работы с Плиткой.
    """
    class Meta:
        model = Product
        fields = ('id', 'sub_category', 'name', 'series', 'brand', 'article', 'size', 'purpose_of_goods', 'color',
                  'price')


class LightingSerializer(serializers.ModelSerializer):
    """
    Serializer для работы с Освещением.
    """
    class Meta:
        model = Product
        fields = ('id', 'sub_category', 'name', 'supplier', 'article', 'brand', 'collection', 'style', 'color',
                  'base_type', 'count_lamp', 'max_lamp_power', 'height', 'diameter', 'descriptions', 'price')


class WallDecorSerializer(serializers.ModelSerializer):
    """
    Serializer для работы с Декор стен.
    """
    class Meta:
        model = Product
        fields = ('id', 'sub_category', 'name', 'article', 'series', 'product_class', 'docking_method', 'size',
                  'drawing', 'descriptions', 'price')


class PlumbingSerializer(serializers.ModelSerializer):
    """
    Serializer для работы с Сантехникой.
    """
    class Meta:
        model = Product
        fields = ('id', 'sub_category', 'name', 'supplier', 'article', 'brand', 'color', 'size', 'material',
                  'power', 'descriptions', 'price', 'package')


class FurnitureSerializer(serializers.ModelSerializer):
    """
    Serializer для работы с Мебелью.
    """
    class Meta:
        model = Product
        fields = ('id', 'sub_category', 'name', 'article', 'brand', 'series', 'size', 'descriptions', 'price')


class GardenConstructionSerializer(serializers.ModelSerializer):
    """
    Serializer для работы с Садовыми конструкциями.
    """
    class Meta:
        model = Product
        fields = ('id', 'sub_category', 'name', 'voltage', 'size', 'descriptions', 'price')