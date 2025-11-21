from rest_framework import serializers
from .models import Quiz, Question, MCQOption
from authentication.models import User


class MCQOptionSerializer(serializers.ModelSerializer):
    """
    Serializer for MCQ options.
    """
    class Meta:
        model = MCQOption
        fields = ['id', 'option_text', 'is_correct', 'order']

    def validate(self, attrs):
        question = self.context.get('question')
        if question and question.question_type not in ['MCQ', 'TRUE_FALSE']:
            raise serializers.ValidationError("Options can only be added to MCQ or True/False questions.")
        return attrs


class MCQOptionPublicSerializer(serializers.ModelSerializer):
    """
    Public serializer for MCQ options (without correct answer info).
    """
    class Meta:
        model = MCQOption
        fields = ['id', 'option_text', 'order']


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for questions (admin view with correct answers).
    """
    options = MCQOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'question_text', 'question_type', 'order', 'points', 
            'is_required', 'explanation', 'options', 'created_at'
        ]

    def validate(self, attrs):
        if attrs.get('order', 0) < 1:
            raise serializers.ValidationError("Question order must be positive.")
        return attrs


class QuestionPublicSerializer(serializers.ModelSerializer):
    """
    Public serializer for questions (without correct answers and explanations).
    """
    options = MCQOptionPublicSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'question_text', 'question_type', 'order', 'points', 
            'is_required', 'options'
        ]


class QuestionCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating questions with options.
    """
    options = MCQOptionSerializer(many=True, required=False)
    
    class Meta:
        model = Question
        fields = [
            'question_text', 'question_type', 'order', 'points', 
            'is_required', 'explanation', 'options'
        ]

    def validate(self, attrs):
        question_type = attrs.get('question_type')
        options = attrs.get('options', [])
        
        if question_type == 'MCQ':
            if len(options) < 2:
                raise serializers.ValidationError("MCQ questions must have at least 2 options.")
            if len(options) > 6:
                raise serializers.ValidationError("MCQ questions can have at most 6 options.")
            
            correct_count = sum(1 for option in options if option.get('is_correct', False))
            if correct_count != 1:
                raise serializers.ValidationError("MCQ questions must have exactly one correct answer.")
        
        elif question_type == 'TRUE_FALSE':
            if len(options) != 2:
                raise serializers.ValidationError("True/False questions must have exactly 2 options.")
            
            correct_count = sum(1 for option in options if option.get('is_correct', False))
            if correct_count != 1:
                raise serializers.ValidationError("True/False questions must have exactly one correct answer.")
        
        elif question_type == 'TEXT':
            if options:
                raise serializers.ValidationError("Text questions cannot have options.")
        
        return attrs

    def create(self, validated_data):
        options_data = validated_data.pop('options', [])
        question = Question.objects.create(**validated_data)
        
        for option_data in options_data:
            MCQOption.objects.create(question=question, **option_data)
        
        return question

    def update(self, instance, validated_data):
        options_data = validated_data.pop('options', None)
        
        # Update question fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update options if provided
        if options_data is not None:
            # Delete existing options
            instance.options.all().delete()
            
            # Create new options
            for option_data in options_data:
                MCQOption.objects.create(question=instance, **option_data)
        
        return instance


class QuizSerializer(serializers.ModelSerializer):
    """
    Serializer for quizzes (admin view).
    """
    questions = QuestionSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    total_questions = serializers.ReadOnlyField()
    total_points = serializers.ReadOnlyField()
    total_responses = serializers.ReadOnlyField()
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'created_by', 'created_by_name',
            'time_limit', 'is_active', 'passing_score', 'show_results_immediately',
            'allow_retakes', 'max_attempts', 'questions', 'total_questions',
            'total_points', 'total_responses', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class QuizPublicSerializer(serializers.ModelSerializer):
    """
    Public serializer for quizzes (without admin details).
    """
    questions = QuestionPublicSerializer(many=True, read_only=True)
    total_questions = serializers.ReadOnlyField()
    total_points = serializers.ReadOnlyField()
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'time_limit', 'passing_score',
            'show_results_immediately', 'allow_retakes', 'max_attempts',
            'questions', 'total_questions', 'total_points'
        ]


class QuizListSerializer(serializers.ModelSerializer):
    """
    Serializer for quiz list view (without questions).
    """
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    total_questions = serializers.ReadOnlyField()
    total_points = serializers.ReadOnlyField()
    total_responses = serializers.ReadOnlyField()
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'created_by_name', 'time_limit',
            'is_active', 'passing_score', 'allow_retakes', 'max_attempts',
            'total_questions', 'total_points', 'total_responses', 'created_at'
        ]


class QuizPublicListSerializer(serializers.ModelSerializer):
    """
    Public serializer for quiz list view.
    """
    total_questions = serializers.ReadOnlyField()
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'time_limit', 'total_questions'
        ]


class QuizCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating quizzes.
    """
    class Meta:
        model = Quiz
        fields = [
            'title', 'description', 'time_limit', 'is_active', 'passing_score',
            'show_results_immediately', 'allow_retakes', 'max_attempts'
        ]

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Quiz title must be at least 3 characters long.")
        return value.strip()

    def validate_time_limit(self, value):
        if value < 0:
            raise serializers.ValidationError("Time limit cannot be negative.")
        return value

    def validate_passing_score(self, value):
        if not 0 <= value <= 100:
            raise serializers.ValidationError("Passing score must be between 0 and 100.")
        return value