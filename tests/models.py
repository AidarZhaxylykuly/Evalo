from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    content = models.TextField()
    answer_list = models.JSONField(default=list)
    correct_answers = models.JSONField(default=list)
    points = models.FloatField()

    def __str__(self):
        return self.content


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Test(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    question_list = models.ManyToManyField(
        Question)
    total_points = models.FloatField()
    has_timer = models.BooleanField(default=False)
    starting_datetime = models.DateTimeField(blank=True)
    submission_datetime = models.DateTimeField(blank=True)
    is_private = models.BooleanField(default=False)
    entrance_code = models.IntegerField()
    allowed_users = models.ManyToManyField(
        User,
        related_name="allowed_tests")
    test_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True)
    like = models.ManyToManyField(
        User,
        related_name="liked_tests",
        blank=True)

    def is_user_allowed(self, user):
        return self.allowed_users.filter(id=user.id).exists()

    def __str__(self):
        return self.title


class AnswerBlank(models.Model):
    User = models.ForeignKey(
        User,
        related_name="blank_user",
        on_delete=models.CASCADE,
    )
    Test = models.ForeignKey(
        Test,
        related_name="blank_test",
        on_delete=models.CASCADE
    )
    Answers = models.JSONField(default=dict)
    Score = models.FloatField()
    Timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "AnswerBlank"
        verbose_name_plural = "AnswerBlanks"

    def __str__(self):
        return f'id: {self.id}, user: {self.User}, test: {self.Test}, answers: {self.Answers}, score: {self.Score}, time: {self.Timestamp}'