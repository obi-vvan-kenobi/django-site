from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from isbn_field import ISBNField
from phonenumber_field.modelfields import PhoneNumberField
from autoslug import AutoSlugField


class Categories(models.Model):
    name = models.CharField(max_length=30, verbose_name='Категория')
    slug = models.SlugField(max_length=50, unique=True, db_index=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('sub_cat', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SubCategories(models.Model):
    name = models.CharField(max_length=255, verbose_name='Подкатегория')
    cat = models.ForeignKey('Categories', related_name='subcat', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('books', kwargs={'cat_slug': self.cat.slug, 'sub_cat_name': self.name})
    

class Authors(models.Model):
    name = models.CharField(max_length=255, verbose_name='Автор')

    def __str__(self):
        return self.name


class Book(models.Model):
    STATUS_CHOICES = (
        ('PUBLISH', 'Опубликовано'),
        ('MEAP', 'MEAP'),
    )
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    isbn = ISBNField(max_length=255, null=True, blank=True, verbose_name='ISBN')
    page_count = models.IntegerField(verbose_name='Количество страниц')
    time_publish = models.DateTimeField(null=True, blank=True)
    thumbnail_url = models.URLField(max_length=200, null=True, blank=True, verbose_name='Адрес обложки книги')
    photo_url = models.ImageField(upload_to="media/", null=True)
    short_description = models.CharField(max_length=5000, null=True, blank=True, verbose_name='Краткое описание')
    long_description = models.CharField(max_length=5000, null=True, blank=True, verbose_name='Полное описание')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PUBLISH', verbose_name='Статус')
    cat = models.ForeignKey('Categories', on_delete=models.PROTECT)
    sub_cat = models.ManyToManyField(SubCategories, blank=True)
    author = models.ManyToManyField(Authors)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Books'
        ordering = ['time_publish', 'title']


class ContactMessages(models.Model):
    message = models.TextField(verbose_name='Сообщение')
    contact = models.ForeignKey('Contact', on_delete=models.PROTECT)


class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    email = models.EmailField()
    telephone_number = PhoneNumberField(region='RU', verbose_name='Телефон')

    def __str__(self):
        return self.name
