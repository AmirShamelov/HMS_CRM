from django.db import models
from doctor.models import Doctor


class Review(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=12, verbose_name='Номер телефона')
    date = models.DateField(verbose_name='Дата приема')
    review = models.TextField(verbose_name='Отзыв')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Врач')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Отзыв {self.first_name} {self.last_name}'

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Отзыв на врача'
        verbose_name_plural = 'Отзывы на врачей'



