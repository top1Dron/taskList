from django import forms
from tasks.models import TodoItem


class AddTaskForm(forms.Form):
    description = forms.CharField(max_length=64, label='')


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ('description', 'priority', 'tags')
        labels = {'description': 'Description', 'priority': '', 'tags': 'tags'}


class TodoItemExportForm(forms.Form):
    prio_high = forms.BooleanField(
        label="high priority", initial=True, required=False
    )
    prio_med = forms.BooleanField(
        label="medium priority", initial=True, required=False
    )
    prio_low = forms.BooleanField(
        label="low priority", initial=False, required=False
    )