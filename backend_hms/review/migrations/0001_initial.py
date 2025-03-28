# Generated by Django 4.2 on 2025-03-26 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctor', '0003_alter_doctor_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('phone_number', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('date', models.DateField(verbose_name='Дата приема')),
                ('review', models.TextField(verbose_name='Отзыв')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('doctor_iin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor')),
            ],
        ),
    ]
