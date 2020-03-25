from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView


from tasks.models import TodoItem
from tasks.forms import TodoItemForm


@login_required
def index(request):
    return HttpResponse("Simple answer from tasks app")


def complete_task(request, uid):
    task = TodoItem.objects.get(id=uid)
    task.is_completed = True
    task.save()
    return HttpResponse("OK")


def delete_task(request, uid):
    try:
        task = TodoItem.objects.get(id=uid)
        task.delete()
    except:
        pass
    return redirect(reverse("tasks:list"))


class TaskListView(LoginRequiredMixin, ListView):
    model=TodoItem
    context_object_name = 'tasks'
    template_name = 'tasks/list.html'


    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return []
        return user.tasks.all()


class TaskCreateView(View):
    def my_render(self, request, form):
        return render(request, 'tasks/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TodoItemForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            return redirect(reverse("tasks:list"))

        return self.my_render(request, form)


    def get(self, request, *args, **kwargs):
        form = TodoItemForm()
        return self.my_render(request, form)


class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = 'tasks/details.html'