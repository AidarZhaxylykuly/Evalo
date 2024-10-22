from django import forms
from .models import Question
from .models import Test

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['content', 'answer_list', 'correct_answers', 'points']

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'author', 'question_list', 'total_points', 'has_timer', 
                  'starting_datetime', 'submission_datetime', 'is_private', 'entrance_code', 
                  'allowed_users', 'test_category', 'like']
