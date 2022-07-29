from django.core.management.base import BaseCommand
from academ.models import Apartment, Building, ImageGallery
import json
import os
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


def check_apartment(building):
    """
    Проверка на наличие квартир в базе.
    Если квартиры имеются - возвращаем 1, иначе 0
    @param building: дом
    @return: 0, 1
    """
    try:
        apartments = Apartment.objects.filter(building=building).first()
        if apartments:
            print(Apartment.objects.filter(building=building).first())
            return 1
        else:
            print('No apartments found...')
    except Apartment.DoesNotExist:
        print('No apartments found...')
        return 0


def last_floor_apartments_generator(apartment_data, building):
    apartment_instance = Apartment.objects.filter(number=apartment_data['number'],)

    if apartment_instance:
        print(f"Apartment with number: '{apartment_data['number']}' already exists!")
        pass
    else:
        print(f"Generating apartment with number: '{apartment_data['number']}'...")
        apartment = Apartment(building=building,
                              floor=14,
                              area=apartment_data['area'],
                              number=apartment_data['number'],
                              section=apartment_data['section'],
                              type=apartment_data['apartment_type'])
        apartment.save()


def apartment_generator(params, building):
    """
    Функция, генерирующая квартиры и записывающая их в базу данных на основе набора параметров.
    @param params: набор параметров
    @param building: дом
    """
    number = params['number']

    if params['section'] != 3:
        start = 4
    else:
        start = 2

    for i in range(start, building.floors):
        if i != start:
            number += params['delta']

        apartment_instance = Apartment.objects.filter(number=number)

        if apartment_instance:
            print(f"Apartment with number: '{number}' already exists!")
            pass
        else:
            print(f"Generating apartment with number: '{number}'...")
            apartment = Apartment(building=building, floor=i, area=params['area'],
                                  number=number, section=params['section'], type=params['apartment_type'])
            apartment.save()


def gallery_generator(building):
    gallery_instance = ImageGallery.objects.filter(building=building).first()
    if gallery_instance:
        print(ImageGallery.objects.filter(building=building).first(), ' already exist!')
        return
    else:
        filepath = f'{settings.MEDIA_ROOT}/pictures/building.jpg'
        uploaded_image = SimpleUploadedFile(content=open(filepath, 'rb').read(),
                                            content_type="image/jpg",
                                            name='image.jpg')
        instance = ImageGallery(building=building, image=uploaded_image)
        instance.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        address = 'Academ'
        try:
            building = Building.objects.get(address=address)
        except Building.DoesNotExist:
            building = Building(address=address, floors=14, sections=3)
            building.save()

        # if check_apartment(building):
        #     return

        filepath = os.path.abspath(os.path.dirname(__file__))

        json_data = open(f'{filepath}/apartment_data.json')
        json_data_last_floor = open(f'{filepath}/last_floor_data.json')
        params_list = json.load(json_data)
        params_list_last_floor = json.load(json_data_last_floor)

        print('\nGenerating apartments up to 14th floor...\n')
        for element in params_list:
            apartment_generator(element, building)

        print('\nGenerating 14th floor apartments...\n')
        for element_last_floor in params_list_last_floor:
            last_floor_apartments_generator(element_last_floor, building)

        print('\nGenerating gallery instances...\n')
        gallery_generator(building)
