from django.db import models
from django.contrib.auth import get_user_model
from quizzes.models import Quiz, Question, MCQOption

User = get_user_model()


class QuizResponse(models.Model):
    """
    Model representing a participant's response to a quiz.
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='responses')
    participant_name = models.CharField(max_length=100)
    participant_email = models.EmailField()
    session_id = models.CharField(max_length=100, unique=True)  # Unique session identifier
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total_points = models.PositiveIntegerField(default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_passed = models.BooleanField(default=False)
    time_taken = models.DurationField(null=True, blank=True)  # Time taken to complete
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    attempt_number = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['-started_at']
        verbose_name = 'Quiz Response'
        verbose_name_plural = 'Quiz Responses'
        unique_together = ['quiz', 'participant_email', 'attempt_number']

    def __str__(self):
        return f"{self.participant_name} - {self.quiz.title} (Attempt {self.attempt_number})"

    def calculate_score(self):
        """Calculate and update the score based on answers."""
        total_score = 0
        total_possible = self.quiz.total_points

        for answer in self.answers.all():
            if answer.is_correct:
                total_score += answer.question.points

        self.score = total_score
        self.total_points = total_possible
        self.percentage = (total_score / total_possible * 100) if total_possible > 0 else 0
        self.is_passed = self.percentage >= self.quiz.passing_score
        self.save()

    @property
    def correct_answers_count(self):
        return self.answers.filter(is_correct=True).count()

    @property
    def total_questions_count(self):
        return self.quiz.total_questions


class Answer(models.Model):
    """
    Model representing an answer to a specific question in a quiz response.
    """
    response = models.ForeignKey(QuizResponse, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(
        MCQOption, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        help_text="Selected option for MCQ/True-False questions"
    )
    text_answer = models.TextField(
        blank=True,
        help_text="Text answer for open-ended questions"
    )
    is_correct = models.BooleanField(default=False)
    points_earned = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['response', 'question']
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return f"{self.response.participant_name} - {self.question}"

    def save(self, *args, **kwargs):
        """Override save to automatically calculate correctness and points."""
        if self.question.question_type in ['MCQ', 'TRUE_FALSE']:
            if self.selected_option and self.selected_option.is_correct:
                self.is_correct = True
                self.points_earned = self.question.points
            else:
                self.is_correct = False
                self.points_earned = 0
        elif self.question.question_type == 'TEXT':
            # For text questions, correctness needs to be manually evaluated
            # This could be expanded with AI-based evaluation in the future
            self.points_earned = self.question.points if self.is_correct else 0
        
        super().save(*args, **kwargs)
