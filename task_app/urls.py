from rest_framework.routers import DefaultRouter

from task_app.views import ProjectListViewSet, SprintViewSet, TaskListViewSet

router = DefaultRouter()
router.register(
    prefix="projects",
    viewset=ProjectListViewSet,
    basename="projects",
)
router.register(
    prefix="tasks",
    viewset=TaskListViewSet,
    basename="tasks",
)
router.register(
    prefix="sprints",
    viewset=SprintViewSet,
    basename="sprints",
)
urlpatterns = router.urls
