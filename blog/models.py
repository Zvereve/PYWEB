from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Note(models.Model):

    class Ratings(models.IntegerChoices):
        ACTIVE = 0, _('Активно')
        POSTPON = 1, _('Отложено')
        COMPl = 3, _('Выполнено')

    title = models.CharField(max_length=255, verbose_name="Дела")
    message = models.TextField(default='', verbose_name="Текст")
    public = models.BooleanField(default=True, verbose_name="Опубликован")
    date_add = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    date_up = models.DateTimeField(auto_now=True, verbose_name="время обновления")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    relevant = models.BooleanField(default=False, verbose_name="Важность")
    rating = models.IntegerField(default=Ratings.ACTIVE, choices=Ratings.choices, verbose_name='Статус')

    def __str__(self):
        return f"Дело №{self.id}"

    class Meta:
        verbose_name = _("дело")
        verbose_name_plural = _("список дел")


class Comment(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)  #
    comment = models.TextField(default='', verbose_name='Коментарий')

    def __str__(self):
        return f'{self.author}'
    class Meta:
        verbose_name = _("Коментарий")
        verbose_name_plural = _("Коментарии")