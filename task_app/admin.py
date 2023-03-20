from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from task_app.models import ProjectList, TaskList, Status, Sprint


@admin.register(ProjectList)
class ProjectListAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
        "created",
        "completed",
        "author",
        "performer",
    ]
    list_filter = [
        "title",
        "author",
        "performer",
    ]
    readonly_fields = [
        "created",
    ]
    search_fields = ("title", "description")
    ordering = ["created"]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()


class TaskListHistoryAdmin(SimpleHistoryAdmin):
    list_display = [
        "id",
        "title",
        "description",
        "status",
        "sprint",
        "created",
        "deadline",
        "completed",
        "author",
        "performer",
    ]
    history_list_display = [
        "id",
        "title",
        "description",
        "status",
        "sprint",
        "created",
        "deadline",
        "completed",
        "author",
        "performer",
    ]
    search_fields = ["title"]


# @admin.register(TaskList)


class TaskListAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
        "status",
        "sprint",
        "created",
        "deadline",
        "completed",
        "author",
        "performer",
    ]
    list_filter = [
        "status",
        "sprint",
        "author",
        "performer",
    ]
    readonly_fields = ["created", "status"]
    search_fields = ("title", "description")
    ordering = ["deadline"]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()


admin.site.register(TaskList, TaskListHistoryAdmin)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
    ]


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "created",
        "deadline",
        "completed",
        "sprint_status",
        "project_list",
    ]
