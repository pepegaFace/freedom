from django.db import models
from django.conf import settings
from .managers import SoftDeleteManager, SoftDeleteManagerDeleted, SoftDeleteUserManager
from django.utils.translation import gettext_lazy as _
from .validators import *
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import AbstractUser


image_storage = FileSystemStorage(
    # Physical file location ROOT
    location=u'{0}/pictures/'.format(settings.MEDIA_ROOT),
    # Url for file
    base_url=u'{0}pictures/'.format(settings.MEDIA_URL),
)


class SoftDeleteUserAbstract(AbstractUser):
    class Meta:
        abstract = True

    deleted_on = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteUserManager()  # Expose non-deleted objects only
    objects_unfiltered = models.Manager()  # Expose ALL objects (used primarily in Admin panel)
    objects_deleted = SoftDeleteManagerDeleted()  # Expose all DELETED objects (used primarily in for testing)

    def delete(self):
        self.deleted_on = timezone.now()
        self.is_active = False
        self.save()

    def hard_delete(self):
        super(SoftDeleteUserAbstract, self).delete()


class SoftDeleteAbstract(models.Model):
    class Meta:
        abstract = True

    deleted_on = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()  # Expose non-deleted objects only
    objects_unfiltered = models.Manager()  # Expose ALL objects (used primarily in Admin panel)
    objects_deleted = SoftDeleteManagerDeleted()  # Expose all DELETED objects (used primarily in for testing)

    def delete(self):
        self.deleted_on = timezone.now()
        self.save()

    def hard_delete(self):
        super(SoftDeleteAbstract, self).delete()


class Ticket(models.Model):
    """
    Модель заявок
    """

    # Личные данные
    name = models.CharField('Name', help_text='Required', max_length=150)
    email = models.EmailField('Email', help_text='Required', max_length=150)
    phone_number = models.CharField(_('Phone number'), validators=[phone_regex], max_length=17, default=None,
                                    help_text=_('Required'))

    # Данные о доме
    address = models.CharField('Address', help_text='Required', max_length=150)

    HOUSE_TYPES = (
        (1, "Кирпичный"),
        (2, "Монолитный"),
        (3, "Панельный"),
    )

    house_type = models.PositiveSmallIntegerField(_('House type'), help_text=_('Required'), choices=HOUSE_TYPES)

    CONDITION_TYPES = (
        (1, "Требует ремонта"),
        (2, "Не требует ремонта"),
    )

    condition_type = models.PositiveSmallIntegerField(_('Condition type'), help_text=_('Required'),
                                                      choices=CONDITION_TYPES)

    # Данные о квартире
    apartment_floor = models.PositiveIntegerField(_('Apartment floor'), help_text=_('Required'), default=1)
    house_floors = models.PositiveIntegerField(_('Floors'), help_text=_('Required'), default=1)

    ROOM_TYPE_CHOICES = (
        (1, "Однокомнатная"),
        (2, "Двухкомнатная"),
        (3, "Трехкоманатная"),
        (4, "Четырехкомнатная"),
        (5, "Студия"),
    )

    rooms = models.PositiveSmallIntegerField(_('House type'), help_text=_('Required'), choices=ROOM_TYPE_CHOICES)
    adjoining_rooms = models.BooleanField(_('Adjoining rooms'), help_text=_('Required'), default=False)

    area = models.FloatField(_('Area'), help_text=_('Required'), default=1,
                             validators=[validate_positive_nonzero])

    living_area = models.FloatField(_('Living area'), help_text=_('Required'), default=1,
                                    validators=[validate_positive_nonzero])

    kitchen_area = models.FloatField(_('Kitchen area'), help_text=_('Required'), default=1,
                                     validators=[validate_positive_nonzero])

    date = models.DateTimeField(_('Added'),
                                default=timezone.now,
                                editable=False)

    def __str__(self):
        return f"Ticket address: '{self.address}', rooms: '{self.rooms}', area: '{self.area}', date: '{self.date}'"
