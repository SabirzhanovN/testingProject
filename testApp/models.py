from django.db import models

from accounts.models import User


class Discipline(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.name


class Theme(models.Model):
    name = models.CharField(max_length=255)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.name


class Question(models.Model):
    topic = models.ForeignKey(Theme, on_delete=models.CASCADE)
    question_text = models.TextField()
    image = models.ImageField(upload_to="images/%Y/%m/%d/", null=True, blank=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    variant = models.CharField(max_length=512)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.variant


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

    cnt_questions = models.IntegerField()
    cnt_of_correct_answers = models.IntegerField(default=0)
    percent_of_correct_ans = models.DecimalField(max_digits=6, decimal_places=3)

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'Истории'

    def __str__(self):
        return str(self.user) + " " + str(self.theme)
