from django.urls import path
from .views import (
    PublicQuizListView,
    PublicQuizDetailView,
    QuizSubmissionView,
    QuizResultView,
    AdminQuizResponseListView,
    AdminQuizResponseDetailView
)

urlpatterns = [
    # Public endpoints
    path('quizzes/', PublicQuizListView.as_view(), name='public-quiz-list'),
    path('quizzes/<int:pk>/', PublicQuizDetailView.as_view(), name='public-quiz-detail'),
    path('quizzes/<int:quiz_id>/submit/', QuizSubmissionView.as_view(), name='quiz-submit'),
    path('results/<str:session_id>/', QuizResultView.as_view(), name='quiz-result'),
    
    # Admin endpoints (moved here from quiz app for better organization)
    path('admin/responses/', AdminQuizResponseListView.as_view(), name='admin-response-list'),
    path('admin/responses/<int:pk>/', AdminQuizResponseDetailView.as_view(), name='admin-response-detail'),
]