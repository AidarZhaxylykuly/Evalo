from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from .forms import QuestionForm

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
