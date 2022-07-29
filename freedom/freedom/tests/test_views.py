from django.test import TestCase, Client
from rest_framework.test import APITestCase
from django.http import HttpResponse, JsonResponse
from pathlib import Path
from dotenv import load_dotenv
from freedom.settings import PROJECT_ROOT
from academ.models import *
from kolotok.models import *
from freedom.models import *
from datetime import datetime
import json
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, force_authenticate
import os
import logging

logger = logging.getLogger('django')

load_dotenv(f'{Path(PROJECT_ROOT).parent}/.env.dev')


class Test01ViewAccess(APITestCase):

    """Счетчики под задаваемые в функции setUp объекты в базе"""
    number_of_users = 0
    number_of_categories = 0
    number_of_subcategories = 0
    number_of_tickets = 0
    number_of_buildings = 0
    number_of_apartments = 0
    number_of_appointments = 0
    number_of_supportTickets = 0

    logs = []
    print('\nTESTING VIEWS\n')

    def setUp(self):
        """
        Filling testing database with data
        """
        self.user = User.objects.create_user(
            email='user@user.user',
            username='user',
            password='q1726354',
            role='DefaultUser'
        )
        self.user.save()
        self.number_of_users += 1

        self.manager = User.objects.create_user(
            email='manager@user.user',
            username='manager',
            password='q1726354',
            role='Manager'
        )
        self.manager.save()
        self.number_of_users += 1

        self.admincrm = User.objects.create_user(
            email='admincrm@user.user',
            username='admincrm',
            password='q1726354',
            role='AdminCRM'
        )
        self.admincrm.save()
        self.number_of_users += 1

        self.admin = User.objects.create_superuser(
            email='admin@admin.admin',
            username='admin',
            password='q1726354',
        )
        self.admin.save()
        self.number_of_users += 1

        self.building = Building.objects.create(
            address='Academ',
            floors=14,
            sections=3,
            types=5
        )
        self.building.save()
        self.number_of_buildings += 1

        self.building_1 = Building.objects.create(
            address='Another building',
            floors=14,
            sections=3,
            types=5
        )
        self.building_1.save()
        self.number_of_buildings += 1

        self.testing_category = Category.objects.create(
            name='Testing category'
        )
        self.testing_category.save()
        self.number_of_categories += 1

        self.testing_subcategory = SubCategory.objects.create(
            name='Testing subcategory',
            category=self.testing_category
        )
        self.testing_category.save()
        self.number_of_subcategories += 1

        self.testing_ticket = Ticket.objects.create(
            name="NewUser",
            email="NewUser@example.com",
            phone_number="+999999999",
            address="Testing address",
            house_type=1,
            condition_type=1,
            apartment_floor=1,
            house_floors=1,
            rooms=1,
            adjoining_rooms=False,
            area=12,
            living_area=10,
            kitchen_area=2
        )
        self.testing_ticket.save()
        self.number_of_tickets += 1

        self.apartment = Apartment.objects.create(
            number=1,
            floor=1,
            section=1,
            type=2,
            area=71.05,
            cost=3000000,
            reserved=False,
            building=Building.objects.get(address='Academ')
        )
        self.apartment.save()
        self.number_of_apartments += 1

        self.logs.append({'Test': 'SetUp',
                          'Result': True})
        #
        # self.assertEqual(self.apartment.building, self.building)

    def test01_permissions(self):
        """Test permissions on different users"""

        time_started = datetime.now()
        """Admin"""
        self.client.force_authenticate(self.admin)
        response = self.client.get("/auth/users/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 1)

        response = self.client.get("/auth/users/me/", follow=True)
        self.assertEqual(response.data['username'], 'admin')

        response = self.client.get("/kolotok/categories", follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/freedom/tickets", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['address'], 'Testing address')
        self.client.logout()

        """User"""
        self.client.force_authenticate(self.user)
        response = self.client.get("/auth/users/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        response = self.client.get("/auth/users/me/", follow=True)
        self.assertEqual(response.data['username'], 'user')

        response = self.client.get("/kolotok/categories", follow=True)
        self.assertEqual(response.status_code, 403)

        response = self.client.get("/freedom/tickets", follow=True)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        """Manager"""
        self.client.force_authenticate(self.manager)
        response = self.client.get("/auth/users/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        response = self.client.get("/auth/users/me/", follow=True)
        self.assertEqual(response.data['username'], 'manager')

        response = self.client.get("/kolotok/categories", follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/freedom/tickets", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['address'], 'Testing address')
        self.client.logout()

        """Admin CRM"""
        self.client.force_authenticate(self.admincrm)
        response = self.client.get("/auth/users/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        response = self.client.get("/auth/users/me/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'admincrm')

        response = self.client.get("/kolotok/categories", follow=True)
        self.assertEqual(response.status_code, 403)

        response = self.client.get("/freedom/tickets", follow=True)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        time_finished = datetime.now()

        logger.info(f"'Test': 'test01_permissions', 'Result': True, 'Started_at': {time_started}, "
                    f"'Finished_at': {time_finished}',"
                    f"'Delta: {time_finished - time_started}'")

    def test02_admin_page(self):
        """The admin page loads properly"""

        time_started = datetime.now()

        response = self.client.get("/admin", follow=True)
        self.assertEqual(response.status_code, 200)

        time_finished = datetime.now()

        logger.info(f"'Test': 'test02_admin_page', 'Result': True, 'Started_at': {time_started}, "
                    f"'Finished_at': {time_finished}',"
                    f"'Delta: {time_finished - time_started}'")

    def test03_swagger_page(self):
        """The swagger page loads properly"""
        time_started = datetime.now()

        response = self.client.get("/swagger", follow=True)
        self.assertEqual(response.status_code, 200)

        time_finished = datetime.now()

        logger.info(f"'Test': 'test03_swagger_page', 'Result': True, 'Started_at': {time_started}, "
                    f"'Finished_at': {time_finished}',"
                    f"'Delta: {time_finished - time_started}'")

    def test04_user_views_admin(self):
        """Testing user views as Admin"""

        time_started = datetime.now()

        """Login as admin"""
        self.client.force_authenticate(self.admin)
        response = self.client.get("/auth/users/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) != 1)
        # print(response.data)

        """Check superuser status"""
        response = self.client.get("/auth/users/me/", follow=True)
        self.assertEqual(response.data['is_superuser'], True)

        """Add user"""
        data = {
            'username': 'username',
            'email': 'email@mail.ru',
            'password': 'q12w34e56'
        }

        response = self.client.post(f"/auth/users/", data)
        self.assertEqual(response.status_code, 201)
        user_data = response.data

        """Change user data with PUT method"""
        changed_data = {
            'email': 'email1@mail.ru',
        }

        response = self.client.put(f"/auth/users/{user_data['id']}/", changed_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['email'] != data['email'])
        self.assertEqual(response.data['username'], data['username'])

        """Change user data with PATCH method"""
        # changed_data = {
        #     'email': 'email2@mail.ru',
        # }

        response = self.client.patch(f"/auth/users/{user_data['id']}/",
                                     {'email': 'email2@mail.ru'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['email'] != data['email'])
        self.assertTrue(response.data['email'] != changed_data['email'])
        self.assertEqual(response.data['username'], data['username'])

        """Get user by id and compare"""
        response = self.client.get(f"/auth/users/{user_data['id']}/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], user_data['username'])

        """Remove user by id"""
        response = self.client.delete(f"/auth/users/{user_data['id']}/")
        self.assertEqual(response.status_code, 204)

        time_finished = datetime.now()

        logger.info(f"'Test': 'test04_user_views_admin', 'Result': True, 'Started_at': {time_started}, "
                    f"'Finished_at': {time_finished}',"
                    f"'Delta: {time_finished - time_started}'")

    def test05_user_views_default_user(self):
        """Testing user views as default user"""

        time_started = datetime.now()

        """Login as default user"""
        self.client.force_authenticate(self.user)

        """Get users info"""
        response = self.client.get("/auth/users/", follow=True)
        self.assertEqual(response.data[0]['email'], 'user@user.user')
        self.assertEqual(len(response.data), 1)
        my_id = response.data[0]['id']

        """Get users/me info"""
        response = self.client.get("/auth/users/me", follow=True)
        self.assertEqual(response.data['email'], 'user@user.user')

        """Get user by id and compare"""
        response = self.client.get(f"/auth/users/{my_id + 1}/", follow=True)
        self.assertEqual(response.status_code, 404)

        """Remove user by id"""
        response = self.client.delete(f"/auth/users/{my_id + 1}/")
        self.assertEqual(response.status_code, 403)

        time_finished = datetime.now()

        logger.info(f"'Test': 'test05_user_views_default_user', 'Result': True, 'Started_at': {time_started}, "
                    f"'Finished_at': {time_finished}',"
                    f"'Delta: {time_finished - time_started}'")

    def test06_categories_views_manager(self):
        """Testing categories views as manager"""

        time_started = datetime.now()

        """Login as manager"""
        self.client.force_authenticate(self.manager)

        """Get users info"""
        response = self.client.get("/auth/users/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['email'], 'manager@user.user')
        self.assertEqual(len(response.data), 1)

        """Get categories"""
        response = self.client.get("/kolotok/categories/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Testing category')
        self.assertEqual(len(response.data), self.number_of_categories)

        """Add new categories via POST method"""
        iterations = 3

        for i in range(0, iterations):
            response = self.client.post("/kolotok/categories/",
                                        data={'name': f'Category {i + 1}'},
                                        follow=True)
            self.assertEqual(response.status_code, 201)

        added_categories = \
            self.client.get("/kolotok/categories/", follow=True).data[self.number_of_categories:]

        self.assertEqual(len(added_categories), 3)

        """Change categories via PUT method"""
        response = self.client.put(f"/kolotok/categories/{added_categories[0]['id']}/",
                                   data={'name': f'Category 1 changed'},
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['name'] != 'Category 1')
        self.assertEqual(response.data['name'], 'Category 1 changed')

        """Change categories via PATCH method"""
        response = self.client.patch(f"/kolotok/categories/{added_categories[0]['id']}/",
                                     data={'name': f'Category 1 unchanged'},
                                     follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['name'] != 'Category 1 changed')
        self.assertEqual(response.data['name'], 'Category 1 unchanged')

        """Delete category object"""
        response = self.client.delete(f"/kolotok/categories/{added_categories[0]['id']}/",
                                      follow=True)
        self.assertEqual(response.status_code, 204)

        """Check if category was deleted via GET method"""
        response = self.client.get(f"/kolotok/categories/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), self.number_of_categories + len(added_categories) - 1)

        time_finished = datetime.now()

        logger.info(f"'Test': 'test06_categories_views_manager', 'Result': True, 'Started_at': {time_started}, "
                    f"'Finished_at': {time_finished}',"
                    f"'Delta: {time_finished - time_started}'")

    def test07_subcategories_views_manager(self):
        """Testing categories views as manager"""

        time_started = datetime.now()

        """Login as manager"""
        self.client.force_authenticate(self.manager)

        """Get subcategories"""
        response = self.client.get("/kolotok/sub_categories/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Testing subcategory')
        self.assertEqual(len(response.data), 1)

        """Add new subcategories via POST method"""
        iterations = 3

        for i in range(0, iterations):
            response = self.client.post("/kolotok/sub_categories/",
                                        data={'name': f'Subcategory {i + 1}'},
                                        follow=True)
            self.assertEqual(response.status_code, 400)

            response = self.client.post("/kolotok/sub_categories/",
                                        data={
                                              "name": f'Subcategory {i + 1}',
                                              "category": Category.objects.all()[0].id
                                            },
                                        follow=True)
            self.assertEqual(response.status_code, 201)

        added_subcategories = \
            self.client.get("/kolotok/sub_categories/",
                            follow=True).data[self.number_of_subcategories:]

        self.assertEqual(len(added_subcategories), 3)

        """Change subcategories via PUT method"""
        response = self.client.put(f"/kolotok/sub_categories/{added_subcategories[0]['id']}/",
                                   data={'name': f'Subcategory 1 changed'},
                                   follow=True)
        self.assertEqual(response.status_code, 400)

        response = self.client.put(f"/kolotok/sub_categories/{added_subcategories[0]['id']}/",
                                   data={'name': f'Subcategory 1 changed',
                                         "category": Category.objects.all()[0].id
                                         },
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['name'] != 'Subcategory 1')
        self.assertEqual(response.data['name'], 'Subcategory 1 changed')

        """Change subcategories via PATCH method"""
        response = self.client.patch(f"/kolotok/sub_categories/{added_subcategories[0]['id']}/",
                                     data={'name': f'Subcategory 1 unchanged'},
                                     follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['name'] != 'Subcategory 1 changed')
        self.assertEqual(response.data['name'], 'Subcategory 1 unchanged')

        """Delete category object"""
        response = self.client.delete(f"/kolotok/sub_categories/{added_subcategories[0]['id']}/",
                                      follow=True)
        self.assertEqual(response.status_code, 204)

        """Check if category was deleted via GET method"""
        response = self.client.get(f"/kolotok/sub_categories/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), self.number_of_subcategories + len(added_subcategories) - 1)

        time_finished = datetime.now()

        logger.info(f"'Test': 'test07_subcategories_views_manager', 'Result': True, 'Started_at': {time_started}, "
                    f"'Finished_at': {time_finished}',"
                    f"'Delta: {time_finished - time_started}'")

    def test08_tickets_manager(self):
        """Testing tickets views as manager"""

        time_started = datetime.now()

        """Login as manager"""
        self.client.force_authenticate(self.manager)

        """Get tickets"""
        response = self.client.get("/freedom/tickets/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'NewUser')
        self.assertEqual(response.data[0]['address'], 'Testing address')
        self.assertEqual(len(response.data), self.number_of_tickets)

        """Add new tickets via POST method"""
        """Bad POST request"""
        response = self.client.post("/freedom/tickets/",
                                    data={
                                        "name": f"",
                                        "email": f"email",
                                        "phone_number": f"+bad_phone",
                                        "address": f"",
                                        "house_type": -1,
                                        "condition_type": -1,
                                        "apartment_floor": -1,
                                        "house_floors": -1,
                                        "rooms": -1,
                                        "adjoining_rooms": 'SOME DATA',
                                        "area": -10,
                                        "living_area": 10 - 3 - 5000.0005,
                                        "kitchen_area": 3 - 5000.0005
                                    },
                                    follow=True)

        self.assertEqual(response.data['name'][0], 'This field may not be blank.')
        self.assertEqual(response.data['email'][0], 'Enter a valid email address.')
        self.assertEqual(response.data['phone_number'][0], "Phone number must be entered in the format: '+999999999'. "
                                                           "Up to 15 digits allowed.")
        self.assertEqual(response.data['address'][0], 'This field may not be blank.')
        self.assertEqual(response.data['house_type'][0], '"-1" is not a valid choice.')
        self.assertEqual(response.data['condition_type'][0], '"-1" is not a valid choice.')
        self.assertEqual(response.data['apartment_floor'][0], 'Ensure this value is greater than or equal to 0.')
        self.assertEqual(response.data['house_floors'][0], 'Ensure this value is greater than or equal to 0.')
        self.assertEqual(response.data['rooms'][0], '"-1" is not a valid choice.')
        self.assertEqual(response.data['adjoining_rooms'][0], 'Must be a valid boolean.')
        self.assertEqual(response.data['area'][0], 'Value must be positive!')
        self.assertEqual(response.data['living_area'][0], 'Value must be positive!')
        self.assertEqual(response.data['kitchen_area'][0], 'Value must be positive!')

        self.assertEqual(response.status_code, 400)

        iterations = 3

        for i in range(0, iterations):
            """Legit POST request"""
            response = self.client.post("/freedom/tickets/",
                                        data={
                                              "name": f"User {i+1}",
                                              "email": f"User{i+1}@example.com",
                                              "phone_number": f"88005553535",
                                              "address": f"Address {i+1}",
                                              "house_type": 1,
                                              "condition_type": 1,
                                              "apartment_floor": 1,
                                              "house_floors": 1,
                                              "rooms": 1,
                                              "adjoining_rooms": False,
                                              "area": 10*(i+1),
                                              "living_area": 10*(i+1) - 3*(i+1) - float(f'0.2{i}'),
                                              "kitchen_area": 3*(i+1)
                                            },
                                        follow=True)
            self.assertEqual(response.status_code, 201)

        added_data = self.client.get("/freedom/tickets/", follow=True).data[self.number_of_tickets:]

        self.assertEqual(len(added_data), iterations)

        """Get ticket by id"""
        response = self.client.get(f"/freedom/tickets/{added_data[1]['id']}/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], f'User 2')

        """Delete ticket by id"""
        response = self.client.delete(f"/freedom/tickets/{added_data[1]['id']}/", follow=True)
        self.assertEqual(response.status_code, 204)

        """Check if category was deleted via GET method"""
        response = self.client.get(f"/freedom/tickets/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), self.number_of_categories + len(added_data) - 1)
        self.assertEqual(response.data[self.number_of_tickets]['name'], 'User 1')
        self.assertEqual(response.data[self.number_of_tickets]['address'], 'Address 1')

        time_finished = datetime.now()

        logger.info(f"'Test': 'test08_tickets_manager', 'Result': True, 'Started_at': {time_started}, "
                    f"'Finished_at': {time_finished}',"
                    f"'Delta: {time_finished - time_started}'")

    def test09_support_tickets(self):
        """Test support tickets as various users"""

        time_started = datetime.now()

        response = self.client.get(f"/academ/support/", follow=True)
        self.assertEqual(response.status_code, 401)

        response = self.client.post(f"/academ/support/", data={
                                                                "name": "",
                                                                "phone_number": "number",
                                                                "email": "email",
                                                                "topic_type": 0,
                                                                "message": ""
                                                            }, follow=True, format='json')

        self.assertEqual(response.data['name'][0], 'This field may not be blank.')
        self.assertEqual(response.data['phone_number'][0], "Phone number must be entered in the format: '+999999999'. "
                                                           "Up to 15 digits allowed.")
        self.assertEqual(response.data['email'][0], 'Enter a valid email address.')
        self.assertEqual(response.data['topic_type'][0], '"0" is not a valid choice.')

        self.assertEqual(response.status_code, 400)

        time_finished = datetime.now()

        logger.info(f"'Test': 'test09_support_tickets', 'Result': True, 'Started_at': {time_started}, "
                    f"'Finished_at': {time_finished}',"
                    f"'Delta: {time_finished - time_started}'")

    def test10_appointment(self):
        """Test appointment as manager"""

        time_started = datetime.now()

        """Login as manager"""
        self.client.force_authenticate(self.manager)

        """Get appointments"""
        response = self.client.get(f"/academ/appointment/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        """Test POST method"""

        offset = timedelta(days=1)

        """Try POST with bad data"""
        chosen_date = (datetime.today() - offset).strftime('%Y-%m-%d')
        response = self.client.post(f"/academ/appointment/", data={
                                                                  "client": "",
                                                                  "date": chosen_date,
                                                                  "time": "8:00",
                                                                  "manager": 0,
                                                                  "apartment": -1
                                                                }, follow=True, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['client'][0], 'This field may not be blank.')
        self.assertEqual(response.data['date'][0], f"'Chosen date: {chosen_date}' <= 'Current date'!")
        self.assertEqual(response.data['time'][0], f'"8:00" is not a valid choice.')
        # self.assertEqual(response.data['manager'][0], 'Invalid pk "0" - object does not exist.')
        self.assertEqual(response.data['apartment'][0], 'Invalid pk "-1" - object does not exist.')

        """Check if data weren't added"""
        response = self.client.get(f"/academ/appointment/", follow=True)
        self.assertEqual(len(response.data), 0)

        """Try POST"""
        iterations = 3
        for i in range(1, iterations + 1):
            response = self.client.post(f"/academ/appointment/", data={
                "client": f"Client {i}",
                "date": (datetime.today() + offset).strftime('%Y-%m-%d'),
                "phone_number": f'99999999{i}',
                "time": f"1{i}:00",
                "manager": self.manager.id,
                "building": self.building.id,
                "apartment": self.apartment.id
            }, follow=True, format='json')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data['client'], f'Client {i}')

        """Check if data was added"""
        response = self.client.get(f"/academ/appointment/", follow=True)
        self.assertEqual(len(response.data), iterations + self.number_of_appointments)

        """Try GET by id"""
        response = self.client.get(f"/academ/appointment/{self.number_of_appointments + 2}/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['client'], 'Client 2')
        self.assertEqual(response.data['time'], '12:00')

        """Try PUT as manager"""
        response = self.client.put(f"/academ/appointment/{self.number_of_appointments + 2}/",
                                   {
                                       'client': 'Client 2 changed!',
                                       'apartment': self.apartment.id,
                                       'manager': self.manager.id,
                                       'date': (datetime.today() + offset).strftime('%Y-%m-%d'),
                                       'time': '18:00',
                                   }, follow=True)

        self.assertEqual(response.status_code, 403)

        """Try PATCH as manager"""
        response = self.client.patch(f"/academ/appointment/{self.number_of_appointments + 2}/",
                                     {
                                        'client': 'Client 2 patched!!'
                                     }, follow=True)

        self.assertEqual(response.status_code, 403)
        self.client.logout()

        self.client.force_authenticate(self.admin)
        """POST as admin"""
        response = self.client.post(f"/academ/appointment/", data={
            "client": f"Client by admin",
            "date": (datetime.today() + offset).strftime('%Y-%m-%d'),
            "time": f"16:00",
            "phone_number": "799999999",
            "manager": self.admin.id,
            "building": self.building.id,
            "apartment": self.apartment.id
        }, follow=True, format='json')
        self.assertEqual(response.status_code, 201)
        self.number_of_appointments += 1

        """POST as admin, violating unique rule"""
        response = self.client.post(f"/academ/appointment/", data={
            "client": f"Another client by admin",
            "date": (datetime.today() + offset).strftime('%Y-%m-%d'),
            "time": f"16:00",
            "phone_number": "999999999",
            "manager": self.admin.id,
            "building": self.building.id,
            "apartment": self.apartment.id
        }, follow=True, format='json')
        self.assertEqual(str(response.data['non_field_errors'][0]),
                         "The fields date, time, apartment must make a unique set.")
        self.assertEqual(response.status_code, 400)

        """POST as admin, sending apartment that doesnt exist in chosen building"""
        response = self.client.post(f"/academ/appointment/", data={
            "client": f"Another client by admin",
            "date": (datetime.today() + offset).strftime('%Y-%m-%d'),
            "time": f"17:00",
            "phone_number": "799999999",
            "manager": self.admin.id,
            "building": self.building_1.id,
            "apartment": self.apartment.id
        }, follow=True, format='json')
        print(response.data)
        self.assertEqual(str(response.data['apartment'][0]),
                         'Select a valid apartment please')
        self.assertEqual(response.status_code, 400)

        """Try PUT as admin"""
        response = self.client.get('/academ/appointment/', follow=True)
        self.assertEqual(len(response.data), iterations + self.number_of_appointments)
        self.assertEqual(response.data[iterations + self.number_of_appointments - 1]['client'], 'Client by admin')

        response = self.client.put(f"/academ/appointment/{self.number_of_appointments + 2}/",
                                   {
                                       'client': 'Client 2 changed!',
                                       "phone_number": "779999999",
                                       'date': (datetime.today() + offset + offset).strftime('%Y-%m-%d'),
                                       "building": self.building.id,
                                       'apartment': self.apartment.id,
                                       'manager': self.manager.id
                                   }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['client'], 'Client 2 changed!')
        self.assertTrue(response.data['phone_number'] != 999999992)
        self.assertEqual(response.data['date'], (datetime.today() + offset + offset).strftime('%Y-%m-%d'))
        self.assertEqual(response.data['time'], '9:00')
        self.assertEqual(response.data['apartment'], self.apartment.id)
        self.assertEqual(response.data['manager'], self.manager.id)

        """Try PATCH as admin"""
        self.client.force_authenticate(self.admin)
        response = self.client.patch(f"/academ/appointment/{self.number_of_appointments + 2}/",
                                     {
                                         'client': 'Client 2 patched!!'
                                     }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['client'], 'Client 2 patched!!')
        self.assertEqual(response.data['time'], '9:00')
        self.client.logout()

        self.client.force_authenticate(self.manager)

        """Try DELETE other user's appointment"""
        response = self.client.delete(f"/academ/appointment/"
                                      f"{iterations + self.number_of_appointments}/")
        self.assertEqual(response.status_code, 403)

        """Check if object was not deleted"""
        response = self.client.get(f"/academ/appointment/{iterations + self.number_of_appointments}/")
        self.assertEqual(response.data['client'], 'Client by admin')

        """Try DELETE manager's appointment"""
        deleted_items = 0

        response = self.client.delete(f"/academ/appointment/{self.number_of_appointments + 2}/")
        self.assertEqual(response.status_code, 204)
        deleted_items += 1

        """Check if object was deleted"""
        response = self.client.get(f"/academ/appointment/{self.number_of_appointments + 2}/", follow=True)
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"/academ/appointment/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), iterations + self.number_of_appointments - deleted_items)

        self.client.logout()

        time_finished = datetime.now()

        logger.info(f"'Test': 'test10_appointment', 'Result': True, 'Started_at': {time_started}, "
                    f"'Finished_at': {time_finished}',"
                    f"'Delta: {time_finished - time_started}'")

    def test11_apartments(self):
        """Test apartments as manager"""

        time_started = datetime.now()

        """Login as admin"""
        self.client.force_authenticate(self.admin)

        response = self.client.get(f"/academ/building/", follow=True)
        self.assertEqual(response.status_code, 200)

        time_finished = datetime.now()

        logger.info(f"'Test': 'test11_apartments', 'Result': True, 'Started_at': {time_started}, "
                    f"'Finished_at': {time_finished}',"
                    f"'Delta: {time_finished - time_started}'")

    """SLAVA"""

    def test12_product_views(self):

        self.client.force_authenticate(self.manager)

        # Создаю категории
        categories = ['Напольные покрытия', 'Двери и арки', 'Плитка',
                      'Освещения', 'Декор стен', 'Сантехника',
                      'Мебель', 'Садовые конструкции']

        for category in categories:
            self.client.post("/kolotok/categories/", data={'name': f'{category}'}, follow=True)

        """
        Testing product method get
        """

        # Get запросы по всем продуктам
        response = self.client.get("/kolotok/products/coverings/", follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/kolotok/products/doors/", follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/kolotok/products/furniture/", follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/kolotok/products/garden/", follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/kolotok/products/lighting/", follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/kolotok/products/plumbing/", follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/kolotok/products/tile/", follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/kolotok/products/wall_decor/", follow=True)
        self.assertEqual(response.status_code, 200)

        """
        Testing product method post
        """

        # Создаю продукт и произвожу проверку
        response = self.client.get("/kolotok/products/")
        count_product = len(response.data)

        response = self.client.post("/kolotok/products/", data={
                                                                "name": "string",
                                                                "price": 14567,
                                                                "article": "string",
                                                                "brand": "string",
                                                                "diameter": 367770,
                                                                "sub_category": [
                                                                    SubCategory.objects.all()[0].id
                                                                ]
                                                            }, follow=True, format='json')

        self.assertEqual(response.status_code, 201)

        response = self.client.get("/kolotok/products/")
        self.assertEqual(len(response.data), count_product + 1)

        # Создаю продукт с некоректными данными
        response = self.client.post("/kolotok/products/", data={
                                                                "name": '',
                                                                "price": '',
                                                                "article": '',
                                                                "height": -137565,
                                                                "max_lamp_power": 'string',
                                                                "sub_category": []
                                                            }, follow=True, format='json')
        self.assertEqual(response.data['name'][0], 'This field may not be blank.')
        self.assertEqual(response.data['price'][0], 'A valid integer is required.')
        self.assertEqual(response.data['height'][0], 'Ensure this value is greater than or equal to 0.')
        self.assertEqual(response.data['article'][0], 'This field may not be blank.')
        self.assertEqual(response.data['max_lamp_power'][0], 'A valid integer is required.')
        self.assertEqual(response.data['sub_category'][0], 'This list may not be empty.')
        self.assertEqual(response.status_code, 400)

        response = self.client.post("/kolotok/products/", data={
                                                                "name": 'Продуктик',
                                                                "sub_category": [
                                                                    0
                                                                ]
                                                            }, follow=True, format='json')

        self.assertEqual(response.data['sub_category'][0], 'Invalid pk "0" - object does not exist.')
        self.assertEqual(response.status_code, 400)

        response = self.client.post("/kolotok/products/", data={
                                                                "name": 'Продуктик',
                                                                "sub_category": [
                                                                    'string'
                                                                ]
                                                            }, follow=True, format='json')

        self.assertEqual(response.data['sub_category'][0], 'Incorrect type. Expected pk value, received str.')
        self.assertEqual(response.status_code, 400)

        """
        Testing product method put
        """

        # Обновляю продукт с корректными данными
        response = self.client.put(f"/kolotok/products/{Product.objects.all()[0].id}/", data={
                                                                                      "name": "Name",
                                                                                      "price": 12445,
                                                                                      "sub_category": [
                                                                                        SubCategory.objects.all()[0].id
                                                                                      ]
                                                                                    }, follow=True)

        self.assertEqual(response.data['name'], 'Name')
        self.assertEqual(response.status_code, 200)

        # Обновляю продукт с не корректными данными
        response = self.client.put(f"/kolotok/products/{Product.objects.all()[0].id}/", data={
                                                                                              "name": "Name",
                                                                                              "price": 'string',
                                                                                              "height": -137565,
                                                                                              "sub_category": [
                                                                                                'string'
                                                                                              ]
                                                                                            }, follow=True)

        self.assertEqual(response.data['price'][0], 'A valid integer is required.')
        self.assertEqual(response.data['height'][0], 'Ensure this value is greater than or equal to 0.')
        self.assertEqual(response.data['sub_category'][0], 'Incorrect type. Expected pk value, received str.')
        self.assertEqual(response.status_code, 400)

        response = self.client.put(f"/kolotok/products/{Product.objects.all()[0].id}/", data={
                                                                                              "name": "Name",
                                                                                              "price": 'string',
                                                                                              "height": -137565,
                                                                                              "sub_category": [
                                                                                                183743
                                                                                              ]
                                                                                            }, follow=True)

        self.assertEqual(response.data['sub_category'][0], 'Invalid pk "183743" - object does not exist.')
        self.assertEqual(response.status_code, 400)

        """
        Testing product method patch
        """

        # Обновляю продукт с корректными данными
        response = self.client.patch(f"/kolotok/products/{Product.objects.all()[0].id}/", data={
                                                                                      "name": "Name",
                                                                                      "price": 12445,
                                                                                      "sub_category": [
                                                                                        SubCategory.objects.all()[0].id
                                                                                      ]
                                                                                    }, follow=True)

        self.assertEqual(response.data['name'], 'Name')
        self.assertEqual(response.status_code, 200)

        # Обновляю продукт с не корректными данными
        response = self.client.patch(f"/kolotok/products/{Product.objects.all()[0].id}/", data={
                                                                                              "name": "Name",
                                                                                              "price": 'string',
                                                                                              "height": -137565,
                                                                                              "sub_category": [
                                                                                                'string'
                                                                                              ]
                                                                                            }, follow=True)

        self.assertEqual(response.data['price'][0], 'A valid integer is required.')
        self.assertEqual(response.data['height'][0], 'Ensure this value is greater than or equal to 0.')
        self.assertEqual(response.data['sub_category'][0], 'Incorrect type. Expected pk value, received str.')
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(f"/kolotok/products/{Product.objects.all()[0].id}/", data={
                                                                                              "name": "Name",
                                                                                              "price": 'string',
                                                                                              "height": -137565,
                                                                                              "sub_category": [
                                                                                                183743
                                                                                              ]
                                                                                            }, follow=True)

        self.assertEqual(response.data['sub_category'][0], 'Invalid pk "183743" - object does not exist.')
        self.assertEqual(response.status_code, 400)

        """
        Testing product method delete
        """

        response = self.client.delete(f"/kolotok/products/{Product.objects.all()[0].id}/", follow=True)
        self.assertEqual(response.status_code, 204)

    def test13_building_views(self):
        """
        Testing building method get
        """
        self.client.force_authenticate(self.manager)

        response = self.client.get("/academ/building/", follow=True)
        self.assertEqual(response.status_code, 200)

        """
        Testing building method post
        """

        self.client.force_authenticate(self.manager)

        # Создаю дом и произвожу проверку
        response = self.client.get("/academ/building/")
        count_building = len(response.data)

        response = self.client.post("/academ/building/", data={
                                                              "address": "Building 1",
                                                              "floors": 12,
                                                              "sections": 3,
                                                              "types": 1
                                                            }, follow=True)
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/academ/building/")
        self.assertEqual(len(response.data), count_building + 1)

        response = self.client.post("/academ/building/", data={
                                                              "address": "Academic",
                                                              "floors": -12,
                                                            }, follow=True)

        self.assertEqual(response.data['address'][0], '"Academic" is not a valid choice.')
        self.assertEqual(response.data['floors'][0], 'Ensure this value is greater than or equal to 0.')
        self.assertEqual(response.status_code, 400)

        """
        Testing building method delete
        """

        response = self.client.delete(f"/academ/building/{Building.objects.all()[0].id}/", follow=True)

        self.assertEqual(response.status_code, 204)

        # """
        # Testing building method put
        # """
        #
        # response = self.client.put(f"/academ/building/{Building.objects.all()[0].id}/", data={
        #                                                       "address": "Building 2",
        #                                                       "floors": 12,
        #                                                       "sections": 3,
        #                                                       "types": 1
        #                                                     }, follow=True)
        # print(response.data)
        # self.assertEqual(response.data['address'], 'Building 2')
        # self.assertEqual(response.status_code, 200)
        #
        # response = self.client.put(f"/academ/building/{Building.objects.all()[0].id}/", data={
        #                                                       "address": "Academic",
        #                                                       "floors": -12,
        #                                                     }, follow=True)
        #
        # self.assertEqual(response.data['address'][0], '"Academic" is not a valid choice.')
        # self.assertEqual(response.data['floors'][0], 'Ensure this value is greater than or equal to 0.')
        # self.assertEqual(response.status_code, 400)
        #
        # """
        # Testing building method patch
        # """
        #
        # response = self.client.patch(f"/academ/building/{Building.objects.all()[0].id}/", data={
        #                                                       "address": "Building 1",
        #                                                       "floors": 12,
        #                                                       "sections": 3,
        #                                                       "types": 1
        #                                                     }, follow=True)
        # self.assertEqual(response.data['address'], 'Building 1')
        # self.assertEqual(response.status_code, 200)
        #
        # response = self.client.patch(f"/academ/building/{Building.objects.all()[0].id}/", data={
        #                                                       "address": "Academic",
        #                                                       "floors": -12,
        #                                                     }, follow=True)
        #
        # self.assertEqual(response.data['address'][0], '"Academic" is not a valid choice.')
        # self.assertEqual(response.data['floors'][0], 'Ensure this value is greater than or equal to 0.')
        # self.assertEqual(response.status_code, 400)

    def test14_client_views(self):
        """
        Testing client method get
        """
        self.client.force_authenticate(self.manager)

        response = self.client.get("/academ/client/", follow=True)
        self.assertEqual(response.status_code, 200)

        """
        Testing client method post
        """

        self.client.force_authenticate(self.manager)

        # Создаю клиента и произвожу проверку
        response = self.client.get("/academ/client/")
        count_client = len(response.data)

        response = self.client.post("/academ/client/", data={
                                                              "name": "string",
                                                              "surname": "string",
                                                              "patronymic": "string",
                                                              "phone_number": "+999999123",
                                                              "info": "string",
                                                              "apartment": Apartment.objects.all()[0].id
                                                            }, follow=True)
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/academ/client/")
        self.assertEqual(len(response.data), count_client + 1)

        response = self.client.post("/academ/client/", data={
                                                              "name": "string",
                                                              "patronymic": "   ",
                                                              "phone_number": "+11447",
                                                              "apartment": 'string'
                                                            }, follow=True)
        self.assertEqual(response.data['surname'][0], 'This field is required.')
        self.assertEqual(response.data['patronymic'][0], 'This field may not be blank.')
        self.assertEqual(response.data['phone_number'][0],
                         "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        self.assertEqual(response.data['apartment'][0], 'Incorrect type. Expected pk value, received str.')
        self.assertEqual(response.status_code, 400)

        """
        Testing client method put
        """

        response = self.client.put(f"/academ/client/{FixatedClient.objects.all()[0].id}/", data={
                                                                              "name": "Slava",
                                                                              "surname": "string",
                                                                              "patronymic": "string",
                                                                              "phone_number": "+999999123",
                                                                              "info": "string",
                                                                              "apartment": Apartment.objects.all()[0].id
                                                                            }, follow=True)
        self.assertEqual(response.data['name'], 'Slava')
        self.assertEqual(response.status_code, 200)

        response = self.client.put(f"/academ/client/{FixatedClient.objects.all()[0].id}/", data={
                                                              "name": "string",
                                                              "patronymic": "   ",
                                                              "phone_number": "+11447",
                                                              "apartment": 'string'
                                                            }, follow=True)
        self.assertEqual(response.data['surname'][0], 'This field is required.')
        self.assertEqual(response.data['patronymic'][0], 'This field may not be blank.')
        self.assertEqual(response.data['phone_number'][0],
                         "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        self.assertEqual(response.data['apartment'][0], 'Incorrect type. Expected pk value, received str.')
        self.assertEqual(response.status_code, 400)

        """
        Testing client method patch
        """

        response = self.client.patch(f"/academ/client/{FixatedClient.objects.all()[0].id}/", data={
                                                                              "name": "Slava",
                                                                              "surname": "string",
                                                                              "patronymic": "string",
                                                                              "phone_number": "+999999123",
                                                                              "info": "string",
                                                                              "apartment": Apartment.objects.all()[0].id
                                                                            }, follow=True)
        self.assertEqual(response.data['name'], 'Slava')
        self.assertEqual(response.status_code, 200)

        response = self.client.patch(f"/academ/client/{FixatedClient.objects.all()[0].id}/", data={
                                                              "name": "string",
                                                              "patronymic": "   ",
                                                              "phone_number": "+11447",
                                                              "apartment": 'string'
                                                            }, follow=True)
        self.assertEqual(response.data['patronymic'][0], 'This field may not be blank.')
        self.assertEqual(response.data['phone_number'][0],
                         "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        self.assertEqual(response.data['apartment'][0], 'Incorrect type. Expected pk value, received str.')
        self.assertEqual(response.status_code, 400)

        """
        Testing client method delete
        """

        response = self.client.delete(f"/academ/client/{FixatedClient.objects.all()[0].id}/", follow=True)

        self.assertEqual(response.status_code, 204)

    def test15_reservation_views(self):
        """
        Testing reservation method get
        """
        self.client.force_authenticate(self.manager)

        response = self.client.get("/academ/reservation/", follow=True)
        self.assertEqual(response.status_code, 200)

        """
        Testing client method post
        """

        self.client.force_authenticate(self.manager)

        # Создаю резерватсию и произвожу проверку
        response = self.client.get("/academ/reservation/")
        count_reservation = len(response.data)

        response = self.client.post("/academ/reservation/", data={
                                                                      "user": User.objects.all()[0].id,
                                                                      "apartment": Apartment.objects.all()[0].id
                                                                    }, follow=True)
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/academ/reservation/")
        self.assertEqual(len(response.data), count_reservation + 1)

        # Создаю резерватсию отправляя не коректные данные
        response = self.client.post("/academ/reservation/", data={
                                                                  "user": 100,
                                                                  "apartment": ' '
                                                                }, follow=True)

        self.assertEqual(response.data['user'][0], 'Invalid pk "100" - object does not exist.')
        self.assertEqual(response.data['apartment'][0], 'Incorrect type. Expected pk value, received str.')
        self.assertEqual(response.status_code, 400)

        """
        Testing reservation method delete
        """

        response = self.client.delete(f"/academ/reservation/{Reservation.objects.all()[0].id}/", follow=True)

        self.assertEqual(response.status_code, 204)

    def test16_favorites_views(self):
        """
        Testing favorites method get
        """
        self.client.force_authenticate(self.manager)

        response = self.client.get("/academ/favorite/", follow=True)
        self.assertEqual(response.status_code, 200)

        """
        Testing favorites method post
        """

        self.client.force_authenticate(self.manager)

        # Создаю избранное и произвожу проверку

        response = self.client.get("/academ/reservation/")
        count_favorites = len(response.data)

        response = self.client.post("/academ/favorite/", data={
                                                                    "apartment": Apartment.objects.all()[0].id
                                                                }, follow=True, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/academ/favorite/")
        self.assertEqual(len(response.data), count_favorites + 1)

        # Создаю избранное отправляя не коректные данные
        response = self.client.post("/academ/favorite/", data={
                                                                  "apartment": ' '
                                                                }, follow=True, format='json')

        self.assertEqual(response.data['apartment'][0], 'Incorrect type. Expected pk value, received str.')
        self.assertEqual(response.status_code, 400)

        """
        Testing favorites method delete
        """

        response = self.client.delete(f"/academ/favorite/{Favorite.objects.all()[0].id}/", follow=True)
        self.assertEqual(response.status_code, 204)

    def test17_support_views(self):
        """
        Testing support method get
        """
        self.client.force_authenticate(self.manager)

        response = self.client.get("/academ/support/", follow=True)
        self.assertEqual(response.status_code, 200)

        """
        Testing support method post
        """

        self.client.force_authenticate(self.manager)

        # Создаю и произвожу проверку

        response = self.client.get("/academ/support/", follow=True)
        count_support = len(response.data)

        response = self.client.post("/academ/support/", data={
                                                              "name": "user",
                                                              "phone_number": "+79195473069",
                                                              "email": "menager@example.com",
                                                              "topic_type": 1,
                                                              "message": "string",
                                                            }, follow=True, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/academ/support/")
        self.assertEqual(len(response.data), count_support + 1)

        # Создаю отправляя не коректные данные
        response = self.client.post("/academ/support/", data={
                                                              "name": " ",
                                                              "phone_number": "+791954730",
                                                              "email": "wfdwfppw",
                                                              "topic_type": 8,
                                                              "message": "string",
                                                            }, follow=True, format='json')

        self.assertEqual(response.data['name'][0], 'This field may not be blank.')
        self.assertEqual(response.data['email'][0], 'Enter a valid email address.')
        self.assertEqual(response.data['topic_type'][0], '"8" is not a valid choice.')
        self.assertEqual(response.status_code, 400)

        """
        Testing support method delete
        """

        response = self.client.delete(f"/academ/support/{SupportTicket.objects.all()[0].id}/", follow=True)
        self.assertEqual(response.status_code, 204)
