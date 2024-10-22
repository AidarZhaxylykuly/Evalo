from django.contrib import admin
from .models import Question, Category, Test

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['content', 'points']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'test_category', 'total_points', 'is_private']
    list_filter = ['is_private', 'test_category', 'has_timer']
    search_fields = ['title', 'author__username']
    filter_horizontal = ['question_list', 'allowed_users', 'like']