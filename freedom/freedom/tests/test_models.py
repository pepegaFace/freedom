from django.test import TestCase, Client
from rest_framework.test import APITestCase
from django.http import HttpResponse, JsonResponse
from pathlib import Path
from dotenv import load_dotenv
from freedom.settings import PROJECT_ROOT
from academ.models import *
from kolotok.models import *
from freedom.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, force_authenticate
import os

load_dotenv(f'{Path(PROJECT_ROOT).parent}/.env.dev')


class TestModels(APITestCase):
    """Счетчики под задаваемые в функции setUp объекты в базе"""

    number_of_buildings = 0
    number_of_apartments = 0

    def test_create_buildings_apartments(self):
        """
        Filling testing database with buildings, apartments
        """
        print('\nTESTING MODELS\n')
        self.building_academ = Building.objects.create(
            address='Академический',
            floors=14,
            sections=3,
            types=5
        )
        self.building_academ.save()
        self.number_of_buildings += 1

        self.building = Building.objects.create(
            address='Testing',
            floors=14,
            sections=3,
            types=5
        )
        self.building.save()
        self.number_of_buildings += 1

        self.apartment = Apartment.objects.create(
            number=1,
            floor=1,
            section=1,
            type=3,
            area=71.05,
            cost=3000000,
            reserved=False,
            building=Building.objects.get(address='Академический')
        )
        self.apartment.save()
        self.number_of_apartments += 1

        self.assertEqual(self.apartment.building, self.building_academ)
