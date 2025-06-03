from django.db import models

from django.contrib.auth.models import User
from department.models import Department


class Doctor(models.Model):
    doctor = models.ForeignKey(User, related_name='doctors', verbose_name='Врач', on_delete=models.CASCADE)
    education = models.CharField(max_length=50, verbose_name='Образование')
    position = models.CharField(max_length=50, verbose_name='Специализация')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name='Почта')
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    department = models.ForeignKey(Department, related_name='staff', verbose_name='Отделение', null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='doctors_images', blank=True, null=True, verbose_name='Фото')

    def __str__(self):
        return f'Врач {self.position} {self.doctor.first_name} {self.doctor.last_name}'

    def get_full_name(self):
        return f"{self.doctor.first_name} {self.doctor.last_name}"

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return 'http://127.0.0.1:8000/media/doctors_images/doctor1.png'



    class Meta:
        db_table = 'doctors'
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'

