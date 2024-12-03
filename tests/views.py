import datetime

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone

from .models import Test, Question, Category, AnswerBlank
from django.contrib.auth.decorators import login_required

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

def home(request):
    return render(request, 'home.html')

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@login_required
@swagger_auto_schema(
    operation_summary="Создание теста",
    operation_description="Создаёт новый тест с категориями, вопросами и ответами.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='Название теста'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Описание теста'),
            'starting_datetime': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Дата и время начала теста'),
            'submission_datetime': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Дата и время окончания теста'),
            'is_private': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Приватный тест или нет'),
            'entrance_code': openapi.Schema(type=openapi.TYPE_STRING, description='Код доступа для приватного теста'),
            'test_category': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID категории теста'),
            'questions': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'content': openapi.Schema(type=openapi.TYPE_STRING, description='Содержание вопроса'),
                        'points': openapi.Schema(type=openapi.TYPE_NUMBER, description='Баллы за вопрос'),
                        'answers': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'answer': openapi.Schema(type=openapi.TYPE_STRING, description='Вариант ответа'),
                                    'is_correct': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Правильный ответ или нет')
                                }
                            )
                        )
                    }
                )
            )
        },
        required=['title', 'description', 'starting_datetime', 'submission_datetime', 'test_category']
    ),
    responses={
        302: "Перенаправление на страницу теста после успешного создания",
        400: "Ошибка валидации данных"
    }
)
def create_test(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        starting_datetime = request.POST.get('starting_datetime')
        submission_datetime = request.POST.get('submission_datetime')
        is_private = request.POST.get('is_private') == 'on'
        entrance_code = request.POST.get('entrance_code')

        test_category_id = request.POST.get('test_category')
        test_category = Category.objects.get(id=test_category_id)

        starting_datetime = timezone.make_aware(datetime.datetime.fromisoformat(starting_datetime))
        submission_datetime = timezone.make_aware(datetime.datetime.fromisoformat(submission_datetime))

        test = Test.objects.create(
            title=title,
            description=description,
            total_points=0,
            starting_datetime=starting_datetime,
            submission_datetime=submission_datetime,
            is_private=is_private,
            entrance_code=entrance_code,
            author=request.user,
            test_category=test_category
        )

        question_index = 0
        total_points = 0
        while f'question_{question_index}_content' in request.POST:
            question_content = request.POST.get(f'question_{question_index}_content')
            question_points = float(request.POST.get(f'question_{question_index}_points', 0))

            question = Question.objects.create(
                content=question_content,
                points=question_points
            )

            answer_index = 0
            answer_list = []
            correct_answers = []
            while f'question_{question_index}_answer_{answer_index}' in request.POST:
                answer = request.POST.get(f'question_{question_index}_answer_{answer_index}')
                is_correct = f'question_{question_index}_correct_answer_{answer_index}' in request.POST

                answer_list.append(answer)
                if is_correct:
                    correct_answers.append(answer)

                answer_index += 1

            question.answer_list = answer_list
            question.correct_answers = correct_answers
            question.save()

            test.question_list.add(question)

            total_points += question_points

            question_index += 1

        test.total_points = total_points
        test.save()

        return redirect('test_detail', test.id)

    return render(request, 'test_form.html', {'categories': categories})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@login_required
@swagger_auto_schema(
    operation_summary="Просмотр теста",
    operation_description="Просматривает информацию о тесте по его ID.",
    responses={
        200: "Страница теста с подробной информацией",
        404: "Тест не найден"
    }
)
def show_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    return render(request, 'test/show.html', {'test': test})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@login_required
@swagger_auto_schema(
    operation_summary="Редактирование теста",
    operation_description="Редактирует существующий тест по его ID.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='Название теста'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Описание теста'),
            'starting_datetime': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Дата и время начала теста'),
            'submission_datetime': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Дата и время окончания теста'),
            'is_private': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Приватный тест или нет'),
            'entrance_code': openapi.Schema(type=openapi.TYPE_STRING, description='Код доступа для приватного теста'),
        },
        required=['title', 'description', 'starting_datetime', 'submission_datetime']
    ),
    responses={
        302: "Перенаправление на страницу теста после успешного редактирования",
        404: "Тест не найден"
    }
)
def edit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)

    if request.method == 'POST':
        test.title = request.POST.get('title')
        test.description = request.POST.get('description')
        test.total_points = float(request.POST.get('total_points', 0))
        test.starting_datetime = request.POST.get('starting_datetime')
        test.submission_datetime = request.POST.get('submission_datetime')
        test.is_private = request.POST.get('is_private') == 'on'
        test.entrance_code = request.POST.get('entrance_code')
        test.save()

        return redirect('test_detail', test.id)

    return render(request, 'test_form.html', {'test': test})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@login_required
