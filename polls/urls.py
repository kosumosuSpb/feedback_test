from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from polls import views


urlpatterns = [
    # path('projects/', views.project_list),
    # path('projects/<int:pk>/', views.project_detail),
    # path('questionlist/', views.QuestionListViewAPI.as_view()),
    # path('questionlist/<int:pk>/', views.QuestionListDetailViewAPI.as_view()),
    path('', views.QuestionViewAPI.as_view()),  # вывод всех вопросов
    path('<int:pk>/', views.QuestionDetailViewAPI.as_view()),  # Вывод конкретного вопроса
    path('answers/', views.AnswerListViewAPI.as_view()),  # вывод всех ответов на все вопросы
    path('answers/<int:pk>/', views.AnswerDetailViewAPI.as_view()),  # вывод конкретного ответа
    path('<int:q_pk>/answers/', views.AnswerListViewAPI.as_view()),  # вывод всех ответов на конкретный вопрос
    path('<int:q_pk>/answers/<int:pk>', views.AnswerDetailViewAPI.as_view()),  # вывод конкретного ответа на конкретный вопрос
]

urlpatterns = format_suffix_patterns(urlpatterns)
