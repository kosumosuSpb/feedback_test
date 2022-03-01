from django.test import TestCase
import logging
from polls import models


logger = logging.getLogger(__name__)


class ViewsTestCase(TestCase):
    @staticmethod
    def create_test_fixtures():
        """Создаёт тестовые объекты"""
        project = models.Project(name='project1', description='description1')
        project.save()
        question_list = models.QuestionList(title='Question List 1', project=project)
        question_list.save()
        template = models.Template(name='Template 1')
        template.save()
        question = models.Question(title='Question Title 1',
                                   description='Question descriprion 1',
                                   template=template,
                                   question_list=question_list)
        question.save()
        answer = models.Answer(rating=3, question=question)
        answer.save()

    def test_root_loads_properly(self):
        """Проверяет корректность загрузки root"""
        response = self.client.get('http://127.0.0.1:8000/')
        self.assertEqual(response.status_code, 200)

    def test_projects_loads_properly(self):
        """Проверяет корректность загрузки страницы проектов"""
        response = self.client.get('http://127.0.0.1:8000/projects/')
        self.assertEqual(response.status_code, 200)

    def test_question_lists_loads_properly(self):
        """Проверяет корректность загрузки страницы списков вопросов"""
        response = self.client.get('http://127.0.0.1:8000/question_lists/')
        self.assertEqual(response.status_code, 200)

    def test_questions_loads_properly(self):
        """Проверяет корректность загрузки страницы вопросов"""
        response = self.client.get('http://127.0.0.1:8000/questions/')
        self.assertEqual(response.status_code, 200)

    def test_answers_loads_properly(self):
        """Проверяет корректность загрузки страницы ответов"""
        response = self.client.get('http://127.0.0.1:8000/answers/')
        self.assertEqual(response.status_code, 200)

    def test_questions_action_loads_properly(self):
        """Проверяет корректность работы экшена questions/<id>/answers"""
        # создаём тестовые объекты
        ViewsTestCase.create_test_fixtures()

        # запускаем тест
        response = self.client.get('http://127.0.0.1:8000/questions/1/answers/')
        self.assertEqual(response.status_code, 200)

    def test_rating(self):
        """Проверка рейтинга"""
        # создаём тестовые объекты
        ViewsTestCase.create_test_fixtures()

        # проверяем, что рейтинг - float
        question = models.Question.objects.get(pk=1)
        rating = question.rating
        self.assertIsInstance(rating, float or 0)

