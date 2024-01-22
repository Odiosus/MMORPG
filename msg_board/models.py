from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from froala_editor.fields import FroalaField
from django.urls import reverse
from django.utils import timezone
import datetime


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=True, verbose_name='Категория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('post_category', args=[str(self.pk)])


class Post(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        default=1,
        on_delete=models.CASCADE,
        verbose_name='Автор объявления',
    )
    heading = models.CharField(max_length=250, verbose_name='Заголовок')
    content = FroalaField(verbose_name='Контент')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return f'{self.heading.title()}: {self.content[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Comment(models.Model):
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE, verbose_name='Автор комментария')
    text = models.TextField(verbose_name='Текст комментария')
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Комментарий')
    date_comment = models.DateTimeField(auto_now_add=True, verbose_name='Дата комментария')
    confirm = models.BooleanField(default=False, verbose_name='Подтвердить')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author} {self.text} {self.post_comment}'

    def get_absolute_url(self):
        return reverse('comment_detail', args=[str(self.pk)])


class NewsForSubscribers(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = FroalaField(verbose_name='Текст статьи', blank=True, null=True)
    draft = models.BooleanField(verbose_name='Статус', default=True)

    class Meta:
        verbose_name = 'Рассылка новостей подписчикам'
        verbose_name_plural = 'Рассылка новостей подписчикам'

    def __str__(self):
        return f'{self.title}'


class SubscriberNews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Новостные подписчики')
    news = models.ForeignKey(NewsForSubscribers, on_delete=models.CASCADE, verbose_name='Новость')

    class Meta:
        verbose_name = 'Новостные подписчики'
        verbose_name_plural = 'Новостные подписчики'
