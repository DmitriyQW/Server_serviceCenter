from django.db import models
from django.core.validators import MaxValueValidator #Валидация
from django.contrib.auth.hashers import make_password #Хеширования пароля
# Create your models here.

class Worker(models.Model):
    id_worker = models.AutoField(primary_key=True)
    login_worker = models.CharField(max_length=8)
    tel_worker = models.CharField(max_length=11)
    email_worker = models.EmailField(max_length=60)
    password_worker = models.CharField(max_length=200) #HES
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
    password_user = models.CharField(max_length=200) #HES
    question_user = models.CharField(max_length=25)
    answer_user = models.CharField(max_length=25)
    fio_user = models.CharField(max_length=60)
    address_user = models.CharField(max_length=60)
    age_user = models.PositiveSmallIntegerField(validators=
    [MaxValueValidator(100)]) #Валидация максимальный возврат 100 лет
    dateregister_user = models.DateField()

class State_applic(models.Model):
    id_state = models.AutoField(primary_key=True)
    name_state = models.CharField(max_length=20)

class Type_applic(models.Model):
    id_type = models.AutoField(primary_key=True)
    name_type = models.CharField(max_length=10)

class Manufacturer_applic(models.Model):
    id_manufacturer = models.AutoField(primary_key=True)
    name_manufacturer = models.CharField(max_length=40)

class Application(models.Model):
    id_application = models.AutoField(primary_key=True)
    id_user_applic = models.ForeignKey(User, on_delete=models.CASCADE) #Вторичный ключ Класс,Что при удолении
    id_state_applic = models.ForeignKey(State_applic, on_delete=models.CASCADE)  # f
    id_type_applic = models.ForeignKey(Type_applic, on_delete=models.CASCADE)
    id_manufacturer_applic = models.ForeignKey(Manufacturer_applic,on_delete=models.CASCADE)
    photo_applic = models.CharField(max_length=45)
    reason_applic = models.CharField(max_length=45)
    history_applic = models.CharField(max_length=45)
    model_applic = models.CharField(max_length=45)
    password_applic = models.CharField(max_length=45)
    other_applic = models.CharField(max_length=45)
    date_applic = models.DateField()
    #Null
    adresssamoviz_applic = models.CharField(max_length=45,blank=True,null=True)
    telmastersamoviz_applic = models.CharField(max_length=45,blank=True,null=True)
    fiomastersamoviz_applic = models.CharField(max_length=45,blank=True,null=True)
    verdict_applic = models.CharField(max_length=45,blank=True,null=True)
    descriptionprice_applic = models.CharField(max_length=45,blank=True,null=True)


class PriceList(models.Model):
    id_service = models.AutoField(primary_key=True)
    name_service = models.CharField(max_length=45)
    description_service = models.CharField(max_length=45)
    price_service = models.DecimalField(max_digits=10,decimal_places=2)

class Report(models.Model):
    id_Report = models.AutoField(primary_key=True)
    login = models.CharField(max_length=45)
    ip = models.CharField(max_length=45)
    device = models.CharField(max_length=45)
    action = models.CharField(max_length=45)
    date_action = models.DateTimeField()

class Feedbackcol_number(models.Model):
    id_feedbackcol_number = models.AutoField(primary_key=True)
    number = models.CharField(max_length=2) #!!!

class Feedback(models.Model):
    id_feedback = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_feedbackcol_number = models.ForeignKey(Feedbackcol_number,on_delete=models.CASCADE)
    description_service = models.CharField(max_length=45)

class Publications(models.Model):
    id_publ = models.AutoField(primary_key=True)
    id_worker_public = models.ForeignKey(Worker,on_delete=models.CASCADE)
    photo_publ = models.CharField(max_length=45)
    description_publ = models.CharField(max_length=45)
    source_public = models.CharField(max_length=45)

class Chat(models.Model):
    id_chat = models.AutoField(primary_key=True)
    master_chat = models.ForeignKey(Worker,on_delete=models.CASCADE)
    user_chat = models.ForeignKey(User,on_delete=models.CASCADE)
    date_chat = models.DateTimeField()
    message_chat = models.TextField()