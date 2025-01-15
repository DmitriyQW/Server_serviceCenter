from django.db import models
from django.core.validators import MaxValueValidator #Валидация
from django.contrib.auth.hashers import make_password #Хеширования пароля
# Create your models here.

class Worker(models.Model):
    id_worker = models.AutoField(primary_key=True)
    login_worker = models.CharField(max_length=8)
    tel_worker = models.CharField(max_length=11)
    email_worker = models.EmailField(max_length=60)
    password_worker = models.CharField(max_length=18)
    question_worker = models.CharField(max_length=25)
    answer_worker = models.CharField(max_length=25)
    fio_worker = models.CharField(max_length=60)
    address_worker = models.CharField(max_length=60)
    age_worker = models.PositiveSmallIntegerField(validators=
    [MaxValueValidator(100)]) #Валидация максимальный возврат 100 лет
    dateregister_worker = models.DateField()

class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    login_user = models.CharField(max_length=8)
    tel_user = models.CharField(max_length=11)
    email_user = models.EmailField(max_length=60)
    password_user = models.CharField(max_length=18)
    question_user = models.CharField(max_length=25)
    answer_user = models.CharField(max_length=25)
    fio_user = models.CharField(max_length=60)
    address_user = models.CharField(max_length=60)
    age_user = models.PositiveSmallIntegerField(validators=
    [MaxValueValidator(100)]) #Валидация максимальный возврат 100 лет
    dateregister_user = models.DateField()