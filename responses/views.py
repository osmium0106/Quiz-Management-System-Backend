from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import QuizResponse, Answer
from quizzes.models import Quiz
from quizzes.serializers import QuizPublicListSerializer, QuizPublicSerializer
from .serializers import (
    QuizSubmissionSerializer, QuizResponseSerializer, QuizResponseListSerializer,
    QuizResultSerializer
)
from quiz_management.utils import success_response, error_response


class PublicQuizListView(generics.ListAPIView):
    """
    Public endpoint to list all active quizzes.
    """
    queryset = Quiz.objects.filter(is_active=True)
    serializer_class = QuizPublicListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    @swagger_auto_schema(
        operation_description="List all active quizzes available for public access",
        responses={200: QuizPublicListSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PublicQuizDetailView(generics.RetrieveAPIView):
    """
    Public endpoint to get quiz details for taking the quiz.
    """
    queryset = Quiz.objects.filter(is_active=True)
    serializer_class = QuizPublicSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Get quiz details with questions for taking the quiz",
        responses={200: QuizPublicSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class QuizSubmissionView(generics.CreateAPIView):
    """
    Public endpoint to submit quiz responses.
    """
    serializer_class = QuizSubmissionSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        quiz_id = self.kwargs['quiz_id']
        try:
            quiz = Quiz.objects.get(id=quiz_id, is_active=True)
            context['quiz'] = quiz
        except Quiz.DoesNotExist:
            pass
        return context

    @swagger_auto_schema(
        operation_description="Submit answers for a quiz",
        request_body=QuizSubmissionSerializer,
        responses={
            201: openapi.Response('Quiz submitted successfully', QuizResultSerializer),
            400: 'Bad Request',
            404: 'Quiz not found'
        }
    )
    def post(self, request, *args, **kwargs):
        quiz_id = self.kwargs['quiz_id']
        
        try:
            quiz = Quiz.objects.get(id=quiz_id, is_active=True)
        except Quiz.DoesNotExist:
            return error_response(
                message="Quiz not found or inactive",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            quiz_response = serializer.save()
            result_data = QuizResultSerializer(quiz_response).data
            
            return success_response(
                data=result_data,
                message="Quiz submitted successfully",
                status_code=status.HTTP_201_CREATED
            )
        
        return error_response(
            message="Quiz submission failed",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class QuizResultView(generics.RetrieveAPIView):
    """
    Public endpoint to view quiz results.
    """
    serializer_class = QuizResultSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'session_id'

    def get_queryset(self):
        return QuizResponse.objects.filter(is_completed=True)

    @swagger_auto_schema(
        operation_description="Get quiz results by session ID",
        responses={200: QuizResultSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# Admin views for managing responses
class AdminQuizResponseListView(generics.ListAPIView):
    """
    Admin endpoint to list all quiz responses with filtering.
    """
    queryset = QuizResponse.objects.filter(is_completed=True)
    serializer_class = QuizResponseListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['participant_name', 'participant_email', 'quiz__title']
    ordering_fields = ['submitted_at', 'score', 'percentage']
    ordering = ['-submitted_at']

    def get_queryset(self):
        # Only show responses for quizzes created by the current user
        return QuizResponse.objects.filter(
            is_completed=True,
            quiz__created_by=self.request.user
        )

    @swagger_auto_schema(
        operation_description="List all quiz responses for admin with filtering and pagination",
        responses={200: QuizResponseListSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AdminQuizResponseDetailView(generics.RetrieveAPIView):
    """
    Admin endpoint to view detailed quiz response.
    """
    serializer_class = QuizResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuizResponse.objects.filter(
            is_completed=True,
            quiz__created_by=self.request.user
        )

    @swagger_auto_schema(
        operation_description="Get detailed quiz response with all answers",
        responses={200: QuizResponseSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
