from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class ToDoListObject(models.Model):
    title = models.CharField(max_length=120, db_index=True, verbose_name='Задача')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    is_done = models.BooleanField(default=False, verbose_name='Завершено')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель')

    def get_absolute_url(self):
        return reverse('detail', kwargs={"pk":self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at', 'title']

class Category(models.Model):
    title = models.CharField(max_length=80, db_index=True, verbose_name='Категория')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self):
        return self.title

class Point(models.Model):
    title = models.CharField(max_length=80, verbose_name='Подзадача')
    main = models.ForeignKey('ToDoListObject', on_delete=models.CASCADE, verbose_name='Подзадача для')
    is_completed = models.BooleanField(default=False, verbose_name='Выполнено')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель подзадачи')

    class Meta:
        verbose_name = 'Подзадача'
        verbose_name_plural = 'Подзадачи'

    def __str__(self):
        return self.title