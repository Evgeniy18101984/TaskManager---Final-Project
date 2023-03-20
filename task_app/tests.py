from datetime import timezone

from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from task_app.models import TaskList, ProjectList


class ArticleTestCase(APITestCase):
    # def setUp(self) -> None:
    # a = baker.make(ProjectList, 5, content="some_content")
    # User = get_user_model()
    # user = User(username="test")
    # user.save()
    # _set_current_user(user)
    # self.client.force_authenticate(user=user)

    def test_action_calculate(self):
        url = "/api/projects/actions/count/"
        resp = self.client.get(url, content_type="application/json")
        resp_json = resp.json()

        self.assertEqual(200, resp.status_code)
        self.assertIn("count", resp_json.keys())
        self.assertEqual(0, resp_json["count"])


class ProjectListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TEST", password="1q2wefweWRKDe!Q@W#E", email="test@test.com"
        )
        self.test = ProjectList(
            title="TEST",
            description="TEST",
            author=self.user,
        )

        self.test.save()

    def tearDown(self):
        self.test.delete()

    def test_read(self):
        self.assertEqual(self.test.title, "TEST")
        self.assertEqual(self.test.description, "TEST")

    def test_edit_description(self):
        self.test.description = "NEWTEST"
        self.test.save()
        self.assertEqual(self.test.description, "NEWTEST")

    def test_edit_title(self):
        self.test.title = "NEWTESTTITLE"
        self.test.save()
        self.assertEqual(self.test.title, "NEWTESTTITLE")

    def test_user_authenticate(self):
        user = authenticate(username="TEST", password="1q2wefweWRKDe!Q@W#E")
        self.assertTrue((user is not None) and user.is_authenticated)
