from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import Test, Question, Category, AnswerBlank


class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        self.category = Category.objects.create(name="Math", description="Math tests")

        self.question = Question.objects.create(
            content="What is 2 + 2?",
            answer_list=["2", "3", "4", "5"],
            correct_answers=["4"],
            points=10.0
        )

        self.test = Test.objects.create(
            title="Basic Math Test",
            description="A simple math test",
            author=self.user,
            total_points=10.0,
            has_timer=True,
            starting_datetime=timezone.now(),
            submission_datetime=timezone.now() + timezone.timedelta(hours=1),
            is_private=False,
            entrance_code=12345,
            test_category=self.category
        )
        self.test.question_list.add(self.question)

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Math")
        self.assertEqual(self.category.description, "Math tests")

    def test_question_creation(self):
        self.assertEqual(self.question.content, "What is 2 + 2?")
        self.assertEqual(self.question.correct_answers, ["4"])
        self.assertEqual(self.question.points, 10.0)

    def test_test_creation(self):
        self.assertEqual(self.test.title, "Basic Math Test")
        self.assertEqual(self.test.total_points, 10.0)
        self.assertTrue(self.test.has_timer)

    def test_answer_blank_creation(self):
        answer_blank = AnswerBlank.objects.create(
            User=self.user,
            Test=self.test,
            Answers={"1": ["4"]},
            Score=10.0
        )
        self.assertEqual(answer_blank.User, self.user)
        self.assertEqual(answer_blank.Test, self.test)
        self.assertEqual(answer_blank.Score, 10.0)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.category = Category.objects.create(name="Math", description="Math tests")
        self.test = Test.objects.create(
            title="Basic Math Test",
            description="A simple math test",
            author=self.user,
            total_points=10.0,
            has_timer=True,
            starting_datetime=timezone.now(),
            submission_datetime=timezone.now() + timezone.timedelta(hours=1),
            is_private=False,
            entrance_code=12345,
            test_category=self.category
        )
        self.client.login(username="testuser", password="testpassword")

    def test_home_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_create_test_view(self):
        response = self.client.get("/test/create/")
        self.assertEqual(response.status_code, 200)

    def test_show_test_view(self):
        response = self.client.get(f"/test/{self.test.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Basic Math Test")

    def test_edit_test_view(self):
        response = self.client.get(f"/test/{self.test.id}/edit/")
        self.assertEqual(response.status_code, 200)

    def test_delete_test_view(self):
        response = self.client.post(f"/test/{self.test.id}/delete/")
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Test.objects.filter(id=self.test.id).exists())
