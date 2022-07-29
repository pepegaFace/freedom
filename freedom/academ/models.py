from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractUser, UnicodeUsernameValidator)
from django.utils.translation import gettext_lazy as _
from freedom.validators import *
from django.dispatch import receiver
from django.utils import timezone, dateformat
import os.path
from django.core.files.storage import FileSystemStorage
from freedom.models import SoftDeleteAbstract, SoftDeleteUserAbstract, image_storage
from rest_framework.exceptions import ValidationError as drf_ValidationError

# import datetime

username_validator = UnicodeUsernameValidator()


def building_directory_path(instance, filename):
    """
    Функция, генерирующая путь до картинки дома
    @param instance: конкретный дом
    @param filename: имя файла
    @return:
    """
    return f'buildings/{instance.building}/{filename}'


def building_uploaded_schema_directory_path(instance, filename):
    """
    Функция, генерирующая путь, для загружаемого чертежа этажа дома
    @param instance: конкретный дом
    @param filename: имя файла
    @return:
    """
    return f'blueprints/{instance.address}/schema_uploaded/{filename}'


def building_default_schema_directory_path(instance):
    """
    Функция, генерирующая путь до имеющегося по умолчанию чертежа этажа дома
    @param instance: конкретный дом
    @return:
    """
    filepath = f'/blueprints/{instance.address}/schema_default/schema.svg'

    if not os.path.isfile(image_storage.location + filepath):
        filepath = 'blueprint.svg'

    return f'{filepath}'


def avatar_directory_path(instance, filename):
    """
    Функция, генерирующая путь для загружаемой аватарки пользователя
    @param instance:
    @param filename: загружаемая аватарка
    @return:
    """
    return u'avatars/{0}'.format(filename)


def blueprint_directory_path(instance):
    """
    Функция, генерирующая путь до имеющегося по умолчанию чертежа квартиры
    @param instance: квартира
    @return:
    """
    if '.' not in str(instance.area):
        instance.area += '.0'

    area = str(instance.area).split('.')

    filepath = f'/blueprints/{instance.building.address}/section_{instance.section}' \
               f'/{instance.type}_{area[0]}-{area[1]}.svg'

    # print(image_storage.location + filepath)
    if not os.path.isfile(image_storage.location + filepath):
        filepath = 'blueprint.svg'
        # print('File does not exist!')

    return f'{filepath}'


def custom_blueprints(instance, filename):
    """
    Функция, генерирующая путь для загружаемых чертежей квартир
    @param instance:
    @param filename: чертеж квартиры
    @return:
    """
    return f'building/custom_blueprints/{filename}'


def gallery_image_directory_path(instance, filename):
    filepath = f"gallery/{instance.building.address}/{filename}"
    return f'{filepath}'


class User(SoftDeleteUserAbstract):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        default=None,
        null=False,
        unique=True,
        help_text=_('Required'),
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
    )

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required'),
        validators=[username_validator],
        default=None,
        null=False,
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    password = models.CharField(
        _('password'),
        max_length=128,
        default=None,
        null=False,
    )

    is_manager = 'Manager'
    is_crm_admin = 'AdminCRM'
    is_default = 'DefaultUser'

    ROLE_CHOICES = (
        (is_default, "Пользователь"),
        (is_manager, "Менеджер"),
        (is_crm_admin, "Администратор CRM"),
    )
    role = models.CharField(choices=ROLE_CHOICES, default=is_default, max_length=15)

    # avatar = models.ImageField(_('Avatar'), upload_to=get_img_upload_path, validators=[image_restriction],
    #                            default=settings.FILE_PATH_FIELD_DIRECTORY + '/avatars/default.jpeg')

    phone_number = models.CharField(_('Phone number'), validators=[phone_regex], max_length=17, help_text=_('Required'),
                                    default='XXXXXXXX')

    avatar = models.ImageField(_('Avatar'), upload_to=avatar_directory_path, storage=image_storage,
                               validators=[image_restriction], blank=True, null=True,
                               default='avatar.png')

    def __str__(self):
        return f'{self.username}'


