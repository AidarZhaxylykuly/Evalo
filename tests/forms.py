from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['content', 'answer_list', 'correct_answers', 'points']
