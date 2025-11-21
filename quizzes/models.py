from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Quiz(models.Model):
    """
    Model representing a quiz.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    time_limit = models.PositiveIntegerField(
        help_text="Time limit in minutes (0 = no time limit)",
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1440)]  # Max 24 hours
    )
    is_active = models.BooleanField(default=True)
    passing_score = models.PositiveIntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Passing score percentage"
    )
    show_results_immediately = models.BooleanField(
        default=True,
        help_text="Show results to participants immediately after submission"
    )
    allow_retakes = models.BooleanField(default=False)
    max_attempts = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Maximum number of attempts allowed per participant"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.title

    @property
    def total_questions(self):
        return self.questions.count()

    @property
    def total_points(self):
        return self.questions.aggregate(total=models.Sum('points'))['total'] or 0

    @property
    def total_responses(self):
        return self.responses.count()


class Question(models.Model):
    """
    Model representing a question in a quiz.
    """
    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice'),
        ('TRUE_FALSE', 'True/False'),
        ('TEXT', 'Text Answer'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    order = models.PositiveIntegerField(default=1)
    points = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    is_required = models.BooleanField(default=True)
    explanation = models.TextField(
        blank=True,
        help_text="Explanation shown after answering (optional)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['quiz', 'order']
        unique_together = ['quiz', 'order']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}: {self.question_text[:50]}"

    def get_correct_answer(self):
        """Get the correct answer for MCQ and True/False questions."""
        if self.question_type == 'MCQ':
            return self.options.filter(is_correct=True).first()
        elif self.question_type == 'TRUE_FALSE':
            return self.options.filter(is_correct=True).first()
        return None


class MCQOption(models.Model):
    """
    Model representing multiple choice options for MCQ and True/False questions.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['question', 'order']
        unique_together = ['question', 'order']
        verbose_name = 'MCQ Option'
        verbose_name_plural = 'MCQ Options'

    def __str__(self):
        return f"{self.question} - Option {self.order}: {self.option_text[:30]}"
