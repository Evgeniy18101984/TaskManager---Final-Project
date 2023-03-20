"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include
from django.contrib.auth import views

from task_app.views import (
    ProjectView,
    ProjectDeleteView,
    ProjectUpdateView,
    ProjectCreateView,
    TaskView,
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView,
    SprintUpdateView,
    SprintDeleteView,
    SprintCreateView,
    SprintView,
)
from task_app import views as v

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("task_app.urls")),
    path("", ProjectView.as_view(), name="home"),
    # Авторизация
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", v.register, name="register"),
    # Проекты
    path("project/create/", ProjectCreateView.as_view(), name="create"),
    path("project/delete/<int:pk>/", ProjectDeleteView.as_view(), name="delete"),
    path("project/edit/<int:pk>/", ProjectUpdateView.as_view(), name="edit"),
    # Задачи
    path("task/", TaskView.as_view(), name="home_task"),
    path("task/create/", TaskCreateView.as_view(), name="create_task"),
    path("task/delete/<int:pk>/", TaskDeleteView.as_view(), name="delete_task"),
    path("task/edit/<int:pk>/", TaskUpdateView.as_view(), name="edit_task"),
    # Спринты
    path("sprint/", SprintView.as_view(), name="home_sprint"),
    path("sprint/create/", SprintCreateView.as_view(), name="create_sprint"),
    path("sprint/delete/<int:pk>/", SprintDeleteView.as_view(), name="delete_sprint"),
    path("sprint/edit/<int:pk>/", SprintUpdateView.as_view(), name="edit_sprint"),
    # Django Rest Framework
]