@swagger_auto_schema(
    operation_summary="Удаление теста",
    operation_description="Удаляет тест по его ID.",
    responses={
        302: "Перенаправление после успешного удаления",
        404: "Тест не найден"
    }
)
def delete_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    test.delete()
    return redirect('some_view_after_delete')

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@login_required
@swagger_auto_schema(
    operation_summary="Добавление пользователя к тесту",
    operation_description="Добавляет пользователя к списку пользователей, которые могут проходить тест.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID пользователя'),
        },
        required=['user_id']
    ),
    responses={
        200: "Пользователь успешно добавлен",
        404: "Тест или пользователь не найдены"
    }
)
def add_user_to_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    user_id = request.POST.get('user_id')
    user = get_object_or_404(User, id=user_id)
    test.allowed_users.add(user)
    return JsonResponse({'status': 'success'})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@login_required
@swagger_auto_schema(
    operation_summary="Удаление пользователя из теста",
    operation_description="Удаляет пользователя из списка пользователей, которые могут проходить тест.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID пользователя'),
        },
        required=['user_id']
    ),
    responses={
        200: "Пользователь успешно удалён",
        404: "Тест или пользователь не найдены"
    }
)
def delete_user_from_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    user_id = request.POST.get('user_id')
    user = get_object_or_404(User, id=user_id)
    test.allowed_users.remove(user)
    return JsonResponse({'status': 'success'})


#####################for AnswerBlank model(test passing)##############################
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@login_required
@swagger_auto_schema(
    operation_summary="Прохождение теста",
    operation_description="Возвращает страницу прохождения теста.",
    responses={
        200: "Страница прохождения теста",
        404: "Тест не найден"
    }
)
def pass_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    return render(request, 'test_passing.html', {'test': test})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@login_required
@swagger_auto_schema(
    operation_summary="Отправка результатов теста",
    operation_description="Отправляет результаты прохождения теста и вычисляет баллы пользователя.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'answers': openapi.Schema(type=openapi.TYPE_OBJECT, description='Ответы пользователя по вопросам теста')
        },
        required=['answers']
    ),
    responses={
        302: "Перенаправление на страницу с результатами теста после успешной отправки",
        400: "Ошибка в запросе"
    }
)
def submit_test(request, test_id):
    if request.method == 'POST':
        test = get_object_or_404(Test, id=test_id)
        user_answers = {}
        total_score = 0

        for question in test.question_list.all():
            question_id = str(question.id)
            user_answers[question_id] = request.POST.getlist(f'answers_{question_id}[]')

            correct_answers = question.correct_answers
            question_points = question.points
            if set(user_answers[question_id]) == set(correct_answers):
                total_score += question_points

        AnswerBlank.objects.create(
            User=request.user,
            Test=test,
            Answers=user_answers,
            Score=total_score
        )

        return redirect('test_result', test_id=test.id)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@login_required
@swagger_auto_schema(
    operation_summary="Просмотр результата теста",
    operation_description="Просматривает результаты прохождения теста пользователем или автором теста.",
    responses={
        200: "Страница с результатами теста",
        404: "Тест не найден"
    }
)
def test_result(request, test_id):
    test = Test.objects.get(id=test_id)

    is_author = test.author == request.user

    if not is_author:
        answer_blank = AnswerBlank.objects.filter(User=request.user, Test=test).last()
        if not answer_blank:
            return redirect('test_list')

        percentage = (answer_blank.score / test.total_points) * 100
        return render(request, 'test_result_user.html', {
            'answer_blank': answer_blank,
            'test': test,
            'percentage': percentage
        })

    else:
        answer_blanks = AnswerBlank.objects.filter(Test=test)
        result_data = []

        for answer_blank in answer_blanks:
            percentage = (answer_blank.Score / test.total_points) * 100
            result_data.append({
                'user': answer_blank.User,
                'score': answer_blank.Score,
                'total_points': test.total_points,
                'percentage': percentage,
                'timestamp': answer_blank.Timestamp,
                'answers': answer_blank.Answers
            })

        return render(request, 'test_result_author.html', {
            'result_data': result_data,
            'test': test
        })
