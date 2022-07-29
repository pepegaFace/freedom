from datetime import datetime, timezone
from academ.models import Reservation, Appointment, Apartment


def remove_expired_reservations():
    """
    Функция для удаления устаревших записей в таблице 'Reservations'
    """
    print(f'Cron was started at {datetime.now()}')
    reservations = Reservation.objects.all()
    for reservation in reservations:
        if reservation.expiration_date < datetime.now(timezone.utc):
            print(f'Deleting {Reservation.objects.filter(pk=reservation.id)}')
            Reservation.objects.filter(pk=reservation.id).delete()
    print(f'Cron was stopped at {datetime.now()}')


def remove_expired_appointments():
    """
    Функция для удаления устаревших записей в таблице 'Appointments'
    """
    print(f'\nCron was started at {datetime.now()}\n')
    appointments = Appointment.objects.filter(date__lte=datetime.today().strftime('%Y-%m-%d')).delete()
    print(f'Removed appointments: {appointments}')
    print(f'\nCron was stopped at {datetime.now()}')


def mycron():
    print(f'Cron was started at {datetime.now()}')
    print(f'ALL APARTMENTS IN DB')
    print(Apartment.objects.all())
    print(f'Cron was stopped at {datetime.now()}')


