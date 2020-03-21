from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.tasks_list, name='list'),
    path('complete/<int:uid>', views.complete_task, name='complete'),
    path('delete/<int:uid>', views.delete_task, name='delete'),
]