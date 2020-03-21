from django.http import HttpResponse
from django.shortcuts import render
from tasks.models import TodoItem


def index(request):
    return HttpResponse("Simple answer from tasks app")


def tasks_list(request):
    all_tasks = TodoItem.objects.all()
    return render(
        request,
        'tasks/list.html',
        {'tasks' : all_tasks}
    )