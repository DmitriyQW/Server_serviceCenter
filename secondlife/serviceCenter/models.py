from django.db import models
from django.core.validators import MaxValueValidator #Валидация
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password  # Хеширования пароля
from .utils import  UserUtils #Hes


#Определение моделей - они же таблицы, поля, связи, значения по умолчанию (дата)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('master', 'Мастер'),
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
    )

    # Поля для всех типов пользователей
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    tel = models.CharField(max_length=11, blank=True, null=True)
    fio = models.CharField(max_length=110)
    address = models.CharField(max_length=256, blank=True, null=True)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)], blank=True, null=True)
    dateregister = models.DateTimeField(default=timezone.now)

    # Поля для мастеров и пользователей
    question = models.CharField(max_length=100, blank=True, null=True)
    answer = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Хеширование пароля и ответа при сохранении
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)

        if self.answer and not self.answer.startswith('pbkdf2_'):
            self.answer = make_password(self.answer)

        super().save(*args, **kwargs)

    def check_answer(self, raw_answer):
        """Проверка контрольного ответа"""
        return check_password(raw_answer, self.answer)

    def __str__(self):
        # Используем утилиту для форматирования имени пользователя
        return UserUtils.format_username(self.username)


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
    id_application = models.AutoField(primary_key=True) #id
    id_state_applic = models.ForeignKey(State_applic, on_delete=models.PROTECT)  # Статус заявки (Готово)
    id_user_applic = models.ForeignKey(CustomUser, on_delete=models.PROTECT,related_name= "user_applic") #id user
    id_worker_applic = models.ForeignKey(CustomUser, on_delete=models.PROTECT, blank=True, null=True,related_name= "worker_applic") # NULL id worker
    photo_applic = models.CharField(max_length=200) # no
    id_typeDevice_applic = models.ForeignKey(TypeDevice_applic, on_delete=models.PROTECT)  # Тип устройства (Планшет)
    id_manufacturer_applic = models.ForeignKey(Manufacturer_applic, on_delete=models.PROTECT) # Производитель
    model_applic = models.CharField(max_length=100) # Модель
    reason_applic = models.CharField(max_length=250) # Причина обращения
    history_applic = models.CharField(max_length=500) # Пред история
    passwordDevice_applic = models.CharField(max_length=256) #Пароль от устройства
    otherInfo_applic = models.CharField(max_length=1000) #Полезная информация

    date_applic = models.DateTimeField(default=timezone.now) #Дата создания заявки

    deviceStatus_applic = models.CharField(max_length=1000)# Состояние Устройства (Рабочий, Не рабочий,скол и т.п)

    adresssamoviz_applic = models.CharField(max_length=256,blank=True,null=True) #Null Адресс для забора устройства
    telmastersamoviz_applic = models.CharField(max_length=11,blank=True,null=True) #Null Телефон мастера
    fiomastersamoviz_applic = models.CharField(max_length=110,blank=True,null=True) #Null Фио мастера


    descriptionWorks_applic = models.CharField(max_length=2000, blank=True, null=True)  # Null Дефект реальный
    verdictPrice_applic = models.CharField(max_length=2000,blank=True,null=True) #Null Стоимость работ

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
    id_user = models.ForeignKey(CustomUser,on_delete=models.PROTECT,related_name= "feedbackcol_user")
    id_feedbackcol_number = models.ForeignKey(Feedbackcol_number,on_delete=models.PROTECT)
    description_service = models.CharField(max_length=500)
    date_feedback = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id_feedback}({self.date_feedback})({self.id_user})({self.id_feedbackcol_number})"

class Publications(models.Model):
    id_publ = models.AutoField(primary_key=True)
    id_worker_public = models.ForeignKey(CustomUser,on_delete=models.PROTECT,related_name= "public_worker")
    photo_publ = models.CharField(max_length=200)
    description_publ = models.CharField(max_length=100)
    source_public = models.CharField(max_length=1000)
    date_public = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id_publ}({self.date_public})({self.description_publ})({self.source_public})({self.id_worker_public})"

class Chat(models.Model):
    id_chat = models.AutoField(primary_key=True)
    worker_chat = models.ForeignKey(CustomUser,on_delete=models.PROTECT,related_name= "chat_worker")
    user_chat = models.ForeignKey(CustomUser,on_delete=models.PROTECT,related_name= "chat_user")
    date_chat = models.DateTimeField(default=timezone.now)
    message_chat = models.TextField()

    def __str__(self):
        return f"{self.id_chat}({self.date_chat})({self.user_chat})({self.worker_chat})"