from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from task_manager.users.models import MyUser
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class LoginMixinTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = MyUser.objects.create_user(
            username="test_user1",  # pk:1
            first_name="first1",
            last_name="last1",
            password="12qazWSX",
        )
        cls.user2 = MyUser.objects.create_user(
            username="test_user2",  # pk:2
            first_name="first2",
            last_name="last2",
            password="12qazWSX",
        )

        cls.label1 = Label.objects.create(name="Testlabel_1")  # pk:1
        cls.label2 = Label.objects.create(name="Testlabel_2")  # pk:2
        cls.label3 = Label.objects.create(name="Testlabel_3")  # pk:3

        cls.status1 = Status.objects.create(name="Teststatus_1")  # pk:1
        cls.status2 = Status.objects.create(name="Teststatus_2")  # pk:2
        cls.status3 = Status.objects.create(name="Teststatus_3")  # pk:3

        cls.task1 = Task.objects.create(
            name="Testtask_1",  # pk:1
            author=cls.user2,  # author:2
            executor=cls.user1,  # executor:1
            status=cls.status1,  # status:1
        )
        cls.task1.labels.set([cls.label1, cls.label2])  # labels [1,2]

        cls.task2 = Task.objects.create(
            name="Testtask_2",  # pk:2
            author=cls.user1,  # author:1
            executor=cls.user2,  # executor:2
            status=cls.status2,  # status:2
        )

        cls.urls = [
            reverse("user_update", kwargs={"pk": cls.user1.pk}),
            reverse("user_delete", kwargs={"pk": cls.user1.pk}),
            reverse("labels"),
            reverse("label_create"),
            reverse("label_update", kwargs={"pk": cls.label1.pk}),
            reverse("label_delete", kwargs={"pk": cls.label1.pk}),
            reverse("statuses"),
            reverse("status_create"),
            reverse("status_update", kwargs={"pk": cls.status1.pk}),
            reverse("status_delete", kwargs={"pk": cls.status1.pk}),
            reverse("tasks"),
            reverse("task_show", kwargs={"pk": cls.task1.pk}),
            reverse("task_create"),
            reverse("task_update", kwargs={"pk": cls.task1.pk}),
            reverse("task_delete", kwargs={"pk": cls.task1.pk}),
        ]

    def test_access_without_login(self):
        for url in self.urls:
            response = self.client.get(url, follow=False)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("login"))

            response = self.client.get(url, follow=True)
            self.assertContains(
                response, _("You are not logged in! Please log in."), status_code=200
            )
