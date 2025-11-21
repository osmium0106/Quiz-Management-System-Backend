from django.contrib import admin
from .models import Quiz, Question, MCQOption


class MCQOptionInline(admin.TabularInline):
    model = MCQOption
    extra = 2


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'is_active', 'total_questions', 'total_points', 'created_at')
    list_filter = ('is_active', 'created_by', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'total_questions', 'total_points')
    ordering = ('-created_at',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question_text_short', 'question_type', 'order', 'points')
    list_filter = ('question_type', 'quiz')
    search_fields = ('question_text', 'quiz__title')
    inlines = [MCQOptionInline]
    ordering = ('quiz', 'order')
    
    def question_text_short(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question Text'


@admin.register(MCQOption)
class MCQOptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'option_text_short', 'is_correct', 'order')
    list_filter = ('is_correct', 'question__question_type')
    search_fields = ('option_text', 'question__question_text')
    
    def option_text_short(self, obj):
        return obj.option_text[:30] + '...' if len(obj.option_text) > 30 else obj.option_text
    option_text_short.short_description = 'Option Text'
