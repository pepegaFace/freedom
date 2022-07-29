from django.core.management.base import BaseCommand
from kolotok.models import *
import json
import os


class Command(BaseCommand):
    """
    Наполняет базу магазина категориями, под-ктегориями и товароми
    """
    def handle(self, *args, **options):
        categories = {'Напольные покрытия': 'Ламинат', 'Двери и арки': 'Входные двери', 'Плитка': 'Керамическая плитка',
                      'Освещения': 'Люстры', 'Декор стен': 'Виниловые обои', 'Сентехника': 'Вынны',
                      'Мебель': 'Кровати', 'Садовые конструкции': 'Статуэтки'}

        for category, sub_category in categories.items():
            categor = Category(name=category)
            categor.save()

            sub_categor = SubCategory(name=sub_category, category=Category.objects.get(name=category))
            sub_categor.save()

        filepath = os.path.abspath(os.path.dirname(__file__))

        json_data = open(f'{filepath}/product_data.json')
        product_list = json.load(json_data)

        min_id_sub_category = SubCategory.objects.get(name='Ламинат').id
        for element in product_list:
            product = Product(**element)
            product.save()
            product.sub_category.add(SubCategory.objects.get(id=min_id_sub_category))
            product.save()

            min_id_sub_category += 1