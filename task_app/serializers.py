from rest_framework import serializers

from task_app.models import ProjectList, TaskList, Sprint


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectList
        read_only_fields = ["id", "created"]
        fields = read_only_fields + [
            "title",
            "description",
            "completed",
            "author",
            "performer",
        ]


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskList
        read_only_fields = ["id", "created"]
        fields = read_only_fields + [
            "title",
            "description",
            "status",
            "sprint",
            "deadline",
            "completed",
            "author",
            "performer",
        ]


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        read_only_fields = ["id", "created"]
        fields = read_only_fields + [
            "title",
            "deadline",
            "completed",
            "sprint_status",
            "project_list",
        ]
