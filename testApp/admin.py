from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Discipline, Theme, Question, Answer, History


class AnswerInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        correct_count = sum(form.cleaned_data.get('is_correct', False) for form in self.forms)
        if correct_count == 0:
            raise ValidationError('Хотябы 1 ответ должен быть правильным!')
        if correct_count == len(self.forms):
            raise ValidationError('Все варианты не могут быть правильными!')


class AnswerInline(admin.TabularInline):
    model = Answer
    formset = AnswerInlineFormSet


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.save()
            return
        correct_answers = obj.answer_set.filter(is_correct=True)
        if not correct_answers.exists():
            raise ValidationError('Хотябы 1 ответ должен быть правильным!')
        if correct_answers.count() == obj.answer_set.count():
            raise ValidationError('Все варианты не могут быть правильными!')
        super().save_model(request, obj, form, change)


admin.site.register(Discipline)
admin.site.register(Theme)
admin.site.register(Question, QuestionAdmin)


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'theme', 'cnt_questions', 'cnt_of_correct_answers', 'percent_of_correct_ans')