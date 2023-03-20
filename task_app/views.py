from rest_framework.decorators import action
from django.http import JsonResponse

from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from rest_framework import viewsets, mixins

from .filters import SprintFilterSet, TaskListFilterSet, ProjectListFilterSet
from .forms import RegisterForm
from django.contrib.admin.widgets import AdminDateWidget
from task_app.models import ProjectList, TaskList, Sprint
from django.views.generic import (
    CreateView,
    ListView,
    DeleteView,
    UpdateView,
)

from .serializers import ProjectListSerializer, SprintSerializer, TaskListSerializer


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect("/login")
    else:
        form = RegisterForm()
    return render(response, "registration/register.html", {"form": form})


"""Список проектов"""


class ProjectView(ListView):
    context_object_name = "project_"
    queryset = ProjectList.objects.all()
    template_name = "taskapp/home.html"


class ProjectCreateView(CreateView):
    model = ProjectList
    fields = [
        "title",
        "description",
        "completed",
        "performer",
    ]
    template_name = "taskapp/project_create.html"
    success_url = reverse_lazy("home")

    def get_form(self, form_class=None):
        form = super(ProjectCreateView, self).get_form(form_class)
        form.fields["completed"].widget = AdminDateWidget(attrs={"type": "date"})
        return form

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super(ProjectCreateView, self).form_valid(form)


class ProjectDeleteView(DeleteView):
    model = ProjectList
    template_name = "taskapp/project_delete.html"
    success_url = reverse_lazy("home")


class ProjectUpdateView(UpdateView):
    model = ProjectList
    fields = [
        "title",
        "description",
        "completed",
        "performer",
    ]
    template_name = "taskapp/project_edit.html"
    success_url = reverse_lazy("home")

    def get_form(self, form_class=None):
        form = super(ProjectUpdateView, self).get_form(form_class)
        form.fields["completed"].widget = AdminDateWidget(attrs={"type": "date"})
        return form

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super(ProjectUpdateView, self).form_valid(form)


"""Список спринтов"""


class SprintView(ListView):
    context_object_name = "sprint_"
    queryset = Sprint.objects.all()
    template_name = "taskapp/home_sprint.html"


class SprintCreateView(CreateView):
    model = Sprint
    fields = [
        "title",
        "deadline",
        "completed",
        "sprint_status",
        "project_list",
    ]
    template_name = "taskapp/sprint_create.html"
    success_url = reverse_lazy("home_sprint")

    def get_form(self, form_class=None):
        form = super(SprintCreateView, self).get_form(form_class)
        form.fields["deadline"].widget = AdminDateWidget(attrs={"type": "date"})
        form.fields["completed"].widget = AdminDateWidget(attrs={"type": "date"})
        form.fields["project_list"].required = True
        return form


class SprintDeleteView(DeleteView):
    model = Sprint
    template_name = "taskapp/sprint_delete.html"
    success_url = reverse_lazy("home_sprint")


class SprintUpdateView(UpdateView):
    model = Sprint
    fields = [
        "title",
        "deadline",
        "completed",
        "sprint_status",
        "project_list",
    ]
    template_name = "taskapp/sprint_edit.html"
    success_url = reverse_lazy("home_sprint")

    def get_form(self, form_class=None):
        form = super(SprintUpdateView, self).get_form(form_class)
        form.fields["deadline"].widget = AdminDateWidget(attrs={"type": "date"})
        form.fields["completed"].widget = AdminDateWidget(attrs={"type": "date"})
        form.fields["project_list"].required = True
        return form


"""Список задач"""


class TaskView(ListView):
    context_object_name = "task_"
    queryset = TaskList.objects.all()
    template_name = "taskapp/home_task.html"


class TaskCreateView(CreateView):
    model = TaskList
    fields = [
        "title",
        "description",
        "sprint",
        "deadline",
        "completed",
        "performer",
    ]
    template_name = "taskapp/task_create.html"
    success_url = reverse_lazy("home_task")

    def get_form(self, form_class=None):
        form = super(TaskCreateView, self).get_form(form_class)
        form.fields["deadline"].widget = AdminDateWidget(attrs={"type": "date"})
        form.fields["completed"].widget = AdminDateWidget(attrs={"type": "date"})
        return form

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super(TaskCreateView, self).form_valid(form)


class TaskDeleteView(DeleteView):
    model = TaskList
    template_name = "taskapp/task_delete.html"
    success_url = reverse_lazy("home_task")


class TaskUpdateView(UpdateView):
    model = TaskList
    fields = [
        "title",
        "description",
        "sprint",
        "deadline",
        "completed",
        "performer",
    ]
    template_name = "taskapp/task_edit.html"
    success_url = reverse_lazy("home_task")

    def get_form(self, form_class=None):
        form = super(TaskUpdateView, self).get_form(form_class)
        form.fields["deadline"].widget = AdminDateWidget(attrs={"type": "date"})
        form.fields["completed"].widget = AdminDateWidget(attrs={"type": "date"})
        return form

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super(TaskUpdateView, self).form_valid(form)


"""Django Rest Framework"""

"""Проекты"""


class ProjectListViewSet(
    mixins.ListModelMixin,  # GET /projects
    mixins.CreateModelMixin,  # POST /projects
    mixins.RetrieveModelMixin,  # GET /projects/1
    mixins.DestroyModelMixin,  # DELETE /projects/1
    mixins.UpdateModelMixin,  # PUT /projects/1
    viewsets.GenericViewSet,
):
    queryset = ProjectList.objects.all().order_by("id")
    serializer_class = ProjectListSerializer
    filterset_class = ProjectListFilterSet

    @action(detail=False, methods=["get"], url_path="actions/count")
    def get_count(self, request, pk=None):
        # user = request.user
        count = self.get_queryset().count()
        return JsonResponse(data={"count": count})


"""Задачи"""


class TaskListViewSet(
    mixins.ListModelMixin,  # GET /tasks
    mixins.CreateModelMixin,  # POST /tasks
    mixins.RetrieveModelMixin,  # GET /tasks/1
    mixins.DestroyModelMixin,  # DELETE /tasks/1
    mixins.UpdateModelMixin,  # PUT /tasks/1
    viewsets.GenericViewSet,
):
    queryset = TaskList.objects.all().order_by("id")
    serializer_class = TaskListSerializer
    filterset_class = TaskListFilterSet

    @action(detail=False, methods=["get"], url_path="actions/count")
    def get_count(self, request, pk=None):
        user = request.user
        count = self.get_queryset().count()
        return JsonResponse(data={"count": count, "user": str(user.username)})


"""Спринты"""


class SprintViewSet(
    mixins.ListModelMixin,  # GET /sprints
    mixins.CreateModelMixin,  # POST /sprints
    mixins.RetrieveModelMixin,  # GET /sprints/1
    mixins.DestroyModelMixin,  # DELETE /sprints/1
    mixins.UpdateModelMixin,  # PUT /sprints/1
    viewsets.GenericViewSet,
):
    queryset = Sprint.objects.all().order_by("id")
    serializer_class = SprintSerializer
    filterset_class = SprintFilterSet
