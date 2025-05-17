from django.contrib.auth.models import AbstractUser
from django.db import models

from Pereval import settings


class User(AbstractUser):
    email = models.EmailField(max_length=200)
    fam = models.CharField(max_length=50, verbose_name='Фамилия')
    name = models.CharField(max_length=50, verbose_name='Имя')
    otc = models.CharField(max_length=50, verbose_name='Отчество')
    phone = models.CharField(max_length=16, verbose_name='Телефон')


class Coordinates(models.Model):
    latitude = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    height = models.IntegerField(null=True)


class Level(models.Model):
    difficulty_1 = 'I'
    difficulty_2 = 'II'
    difficulty_3 = 'III'
    difficulty_4 = 'IV'
    difficulty_5 = 'V'
    difficulty_6 = 'VI'

    LEVEL_CHOICES = {
        (difficulty_1, 'Категория I'),
        (difficulty_2, 'Категория II'),
        (difficulty_3, 'Категория III'),
        (difficulty_4, 'Категория IV'),
        (difficulty_5, 'Категория V'),
        (difficulty_6, 'Категория VI'),
    }

    spring = models.CharField(max_length=3, choices=LEVEL_CHOICES, default=difficulty_1, verbose_name='Весна')
    summer = models.CharField(max_length=3, choices=LEVEL_CHOICES, default=difficulty_1, verbose_name='Лето')
    autumn = models.CharField(max_length=3, choices=LEVEL_CHOICES, default=difficulty_1, verbose_name='Осень')
    winter = models.CharField(max_length=3, choices=LEVEL_CHOICES, default=difficulty_1, verbose_name='Зима')


class SpecificationOfPereval(models.Model):
    new = 'new'
    pending = 'pnd'
    accepted = 'acp'
    rejected = 'rjt'

    STATUSES = [
        (new, 'Новое описание'),
        (pending, 'На рассмотрении'),
        (accepted, 'Подтверждено'),
        (rejected, 'Отклонено'),
    ]

    beauty_title = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=50, blank=True)
    other_titles = models.CharField(max_length=128, blank=True)
    connect = models.CharField(max_length=128, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coords = models.OneToOneField(Coordinates, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=STATUSES, default='new')
    level = models.ForeignKey(Level, on_delete=models.CASCADE)


class Images(models.Model):
    data = models.URLField(max_length=1500, blank=True, verbose_name='Cсылка на вид')
    title = models.TextField(blank=True, verbose_name='Описание вида')
    pereval = models.ForeignKey(
        SpecificationOfPereval,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name='Вид перевала',
        # на сколько я понял, это имя нужно для сериализатора,
        # он будет собирать список в этом поле и номеру перевала
        related_name='images',
    )

    def __str__(self):
        return self.title[:200]
