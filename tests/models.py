from django.db import models
from django.contrib.postgres.fields import JSONField  
from django.contrib.auth.models import User

class Question(models.Model):
    content = models.TextField(verbose_name="Содержание вопроса")
    answer_list = models.JSONField(default=list, verbose_name="Варианты ответов")
    correct_answers = models.JSONField(default=list, verbose_name="Правильные ответы")
    points = models.FloatField(verbose_name="Очки за правильный ответ")

    def __str__(self):
        return self.content

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории")

    def __str__(self):
        return self.name

class Test(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название теста")
    description = models.TextField(verbose_name="Описание теста")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tests", verbose_name="Автор теста")
    question_list = models.ManyToManyField(Question, verbose_name="Список вопросов")
    total_points = models.FloatField(verbose_name="Общее количество очков")
    has_timer = models.BooleanField(default=False, verbose_name="Наличие таймера")
    starting_datetime = models.DateTimeField(verbose_name="Дата и время начала теста")
    submission_datetime = models.DateTimeField(verbose_name="Дата и время сдачи теста")
    is_private = models.BooleanField(default=False, verbose_name="Приватный тест")
    entrance_code = models.IntegerField(verbose_name="Код для входа")
    allowed_users = models.ManyToManyField(User, related_name="allowed_tests", verbose_name="Разрешенные пользователи")
    test_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория теста")
    like = models.ManyToManyField(User, related_name="liked_tests", blank=True, verbose_name="Лайки")

    def __str__(self):
        return self.title
    
class AnswerBlank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    answers = models.JSONField(default=dict)
    score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'AnswerBlank for {self.user.username} on {self.test.title}'