class Building(models.Model):
    ADDRESS_CHOICES = (
        ('Academ', "Академический"),
        ('Building 1', "Building 1"),
        ('Building 2', "Building 2"),
    )

    address = models.CharField(_('Address'), help_text=_('Required'), choices=ADDRESS_CHOICES,
                               default=None, null=True, unique=True, max_length=150)

    floors = models.PositiveSmallIntegerField(_('Floors'), help_text=_('Required'), default=1, null=True,
                                              validators=[validate_nonzero])

    sections = models.PositiveSmallIntegerField(_('Sections'), help_text=_('Required'), default=1, null=True,
                                                validators=[validate_nonzero])

    TYPES_CHOICES = (
        (1, "Только однокомнатные"),
        (2, "Однокомнатные и двухкомнатные"),
        (3, "Однокомнатные, двухкомнатные и трехкомантные"),
        (4, "Однокомнатные, двухкомнатные, трехкомантные и четырехкомнатные"),
        (5, "Однокомнатные, двухкомнатные, трехкомантные, четырехкомнатные и студии"),
    )

    types = models.PositiveSmallIntegerField(default=5, choices=TYPES_CHOICES)

    image = models.ImageField(_('Image'), default='building.jpg',  storage=image_storage,
                              upload_to=building_directory_path, blank=True, null=True)

    floor_schema = models.FileField(_('Floor schema'), default='blueprint.svg',
                                    storage=image_storage, upload_to=building_uploaded_schema_directory_path,
                                    blank=True, null=True, validators=[validate_image_file_extension])

    def __str__(self):
        return f'{self.address}'


@receiver(models.signals.pre_save, sender=Building)
def building_blueprint_receiver(sender, instance, **kwargs):
    """
    Функция, генерирующая путь до чертежа дома.
    Если файла с чертежем не существует - использует значение по умолчанию.
    @param sender: модель, которая шлет сигнал
    @param instance: представление модели
    @param kwargs:
    """
    if not instance.floor_schema:
        instance.floor_schema = building_default_schema_directory_path(instance)


class Apartment(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, help_text=_('Required'))

    number = models.PositiveSmallIntegerField(_('Number'), help_text=_('Required'), default=1, null=True,
                                              validators=[validate_nonzero])

    floor = models.PositiveSmallIntegerField(_('Floor'), help_text=_('Required'), default=1, null=True,
                                             validators=[validate_nonzero])

    section = models.PositiveSmallIntegerField(_('Section'), help_text=_('Required'), default=1, null=True,
                                               validators=[validate_nonzero])

    TYPE_CHOICES = (
        (1, "Однокомнатная"),
        (2, "Двухкомнатная"),
        (3, "Трехкоманатная"),
        (4, "Четырехкомнатная"),
        (5, "Студия"),
    )

    type = models.IntegerField(choices=TYPE_CHOICES, default=1, null=True)
    # image = models.FilePathField(_('Image'), path=settings.FILE_PATH_FIELD_DIRECTORY + '/building1',
    #                              default=settings.FILE_PATH_FIELD_DIRECTORY + '/building1')
    # image = models.ImageField(_('Image'), default=settings.FILE_PATH_FIELD_DIRECTORY + '/building1/default.jpg')

    # image = models.CharField(_('Image'), default=settings.FILE_PATH_FIELD_DIRECTORY + '/building1/default.jpg',
    #                          max_length=150, blank=True)

    image = models.ImageField(_('Image'), default='blueprints/blueprint.jpg', storage=image_storage,
                              upload_to=custom_blueprints, blank=True, null=True)

    # area = models.FloatField(_('Area'), help_text=_('Required'), default=1, null=True,
    #                          validators=[validate_positive_nonzero])

    area = models.CharField(_('Area'), help_text=_('Required'), default='1', null=True, max_length=150,
                            validators=[validate_positive_nonzero])
    cost = models.PositiveIntegerField(_('Cost'), default=1, null=False, validators=[validate_nonzero])
    reserved = models.BooleanField(_('Reservation'), default=False)

    class Meta:
        unique_together = ('building', 'number', )

    def __str__(self):
        return f'Дом: {self.building}, Номер квартиры: {self.number}, id: {self.id}'


