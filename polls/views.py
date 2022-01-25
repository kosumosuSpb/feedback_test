from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from polls.models import *
from polls.serializers import *

from rest_framework import generics


# первые два представления на функциях - просто для примера,
# чтобы видеть наглядно, что примерно внутри у дженериков

# список проектов
@api_view(['GET', 'POST'])
def project_list(request, format=None):
    """
    List all projects, or create a new.
    """

    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# проект отдельно
@api_view(['GET', 'PUT', 'DELETE'])
def project_detail(request, pk, format=None):
    """
    Retrieve, update or delete a project.
    """
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionListViewAPI(generics.ListCreateAPIView):
    """
    Question Lists API View
    API представление списков вопросов
    """
    queryset = QuestionList.objects.all()
    serializer_class = QuestionListSerializer


class QuestionListDetailViewAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Question List Detail API View
    API представление списка вопросов (одного)
    """
    queryset = QuestionList.objects.all()
    serializer_class = QuestionListSerializer


class QuestionViewAPI(generics.ListCreateAPIView):
    """
    Question API View
    API представление списка вопросов
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetailViewAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    API представление вопроса (одного)
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerListViewAPI(generics.ListCreateAPIView):
    """
    API представление списка ответов
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def get_queryset(self):
        # берём все ответы (если не указан конкретный вопрос - выдадим их все)
        answers = Answer.objects.all()
        # пытаемся забрать из адреса pk вопроса, если его нет, то берём None
        question_pk = self.kwargs.get('q_pk', None)
        if question_pk:
            # если вопрос указан, то забираем объект с этим id
            # (если его не существует, то придёт просто пустой кверисет)
            answers = answers.filter(question_id=question_pk)
        return answers


class AnswerDetailViewAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    API представление ответа (одного)
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
