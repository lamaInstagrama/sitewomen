from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name='Дата рождения')
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True, verbose_name='Фото')
