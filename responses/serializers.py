from rest_framework import serializers
from .models import QuizResponse, Answer
from quizzes.models import Quiz, Question, MCQOption
from quizzes.serializers import QuizPublicSerializer, QuizPublicListSerializer
import uuid
from django.utils import timezone
from datetime import timedelta


class AnswerSubmissionSerializer(serializers.Serializer):
    """
    Serializer for answer submission.
    """
    question_id = serializers.IntegerField()
    selected_option_id = serializers.IntegerField(required=False, allow_null=True)
    text_answer = serializers.CharField(required=False, allow_blank=True, max_length=1000)

    def validate_question_id(self, value):
        try:
            question = Question.objects.get(id=value)
            return value
        except Question.DoesNotExist:
            raise serializers.ValidationError("Question not found.")

    def validate(self, attrs):
        question_id = attrs.get('question_id')
        selected_option_id = attrs.get('selected_option_id')
        text_answer = attrs.get('text_answer', '').strip()
        
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise serializers.ValidationError("Question not found.")
        
        if question.question_type in ['MCQ', 'TRUE_FALSE']:
            if not selected_option_id:
                if question.is_required:
                    raise serializers.ValidationError(f"Option selection is required for question {question_id}.")
            else:
                try:
                    option = MCQOption.objects.get(id=selected_option_id, question=question)
                    attrs['selected_option'] = option
                except MCQOption.DoesNotExist:
                    raise serializers.ValidationError(f"Invalid option for question {question_id}.")
        
        elif question.question_type == 'TEXT':
            if question.is_required and not text_answer:
                raise serializers.ValidationError(f"Text answer is required for question {question_id}.")
        
        attrs['question'] = question
        return attrs


class QuizSubmissionSerializer(serializers.Serializer):
    """
    Serializer for quiz submission.
    """
    participant_name = serializers.CharField(max_length=100)
    participant_email = serializers.EmailField()
    answers = AnswerSubmissionSerializer(many=True)
    
    def validate_participant_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Participant name must be at least 2 characters long.")
        return value.strip()

    def validate_answers(self, value):
        if not value:
            raise serializers.ValidationError("At least one answer is required.")
        
        question_ids = [answer['question_id'] for answer in value]
        if len(question_ids) != len(set(question_ids)):
            raise serializers.ValidationError("Duplicate answers for the same question are not allowed.")
        
        return value

    def create(self, validated_data):
        quiz = self.context['quiz']
        answers_data = validated_data.pop('answers')
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Check for existing attempts
        existing_attempts = QuizResponse.objects.filter(
            quiz=quiz,
            participant_email=validated_data['participant_email']
        ).count()
        
        if not quiz.allow_retakes and existing_attempts > 0:
            raise serializers.ValidationError("Retakes are not allowed for this quiz.")
        
        if existing_attempts >= quiz.max_attempts:
            raise serializers.ValidationError(f"Maximum attempts ({quiz.max_attempts}) reached for this quiz.")
        
        # Create quiz response
        quiz_response = QuizResponse.objects.create(
            quiz=quiz,
            participant_name=validated_data['participant_name'],
            participant_email=validated_data['participant_email'],
            session_id=session_id,
            attempt_number=existing_attempts + 1,
            submitted_at=timezone.now(),
            is_completed=True
        )
        
        # Create answers
        for answer_data in answers_data:
            Answer.objects.create(
                response=quiz_response,
                question=answer_data['question'],
                selected_option=answer_data.get('selected_option'),
                text_answer=answer_data.get('text_answer', '')
            )
        
        # Calculate score
        quiz_response.calculate_score()
        
        return quiz_response


class AnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for answers.
    """
    question_text = serializers.CharField(source='question.question_text', read_only=True)
    question_type = serializers.CharField(source='question.question_type', read_only=True)
    selected_option_text = serializers.CharField(source='selected_option.option_text', read_only=True)
    correct_option_text = serializers.SerializerMethodField()
    explanation = serializers.CharField(source='question.explanation', read_only=True)
    
    class Meta:
        model = Answer
        fields = [
            'question_text', 'question_type', 'selected_option_text', 
            'text_answer', 'is_correct', 'points_earned', 'correct_option_text', 'explanation'
        ]
    
    def get_correct_option_text(self, obj):
        if obj.question.question_type in ['MCQ', 'TRUE_FALSE']:
            correct_option = obj.question.options.filter(is_correct=True).first()
            return correct_option.option_text if correct_option else None
        return None


class QuizResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for quiz responses.
    """
    answers = AnswerSerializer(many=True, read_only=True)
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    
    class Meta:
        model = QuizResponse
        fields = [
            'id', 'quiz_title', 'participant_name', 'participant_email',
            'session_id', 'score', 'total_points', 'percentage', 'is_passed',
            'time_taken', 'started_at', 'submitted_at', 'attempt_number',
            'correct_answers_count', 'total_questions_count', 'answers'
        ]


class QuizResponseListSerializer(serializers.ModelSerializer):
    """
    Serializer for quiz response list (without detailed answers).
    """
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    
    class Meta:
        model = QuizResponse
        fields = [
            'id', 'quiz_title', 'participant_name', 'participant_email',
            'score', 'total_points', 'percentage', 'is_passed',
            'submitted_at', 'attempt_number', 'correct_answers_count',
            'total_questions_count'
        ]


class QuizResultSerializer(serializers.ModelSerializer):
    """
    Serializer for quiz results shown to participants.
    """
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    answers = serializers.SerializerMethodField()
    
    class Meta:
        model = QuizResponse
        fields = [
            'quiz_title', 'participant_name', 'score', 'total_points',
            'percentage', 'is_passed', 'submitted_at', 'attempt_number',
            'correct_answers_count', 'total_questions_count', 'answers'
        ]
    
    def get_answers(self, obj):
        # Only show answers if quiz allows showing results immediately
        if obj.quiz.show_results_immediately:
            return AnswerSerializer(obj.answers.all(), many=True).data
        return []