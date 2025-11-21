from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Quiz, Question, MCQOption
from .serializers import (
    QuizSerializer, QuizListSerializer, QuizCreateUpdateSerializer,
    QuestionSerializer, QuestionCreateUpdateSerializer,
    MCQOptionSerializer
)
from quiz_management.utils import success_response, error_response


class QuizListCreateView(generics.ListCreateAPIView):
    """
    List all quizzes or create a new quiz.
    """
    queryset = Quiz.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title', 'total_questions']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuizCreateUpdateSerializer
        return QuizListSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @swagger_auto_schema(
        operation_description="List all quizzes with pagination and filtering",
        responses={200: QuizListSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new quiz",
        request_body=QuizCreateUpdateSerializer,
        responses={
            201: QuizSerializer,
            400: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a quiz.
    """
    queryset = Quiz.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return QuizCreateUpdateSerializer
        return QuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(created_by=self.request.user)

    @swagger_auto_schema(
        operation_description="Get quiz details with all questions",
        responses={200: QuizSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update quiz details",
        request_body=QuizCreateUpdateSerializer,
        responses={200: QuizSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update quiz details",
        request_body=QuizCreateUpdateSerializer,
        responses={200: QuizSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a quiz",
        responses={204: 'Quiz deleted successfully'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class QuestionListCreateView(generics.ListCreateAPIView):
    """
    List all questions for a quiz or create a new question.
    """
    serializer_class = QuestionCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        quiz_id = self.kwargs['quiz_id']
        return Question.objects.filter(quiz_id=quiz_id, quiz__created_by=self.request.user)

    def perform_create(self, serializer):
        quiz_id = self.kwargs['quiz_id']
        try:
            quiz = Quiz.objects.get(id=quiz_id, created_by=self.request.user)
            serializer.save(quiz=quiz)
        except Quiz.DoesNotExist:
            return error_response(
                message="Quiz not found or you don't have permission to modify it",
                status_code=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_description="List all questions for a quiz",
        responses={200: QuestionSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Add a new question to quiz",
        request_body=QuestionCreateUpdateSerializer,
        responses={201: QuestionSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a question.
    """
    serializer_class = QuestionCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Question.objects.filter(quiz__created_by=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return QuestionSerializer
        return QuestionCreateUpdateSerializer

    @swagger_auto_schema(
        operation_description="Get question details",
        responses={200: QuestionSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update question details",
        request_body=QuestionCreateUpdateSerializer,
        responses={200: QuestionSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update question",
        request_body=QuestionCreateUpdateSerializer,
        responses={200: QuestionSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a question",
        responses={204: 'Question deleted successfully'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
