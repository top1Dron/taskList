from django import forms
from tasks.models import TodoItem


class AddTaskForm(forms.Form):
    description = forms.CharField(max_length=64, label='')


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ('description',)
        labels = {'description': ''}