@receiver(models.signals.pre_save, sender=Apartment)
def check_apartment_data(sender, instance, **kwargs):
    """
    Функция, генерирующая путь до чертежа квартиры.
    Если файла с чертежем не существует - использует значение по умолчанию.
    @param sender: модель, которая шлет сигнал
    @param instance: представление модели
    @param kwargs:
    """
    if instance.building.types < instance.type or \
            instance.building.floors < instance.floor or \
            instance.building.sections < instance.section:
        raise Exception(f""
                        f"EXCEPTION: Building.types: {instance.building.types} < Apartment.type: {instance.type} = '{instance.building.types < instance.type}'\n"
                        f"Building.floors: {instance.building.floors} < Apartment.floor: {instance.floor} = '{instance.building.floors < instance.floor}'\n"
                        f"Building.sections: {instance.building.sections} < Apartment.section: {instance.section} = '{instance.building.sections < instance.section}'")
    else:
        instance.image = blueprint_directory_path(instance)
    # else:
    #     area = str(instance.area).split('.')
    #     filepath = f'{settings.FILE_PATH_FIELD_DIRECTORY}/{instance.building.address}/section_{instance.section}' \
    #                f'/{instance.type}_{area[0]}-{area[1]}.svg'
    #     if os.path.isfile(filepath):
    #         instance.image = filepath
    #         # print(instance.image)
    #     else:
    #         print('File does not exist, using default value')
    #         instance.image = settings.FILE_PATH_FIELD_DIRECTORY + '/building1/default.jpg'


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)

    date_added = models.DateTimeField(_('Added'),
                                      default=timezone.now(),
                                      editable=False,
                                      blank=True)

    expiration_date = models.DateTimeField(_('Expiration date'),
                                           default=timezone.now() + timezone.timedelta(days=1),
                                           editable=False,
                                           blank=True)


@receiver(models.signals.post_save, sender=Reservation)
def make_apartment_reserved(sender, instance, **kwargs):
    """
    Функция, которая меняет статус 'reserved' на True у квартиры с id = instance.pk на True, при сигнале 'pre_save'
    от модели Reservation
    @param sender: Reservation
    @param instance: Reservation.pk
    @param kwargs: kwargs
    """
    if instance.pk:
        try:
            current_apartment = Apartment.objects.get(pk=instance.apartment.id)
        except Apartment.DoesNotExist:
            return
        else:
            current_apartment.reserved = True
            current_apartment.save()


@receiver(models.signals.post_delete, sender=Reservation)
def expire_reservation(sender, instance, **kwargs):
    """
    Функция, которая меняет статус 'reserved' на False у квартиры с id = instance.pk на True, при сигнале 'pre_save'
    от модели Reservation
    @param sender: Reservation
    @param instance: Reservation.pk
    @param kwargs: kwargs
    """
    if instance.pk:
        try:
            current_apartment = Apartment.objects.get(pk=instance.apartment.id)
        except User.DoesNotExist:
            return
        else:
            current_apartment.reserved = False
            current_apartment.save()


