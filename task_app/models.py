from datetime import timedelta

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from simple_history.models import HistoricalRecords

"""Модель списка проектов"""


class ProjectList(models.Model):
    title = models.CharField(_("Тема проекта"), max_length=100, unique=True)
    description = models.TextField(_("Описание проекта"))
    created = models.DateTimeField(_("Дата создания"), default=timezone.now())
    completed = models.DateTimeField(
        _("Дата выполнения"), default=None, null=True, blank=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="author_project",
        verbose_name=_("Автор проекта"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    performer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_project",
        verbose_name=_("Исполнитель проекта"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    history = HistoricalRecords()

    class Meta:
        ordering = ["created"]

    def get_absolute_url(self):
        return reverse("home", args=[self.id])

    def __str__(self):
        return f"{self.title}"


"""Модель списка спринтов"""


class Sprint(models.Model):
    title = models.CharField(
        _("Название спринта"), max_length=300, blank=True, null=False
    )
    created = models.DateTimeField(_("Дата создания"), default=timezone.now())
    deadline = models.DateTimeField(
        _("Контрольный срок"), default=timezone.now() + timedelta(days=14)
    )
    completed = models.DateTimeField(
        _("Дата выполнения"), null=True, blank=True, default=None
    )
    sprint_status = models.BooleanField(_("Статус"), default=False)
    project_list = models.ForeignKey(
        to="ProjectList",
        on_delete=models.CASCADE,
        blank=True,
        null=False,
        related_name="sprint_project",
        verbose_name="Проект",
    )

    history = HistoricalRecords()

    class Meta:
        ordering = ["deadline"]

    def get_absolute_url(self):
        return reverse("sprint", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if self.sprint_status == True:
            self.completed = timezone.now()
        elif self.completed is not None:
            self.sprint_status = True
        return super().save(*args, **kwargs)


"""Модель списка задач"""


class TaskList(models.Model):
    title = models.CharField(_("Тема задачи"), max_length=100, unique=True)
    description = models.TextField(_("Описание задачи"))
    status = models.ForeignKey(
        to="Status",
        on_delete=models.PROTECT,
        blank=True,
        null=False,
        verbose_name="Статус",
    )
    sprint = models.ForeignKey(
        to="Sprint",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="task_sprint",
        verbose_name="Спринт",
    )
    created = models.DateTimeField(_("Дата/время создания"), default=timezone.now())
    deadline = models.DateTimeField(
        _("Контрольный срок"), default=timezone.now() + timedelta(days=14)
    )
    completed = models.DateTimeField(
        _("Дата/время выполнения"), default=None, null=True, blank=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="author_task",
        verbose_name=_("Автор задачи"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    performer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_task",
        verbose_name=_("Исполнитель задачи"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    history = HistoricalRecords()

    class Meta:
        ordering = ["deadline"]

    def get_absolute_url(self):
        return reverse("task-update", args=[str(self.sprint.id), self.id])

    def __str__(self):
        return f"{self.id}|{self.title}"

    """Статусы"""
    """
    В Postgres:
    1 - "Waiting"
    2 - "Processing"
    3 - "Solved"
    """

    def save(self, *args, **kwargs):
        if self.performer is None and self.completed is None:
            self.status = Status.objects.get(title="Waiting")
        elif self.performer is not None and self.completed is None:
            self.status = Status.objects.get(title="Processing")
        elif self.performer is not None and self.completed is not None:
            self.status = Status.objects.get(title="Solved")
        elif (
            self.status == Status.objects.get(title="Solved") and self.performer is None
        ):
            self.status = Status.objects.get(title="Waiting")
            self.completed = None
        elif (
            self.status == Status.objects.get(title="Solved") and self.completed is None
        ):
            self.status = Status.objects.get(title="Waiting")
        return super().save(*args, **kwargs)


"""Статусы"""


class Status(models.Model):
    title = models.CharField(_("Статус"), max_length=50, blank=True, null=False)

    history = HistoricalRecords()

    def get_absolute_url(self):
        return f"/task/{self}/"

    def __str__(self):
        return f"{self.title}"
