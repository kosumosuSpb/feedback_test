from rest_framework import viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from polls.serializers import *
import logging


# Создаём логгер
logger = logging.getLogger(__name__)


class ProjectVewset(viewsets.ModelViewSet):
    """Проекты"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class QuestionListViewset(viewsets.ModelViewSet):
    """Списки вопросов"""
    queryset = QuestionList.objects.all()
    serializer_class = QuestionListSerializer


class QuestionViewset(viewsets.ModelViewSet):
    """Вопросы"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=True)
    def answers(self, request, pk=None):
        """Отображение ответов на конкретный вопрос"""
        queryset = Question.objects.all()  # берём базовый кверисет
        question = get_object_or_404(queryset, pk=pk)  # вытаскиваем конкретный вопрос
        answers = Answer.objects.filter(question=question)  # фильтруем ответы по этому вопросу
        serializer = AnswerSerializer(answers, many=True)  # прогоняем через сериалайзер ответов
        return Response(serializer.data)  # возвращаем их, как ответ


class AnswersViewset(viewsets.ModelViewSet):
    """Ответы на вопросы"""
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
