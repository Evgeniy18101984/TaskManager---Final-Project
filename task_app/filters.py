from django_filters import rest_framework as dj_filters

from task_app.models import Sprint, TaskList, ProjectList


class ProjectListFilterSet(dj_filters.FilterSet):
    title = dj_filters.CharFilter(field_name="title", lookup_expr="icontains")

    order_by_field = "ordering"

    class Meta:
        model = ProjectList
        fields = [
            "title",
        ]


class TaskListFilterSet(dj_filters.FilterSet):
    title = dj_filters.CharFilter(field_name="title", lookup_expr="icontains")
    status = dj_filters.CharFilter(field_name="status", lookup_expr="exact")

    order_by_field = "ordering"

    class Meta:
        model = TaskList
        fields = ["title", "status"]


class SprintFilterSet(dj_filters.FilterSet):
    title = dj_filters.CharFilter(field_name="title", lookup_expr="icontains")
    sprint_status = dj_filters.CharFilter(
        field_name="sprint_status", lookup_expr="exact"
    )

    order_by_field = "ordering"

    class Meta:
        model = Sprint
        fields = ["title", "sprint_status"]
