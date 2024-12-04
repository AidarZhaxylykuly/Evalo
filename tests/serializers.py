from rest_framework import serializers
from .models import Test, AnswerBlank, Question, Category


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class AnswerBlankSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerBlank
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'