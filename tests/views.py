import datetime

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone

from .models import Test, Question, Category, AnswerBlank
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

@login_required
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



@login_required
def show_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    return render(request, 'test/show.html', {'test': test})


@login_required
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


@login_required
def delete_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    test.delete()
    return redirect('some_view_after_delete')


@login_required
def add_user_to_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    user_id = request.POST.get('user_id')
    user = get_object_or_404(User, id=user_id)
    test.allowed_users.add(user)
    return JsonResponse({'status': 'success'})


@login_required
def delete_user_from_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    user_id = request.POST.get('user_id')
    user = get_object_or_404(User, id=user_id)
    test.allowed_users.remove(user)
    return JsonResponse({'status': 'success'})


#####################for AnswerBlank model(test passing)##############################

@login_required
def pass_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    return render(request, 'test_passing.html', {'test': test})


@login_required
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


@login_required
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


