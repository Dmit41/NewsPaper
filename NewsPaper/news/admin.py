from django.contrib import admin
from .models import Post, Category
from modeltranslation.admin import TranslationAdmin  # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)

# Регистрируем модели для перевода в админке


class CategoryAdmin(TranslationAdmin):
    model = Category


class MyModelAdmin(TranslationAdmin):
    model = Post


admin.site.register(Post)
admin.site.register(Category)