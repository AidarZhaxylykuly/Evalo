from django.contrib import admin
from .models import Question, Category, Test


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['content', 'points']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title']