class Appointment(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, help_text=_('Required'))

    client = models.CharField('Client', help_text='Required', max_length=150)

    phone_number = models.CharField(_('Phone number'), validators=[phone_regex], max_length=17, help_text=_('Required'))

    date = models.DateField(_('Date'), help_text=_('Required'), validators=[date_validator])

    TIME_CHOICES = (
        ("9:00", "9:00"),
        ("9:30", "9:30"),
        ("10:00", "10:00"),
        ("10:30", "10:30"),
        ("11:00", "11:00"),
        ("11:30", "11:30"),
        ("12:00", "12:00"),
        ("12:30", "12:30"),
        ("13:00", "13:00"),
        ("13:30", "13:30"),
        ("14:00", "14:00"),
        ("14:30", "14:30"),
        ("15:00", "15:00"),
        ("15:30", "15:30"),
        ("16:00", "16:00"),
        ("16:30", "16:30"),
        ("17:00", "17:00"),
        ("17:30", "17:30"),
    )

    time = models.CharField(choices=TIME_CHOICES, max_length=150, help_text=_('Required'), default="9:00")

    building = models.ForeignKey(Building, on_delete=models.CASCADE, help_text=_('Required'))

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, help_text=_('Required'),
                                  limit_choices_to={'reserved': False})

    class Meta:
        unique_together = [['date', 'time', 'apartment']]

    def clean(self):
        """
        Метод, который проверяет, существует ли выбранная квартира в выбранном доме.
        @rtype: object
        """
        if self.apartment not in Apartment.objects.filter(building=self.building):
            raise drf_ValidationError({'apartment': _('Select a valid apartment please')})

    def save(self, *args, **kwargs):
        """
        Метод, который вызывается при сохранении представления модели.
        Метод был переписан для вызова clean функций перед сохранением.
        @rtype: object
        """
        self.full_clean()
        return super(Appointment, self).save(*args, **kwargs)

    def __str__(self):
        return f'Запись клиента: "{self.client}", на время "{self.time}, на квартиру: "{self.building, self.apartment}"'


class FixatedClient(models.Model):
    name = models.CharField(_('Name'), help_text=_('Required'), max_length=150)
    surname = models.CharField(_('Surname'), help_text=_('Required'), max_length=150)
    patronymic = models.CharField(_('Patronymic'), help_text=_('Required'), max_length=150)

    phone_number = models.CharField(_('Phone number'), validators=[phone_regex], max_length=17, help_text=_('Required'),
                                    unique=True)

    # building = models.ForeignKey(Building, on_delete=models.CASCADE, help_text=_('Required'))
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, help_text=_('Required'))

    info = models.CharField(_('Additional info'), default=None, max_length=1500, blank=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text=_('Required'))
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, help_text=_('Required'))

    def __str__(self):
        return f'Избранное для пользователя: {self.user}'

    class Meta:
        unique_together = ('user', 'apartment',)


class SupportTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text=_('Required'), blank=True, null=True)
    name = models.CharField(_('Name'), help_text=_('Required'), max_length=150)

    phone_number = models.CharField(_('Phone number'), validators=[phone_regex], max_length=17, help_text=_('Required'))

    email = models.EmailField(verbose_name='Email address', max_length=255, null=False, help_text=_('Required'))

    TOPIC_TYPES = (
        (1, "Вопрос по покупке"),
        (2, "Вопрос по заселению"),
        (3, "Вопрос по стройке"),
        (4, "Вопрос по проживанию"),
        (5, "Обращение в службу безопасности"),
        (6, "Предложение о сотрудничестве"),
        (7, "Сообщить об ошибке на сайте"),
        (8, "Другое")
    )

    topic_type = models.PositiveSmallIntegerField(choices=TOPIC_TYPES, default=1)

    message = models.CharField(_('Message'), help_text=_('Required'), default=None, max_length=1500)


# @receiver(models.signals.post_save, sender=SupportTicket)
# def get_support_ticket_user(sender, instance, **kwargs):
#     """
#     Функция, присваивающая значение в поле user модели SupportTicket.
#     @param sender: SupportTicket
#     @param instance: SupportTicket.pk
#     @param kwargs: kwargs
#     """
#     if instance.pk:
#         for frame_record in inspect.stack():
#             if frame_record[3] == 'get_response':
#                 request = frame_record[0].f_locals['request']
#                 if request.user.id:
#                     SupportTicket.objects.filter(pk=instance.pk).update(user=request.user.id)
#         else:
#             request = None

class ImageGallery(models.Model):
    """
    Модель галлереи
    """
    building = models.ForeignKey(Building, on_delete=models.CASCADE, help_text=_('Required'))
    image = models.ImageField(_('image'), upload_to=gallery_image_directory_path, storage=image_storage,
                              validators=[image_restriction], help_text=_('Required'))

    def __str__(self):
        return f'Галлерея для дома: {self.building}'

    class Meta:
        unique_together = ('building', 'image', )
