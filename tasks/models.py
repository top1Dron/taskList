from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class TodoItem(models.Model):
    description = models.CharField(max_length=64)
    is_completed = models.BooleanField("executed", default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )


    def __str__(self):
        return self.description.lower()


    def get_absolute_url(self):
        return reverse("tasks:details", args=[self.pk])


    class Meta:
        ordering = ('-created',)
    
