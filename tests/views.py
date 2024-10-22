from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from .forms import QuestionForm
from .models import Test
from .forms import TestForm
from django.contrib.auth.decorators import login_required

# Создание нового вопроса
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_question', pk=form.instance.pk)
    else:
        form = QuestionForm()
    return render(request, 'question/create.html', {'form': form})

# Редактирование вопроса
def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('show_question', pk=pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'question/edit.html', {'form': form})

# Отображение вопроса
def show_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'question/show.html', {'question': question})



# Отображение теста
def show_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    return render(request, 'test/show.html', {'test': test})

# Создание нового теста
@login_required
def create_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show', pk=form.instance.pk)
    else:
        form = TestForm()
    return render(request, 'test/create.html', {'form': form})

# Редактирование теста
@login_required
def edit_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if request.method == 'POST':
        form = TestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return redirect('show', pk=pk)
    else:
        form = TestForm(instance=test)
    return render(request, 'test/edit.html', {'form': form})
