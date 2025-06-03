from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    blood_types = (
        (1, '0-'),
        (2, '0+'),
        (3, 'A-'),
        (4, 'A+'),
        (5, 'B-'),
        (6, 'B+'),
        (7, 'AB+'),
        (8, 'AB-'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(max_length=12, blank=True, verbose_name='Номер телефона')
    address = models.TextField(blank=True, verbose_name='Адрес')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    blood = models.IntegerField(choices=blood_types, null=True, blank=True, verbose_name='Группа крови')
    allergies = models.TextField(blank=True, null=True, verbose_name='Аллергия')
    chronic_disease = models.TextField(blank=True, null=True, verbose_name='Хроническое заболевание')

    def __str__(self):
        return f'Профиль {self.user.first_name} {self.user.last_name}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


