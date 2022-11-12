from django.db import models

from users.models import User


class Category(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    name = models.CharField(verbose_name="Название категории", max_length=100, unique=True)

    def __str__(self):
        return self.name


class Ad(models.Model):
    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    name = models.CharField(verbose_name="Название объявления", max_length=100, unique=True)
    author = models.ForeignKey(User, verbose_name="Автор", null=True, on_delete=models.CASCADE, related_name="ads")
    price = models.PositiveIntegerField(verbose_name="Цена", null=True)
    description = models.TextField(max_length=2000, null=True)
    is_published = models.BooleanField(verbose_name="Объявление размещено?", default=False)
    image = models.ImageField(verbose_name="Изображение", upload_to="images/",  null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name="Категория", null=True, on_delete=models.CASCADE, related_name="ads")

    def __str__(self):
        return self.name
