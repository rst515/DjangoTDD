from django.shortcuts import render, redirect

from .forms import NewTaskForm, UpdateTaskForm
from .models import Task


def index(request):
    tasks = Task.objects.all()

    context = {'tasks': tasks}

    return render(request, 'task/index.html', context=context)


def detail(request, pk):
    task = Task.objects.get(pk=pk)

    context = {'task': task}

    return render(request, 'task/detail.html', context=context)


def new(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/')
    else:
        form = NewTaskForm()

    context = {'form': form}

    return render(request, 'task/new.html', context=context)


def update(request, pk):
    task = Task.objects.get(pk=pk)

    if request.method == 'POST':
        form = UpdateTaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()

            return redirect('/')
    else:
        form = UpdateTaskForm(instance=task)

    context = {
        'task': task,
        'form': form,
    }

    return render(request, 'task/update.html', context=context)


def delete(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()

    return redirect('/')
