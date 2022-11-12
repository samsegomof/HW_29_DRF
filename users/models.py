from django.db import models


class Location(models.Model):
    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"

    name = models.CharField(verbose_name="Местоположение", max_length=100)
    lat = models.DecimalField(verbose_name="Широта", max_digits=15, decimal_places=10, null=True)
    lng = models.DecimalField(verbose_name="Долгота", max_digits=15, decimal_places=10, null=True)

    def __str__(self):
        return self.name


class UserRoles:
    USER = "member"
    ADMIN = "admin"
    MODERATOR = "moderator"
    choices = (
        (USER, "Пользователь"),
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор")
    )


class User(models.Model):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['username']

    first_name = models.CharField(verbose_name="Имя", max_length=100)
    last_name = models.CharField(verbose_name="Фамилия", max_length=100)
    username = models.CharField(verbose_name="Никнейм", max_length=50, unique=True)
    password = models.CharField(verbose_name="Пароль", max_length=50)
    role = models.CharField(verbose_name="Группа", choices=UserRoles.choices, default="member", max_length=16)
    age = models.PositiveIntegerField(verbose_name="Возраст", null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Местоположение", null=True)

    def __str__(self):
        return self.username
