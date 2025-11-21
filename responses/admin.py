from django.contrib import admin
from .models import QuizResponse, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ('is_correct', 'points_earned', 'answered_at')


@admin.register(QuizResponse)
class QuizResponseAdmin(admin.ModelAdmin):
    list_display = ('participant_name', 'quiz', 'score', 'percentage', 'is_passed', 'submitted_at', 'attempt_number')
    list_filter = ('is_passed', 'quiz', 'submitted_at', 'attempt_number')
    search_fields = ('participant_name', 'participant_email', 'quiz__title')
    readonly_fields = ('session_id', 'score', 'percentage', 'is_passed', 'started_at', 'submitted_at')
    ordering = ('-submitted_at',)
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('response', 'question', 'is_correct', 'points_earned', 'answered_at')
    list_filter = ('is_correct', 'question__question_type', 'answered_at')
    search_fields = ('response__participant_name', 'question__question_text')
    readonly_fields = ('is_correct', 'points_earned', 'answered_at')
