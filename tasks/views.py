from django.http import HttpResponse
from django.shortcuts import render, redirect
from tasks.models import TodoItem
from tasks.forms import TodoItemForm


def index(request):
    return HttpResponse("Simple answer from tasks app")


def complete_task(request, uid):
    task = TodoItem.objects.get(id=uid)
    task.is_completed = True
    task.save()
    return HttpResponse("OK")


def delete_task(request, uid):
    task = TodoItem.objects.get(id=uid)
    task.delete()
    return redirect("/tasks/list")


def create_task(request):
    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/tasks/list')
    else:
        form = TodoItemForm()
        
    return render(request, "tasks/create.html", {'form': form})


def tasks_list(request):
    all_tasks = TodoItem.objects.all()
    return render(
        request,
        'tasks/list.html',
        {'tasks' : all_tasks}
    )