from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class TodoItem(models.Model):
    PRIORITY_HIGH = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_LOW = 3

    PRIORITY_CHOISES = [
        (PRIORITY_HIGH, 'High priority'),
        (PRIORITY_MEDIUM, 'Medium priority'),
        (PRIORITY_LOW, 'Low priority'),
    ]

    description = models.CharField(max_length=64)
    is_completed = models.BooleanField("executed", default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    priority = models.IntegerField(
        'Priority', choices=PRIORITY_CHOISES, default=PRIORITY_MEDIUM
    )


    def __str__(self):
        return self.description.lower()


    def get_absolute_url(self):
        return reverse("tasks:details", args=[self.pk])


    class Meta:
        ordering = ('-created',)
    
