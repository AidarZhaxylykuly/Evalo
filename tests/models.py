from django.db import models
from django.contrib.postgres.fields import JSONField  

class Question(models.Model):
    content = models.TextField(verbose_name="Содержание вопроса")
    answer_list = models.JSONField(default=list, verbose_name="Варианты ответов")
    correct_answers = models.JSONField(default=list, verbose_name="Правильные ответы")
    points = models.FloatField(verbose_name="Очки за правильный ответ")

    def __str__(self):
        return self.content
