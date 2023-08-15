from django.contrib import admin
from .models import (
    Book,
    Categories,
    SubCategories,
    ContactMessages, Contact,
)


class SubCategoriesInline(admin.TabularInline):
    model = SubCategories
    extra = 0


class ContactMessageInline(admin.TabularInline):
    model = ContactMessages
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = "time_publish"
    empty_value_display = "-empty-"
    filter_horizontal = ['sub_cat', 'author']


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    inlines = [SubCategoriesInline]
    list_display = ('name', 'slug', 'sub_cat')
    readonly_fields = ['slug']

    def sub_cat(self, obj):
        return [i['name'] for i in obj.subcat.all().values('name')]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    inlines = [ContactMessageInline]
