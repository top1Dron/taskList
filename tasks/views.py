from django.http import HttpResponse
from django.shortcuts import render, redirect
from tasks.models import TodoItem


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

def tasks_list(request):
    all_tasks = TodoItem.objects.all()
    return render(
        request,
        'tasks/list.html',
        {'tasks' : all_tasks}
    )