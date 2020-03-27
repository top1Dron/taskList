from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView


from tasks.forms import TodoItemForm, TodoItemExportForm
from tasks.models import TodoItem


@login_required
def index(request):
    return HttpResponse("Simple answer from tasks app")


def complete_task(request, uid):
    task = TodoItem.objects.get(id=uid)
    task.is_completed = True
    task.save()
    messages.warning(request, 'Tak completed')
    return HttpResponse("OK")


def delete_task(request, uid):
    try:
        task = TodoItem.objects.get(id=uid)
        task.delete()
        messages.success(request, 'Task removed')
    except:
        pass
    return redirect(reverse("tasks:list"))


class TaskListView(LoginRequiredMixin, ListView):
    model=TodoItem
    context_object_name = 'tasks'
    template_name = 'tasks/list.html'


    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(owner=user)


class TaskCreateView(View):
    def my_render(self, request, form):
        return render(request, 'tasks/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TodoItemForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            messages.info(request, 'Task created')
            return redirect(reverse("tasks:list"))

        return self.my_render(request, form)


    def get(self, request, *args, **kwargs):
        form = TodoItemForm()
        return self.my_render(request, form)


class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = 'tasks/details.html'


class TaskEditView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        task = TodoItem.objects.get(id=pk)
        form = TodoItemForm(request.POST, instance=task)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            return redirect(reverse('tasks:list'))

        return render(request, 'tasks/edit.html', {'form':form, 'task': task })


    def get(self, request, pk, *args, **kwargs):
        task = TodoItem.objects.get(id=pk)
        form = TodoItemForm(instance=task)
        return render(request, 'tasks/edit.html', {'form':form, 'task': task })


class TaskExportView(LoginRequiredMixin, View):
    def generate_body(self, user, priorities):
        q = Q()
        if priorities['prio_high']:
            q = q | Q(priority=TodoItem.PRIORITY_HIGH)
        if priorities["prio_med"]:
            q = q | Q(priority=TodoItem.PRIORITY_MEDIUM)
        if priorities["prio_low"]:
            q = q | Q(priority=TodoItem.PRIORITY_LOW)
        tasks = TodoItem.objects.filter(owner=user).filter(q).all()

        body = "Ваши задачи и приоритеты:\n"
        for t in list(tasks):
            if t.is_completed:
                body += f"[x] {t.description} ({t.get_priority_display()})\n"
            else:
                body += f"[ ] {t.description} ({t.get_priority_display()})\n"
        return body


    def post(self, request, *args, **kwargs):
        form = TodoItemExportForm(request.POST)
        if form.is_valid():
            email = request.user.email
            body = self.generate_body(request.user, form.cleaned_data)
            send_mail("Tasks", body, settings.SERVER_EMAIL, [email])
            messages.success(request, f"Tasks were sent on email {email}")
        else:
            messages.error(request, "Something went wrong, please try again")
        return redirect(reverse("tasks:list"))


    def get(self, request, *args, **kwargs):
        form = TodoItemExportForm()
        return render(request, "tasks/export.html", {"form": form})