from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import  models

class UserManager(BaseUserManager):

    # Определение метода password=None в create_user означает,
    # что None -это значение по умолчанию для пароля
    # , но оно все равно может быть предоставлено вызывающим.
    def create_user(self,email,password=None):
        # если нет почты , то вызывовится исключение ('Email непременно должен быть указан')
        if not email:
            raise ValueError('Email непременно должен быть указан')
        # Атрибут model менеджера моделей-это просто
        # ссылка на класс модели, для которого был создан менеджер.
        # В этом случае он относится к любой пользовательской модели,
        # которая будет использовать этот менеджер.
        user=self.model(
            email=UserManager.normalize_email(email),
        )
        # отвечает за хеширование пароля
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        # создаем точку входа суперпользователя по email и password
        user=self.create_user(email, password)
        # пользователь по умолчанию админ
        user.is_admin=True
        user.save(using=self._db)
        return user


# db_index=True-используется для ускорения поиска по данным.
# Если очень приблизительно - индексы сортируют ваши данные по тому полю,
# для которого вы укажете db_index=True, а искать по сортированным данным
# получается быстрее, нежели простым перебором всего подряд.
# Указывайте этот параметр, чтобы создать индекс для поля,
# по которому вы совершаете поисковые запросы.


class User(AbstractUser, PermissionsMixin):

    email = models.EmailField(
        'Электронная почта',
        max_length=255,
        # unique-используется для обозначения уникальности значения
        unique=True,
        # db_index=True-используется для ускорения поиска по данным.
        # Если очень приблизительно - индексы сортируют ваши данные по тому полю,
        # для которого вы укажете db_index=True, а искать по сортированным данным
        # получается быстрее, нежели простым перебором всего подряд.
        # Указывайте этот параметр, чтобы создать индекс для поля,
        # по которому вы совершаете поисковые запросы.
        db_index=True
    )
    avatar=models.ImageField(
        'Аватар',
        # поле может быть пустым
        # blank=True определяет, потребуется ли поле в формах.
        # Сюда входят администратор и собственные пользовательские формы.
        # Если blank=True, тогда поле не потребуется,
        # тогда как если оно False, поле не может быть пустым.
        blank=True,
        # пустые значения будут сохранены как NULL
        null=True,
    )
    first_name = models.CharField(
        'Фамилия',
        max_length=100,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        'Имя',
        max_length=100,
        null=True,
        blank=True
    )
    middle_name = models.CharField(
        'Отчество',
        max_length=100,
        null=True,
        blank=True
    )
    date__birth=models.DateField(
        'Дата рождения',
        null=True,
        blank=True
    )
    register_date=models.DateField(
        'Дата регистрации',
        auto_now_add=True
    )
    is_active = models.BooleanField(
        'Активен',
        default=True
    )
    is_admin=models.BooleanField(
        'Суперпользователь',
        default=False
    )

    def get_full_name(self):
        return self.email

    # требуется для админки
    def is_staff(self):
        return self.is_admin

    def get_shot_name(self):
        return self.email

    def __str__(self):
        return self.email

    #
    # Согласно документам , USERNAME_FIELD это:
    # Строка, описывающая имя поля в пользовательской модели,
    # которое используется в качестве уникального идентификатора.
    # Обычно это будет какое-то имя пользователя, но это также
    # может быть адрес электронной почты или любой другой уникальный идентификатор.
    # Поле должно быть уникальным (т. Е. Иметь в своем определении значение unique = True),
    # если только вы не используете пользовательский сервер аутентификации,
    # который может поддерживать неуникальные имена пользователей.
    # Итак, USERNAME_FIELDуказывает, какое поле модели будет использоваться
    # в качестве имени пользователя. Если ваше приложение использует адрес электронной почты
    # вместо имени пользователя, вы можете настроить его, используя USERNAME_FIELD.

    USERNAME_FIELD = 'email'

