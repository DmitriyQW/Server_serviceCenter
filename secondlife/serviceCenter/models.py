from django.db import models
from django.core.validators import MaxValueValidator #Валидация
from django.utils import timezone
from django.contrib.auth.hashers import make_password #Хеширования пароля


#Определение моделей - они же таблицы, поля, связи
class Worker(models.Model):
    id_worker = models.AutoField(primary_key=True)
    login_worker = models.CharField(max_length=32)
    tel_worker = models.CharField(max_length=11)
    email_worker = models.EmailField(max_length=254)
    password_worker = models.CharField(max_length=255) #HES
    question_worker = models.CharField(max_length=100)
    answer_worker = models.CharField(max_length=255)
    fio_worker = models.CharField(max_length=110)
    address_worker = models.CharField(max_length=256)
    age_worker = models.PositiveSmallIntegerField(validators=
    [MaxValueValidator(100)]) #Валидация максимальный возврат 100 лет
    dateregister_worker = models.DateTimeField(default=timezone.now)

    # Определение функции вывода информации строки
    def __str__(self):
        return f"{self.id_worker} ({self.fio_worker})" # Возвращение id и Фио мастера

class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    login_user = models.CharField(max_length=32)
    tel_user = models.CharField(max_length=11)
    email_user = models.EmailField(max_length=254)
    password_user = models.CharField(max_length=255) #HES
    question_user = models.CharField(max_length=100)
    answer_user = models.CharField(max_length=255) #HES
    fio_user = models.CharField(max_length=110)
    address_user = models.CharField(max_length=256)#
    age_user = models.PositiveSmallIntegerField(validators=
    [MaxValueValidator(100)]) #Валидация максимальный возврат 100 лет
    dateregister_user = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id_user}({self.fio_user})"

class State_applic(models.Model):
    id_state = models.AutoField(primary_key=True)
    name_state = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id_state}({self.name_state})"

class TypeDevice_applic(models.Model):
    id_typeD = models.AutoField(primary_key=True)
    name_typeD = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id_typeD}({self.name_typeD})"

class Manufacturer_applic(models.Model):
    id_manufacturer = models.AutoField(primary_key=True)
    name_manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id_manufacturer}({self.name_manufacturer})"

class Application(models.Model):
    id_application = models.AutoField(primary_key=True)
    id_state_applic = models.ForeignKey(State_applic, on_delete=models.PROTECT)  # Статус заявки (Готово)
    id_user_applic = models.ForeignKey(User, on_delete=models.PROTECT)
    id_worker_applic = models.ForeignKey(Worker, on_delete=models.PROTECT, blank=True, null=True) # NULL
    photo_applic = models.CharField(max_length=200)
    id_typeDevice_applic = models.ForeignKey(TypeDevice_applic, on_delete=models.PROTECT)  # Тип устройства (Планшет)
    id_manufacturer_applic = models.ForeignKey(Manufacturer_applic, on_delete=models.PROTECT)
    model_applic = models.CharField(max_length=100)
    reason_applic = models.CharField(max_length=250)
    history_applic = models.CharField(max_length=500)
    passwordDevice_applic = models.CharField(max_length=256)
    otherInfo_applic = models.CharField(max_length=1000)
    date_applic = models.DateTimeField(default=timezone.now)

    deviceStatus_applic = models.CharField(max_length=1000)# Состояние Устройства (Рабочий, Не рабочий,скол и т.п)
    adresssamoviz_applic = models.CharField(max_length=256,blank=True,null=True) #Null
    telmastersamoviz_applic = models.CharField(max_length=11,blank=True,null=True) #Null
    fiomastersamoviz_applic = models.CharField(max_length=110,blank=True,null=True) #Null
    #Дефект пользователя reason_applic
    descriptionWorks_applic = models.CharField(max_length=2000, blank=True, null=True) #Null
    verdictPrice_applic = models.CharField(max_length=2000,blank=True,null=True) #Null

    def __str__(self):
        return f"{self.id_application}({self.date_applic}({self.id_state_applic}({self.id_user_applic})({self.reason_applic})))"

class PriceList(models.Model):
    id_service = models.AutoField(primary_key=True)
    name_service = models.CharField(max_length=100)
    description_service = models.CharField(max_length=500)
    price_service = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
            return f"{self.id_service}({self.name_service})({self.price_service})"
class Report(models.Model):
    id_Report = models.AutoField(primary_key=True)
    login = models.CharField(max_length=32)
    ip = models.CharField(max_length=20)
    device = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    date_action = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id_Report}({self.login}({self.action}({self.date_action})))"

class Feedbackcol_number(models.Model):
    id_feedbackcol_number = models.AutoField(primary_key=True)
    number = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.id_feedbackcol_number}({self.number})"

class Feedback(models.Model): #Пересмотреть добавление id_applic
    id_feedback = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User,on_delete=models.PROTECT)
    id_feedbackcol_number = models.ForeignKey(Feedbackcol_number,on_delete=models.PROTECT)
    description_service = models.CharField(max_length=500)
    date_feedback = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id_feedback}({self.date_feedback})({self.id_user})({self.date_feedback})({self.id_feedbackcol_number})"

class Publications(models.Model):
    id_publ = models.AutoField(primary_key=True)
    id_worker_public = models.ForeignKey(Worker,on_delete=models.PROTECT)
    photo_publ = models.CharField(max_length=200)
    description_publ = models.CharField(max_length=100)
    source_public = models.CharField(max_length=1000)
    date_public = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id_publ}({self.date_public})({self.description_publ})({self.source_public})({self.id_worker_public})"

class Chat(models.Model):
    id_chat = models.AutoField(primary_key=True)
    master_chat = models.ForeignKey(Worker,on_delete=models.PROTECT)
    user_chat = models.ForeignKey(User,on_delete=models.PROTECT)
    date_chat = models.DateTimeField(default=timezone.now)
    message_chat = models.TextField()

    def __str__(self):
        return f"{self.id_chat}({self.date_chat})({self.user_chat})({self.master_chat})({self.master_chat})"