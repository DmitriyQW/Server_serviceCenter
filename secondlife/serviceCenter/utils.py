from django.contrib.auth.hashers import make_password, check_password

def normalize_input(input_string):
    #Нормализация ввода:
    return " ".join(input_string.split())

def hash_password(raw_password):
    #Хеширование пароля
    normalized_password = raw_password.replace(" ", "")
    return make_password(normalized_password)

def hash_answer(raw_answer):
    #Хеширование контрольного ответа
    normalized_answer = normalize_input(raw_answer)
    return make_password(normalized_answer)

class UserUtils:
    @staticmethod
    def format_username(username):
        """
        Возвращает имя пользователя в нижнем регистре и без пробелов.
        """
        return username.lower().replace(" ", "")