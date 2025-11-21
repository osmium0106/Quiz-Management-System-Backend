from django.urls import path
from .views import (
    QuizListCreateView,
    QuizDetailView,
    QuestionListCreateView,
    QuestionDetailView
)

urlpatterns = [
    # Quiz endpoints
    path('quizzes/', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    
    # Question endpoints
    path('quizzes/<int:quiz_id>/questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
]