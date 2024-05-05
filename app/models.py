from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Test(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Набор тестов"
        verbose_name_plural = "Наборы тестов"


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Набор тестов")
    text = models.TextField(verbose_name="Текст вопроса")

    def __str__(self) -> str:
        return self.text

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    text = models.CharField(max_length=100, verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")

    def clean(self):
        if not Answer.objects.filter(question=self.question).exists():
            self.is_correct = True
        else:
            if not Answer.objects.filter(question=self.question, is_correct=True).exists():
                raise ValidationError("Хотя бы один ответ должен быть правильным")

            if self.is_correct and Answer.objects.filter(question=self.question, is_correct=True).count() > 1:
                raise ValidationError("Нельзя отметить все ответы как правильные")

    def __str__(self) -> str:
        return self.text

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Набор тестов")
    correct_answers = models.IntegerField(default=0, verbose_name="Количество правильных ответов")
    total_questions = models.IntegerField(default=0, verbose_name="Общее количество вопросов")
    percent_answers = models.IntegerField(default=0, verbose_name="Процент правильных ответов")

    def __str__(self) -> str:
        return f'{self.user}'

    class Meta:
        verbose_name = "Результат теста"
        verbose_name_plural = "Результаты тестов"
