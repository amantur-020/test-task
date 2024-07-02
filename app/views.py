from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from app.forms import UserRegistrationForm, UserAuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.views.generic.base import View
from .models import Question, Test, Answer, TestResult
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout


class RegisterUserView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'app/registration.html'
    success_url = reverse_lazy('login')


class LoginUserView(LoginView):
    form_class = UserAuthenticationForm
    template_name = 'app/login.html'
    
    def get_success_url(self):
        return reverse_lazy('tests')

class BaseView(View):
    def get(self, request):
        return render(request, 'app/home.html')

class TestListView(LoginRequiredMixin, ListView):
    model = Test
    template_name = 'app/tests.html'
    context_object_name = 'tests'
    login_url = '/login/'

    def get_queryset(self):
        current_user = self.request.user
        TestResult.objects.filter(user=current_user).delete()
        return super().get_queryset()



class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = 'app/questions.html'
    context_object_name = 'question'
    login_url = '/login/'

    def get_queryset(self):
        current_user = self.request.user
        TestResult.objects.filter(user=current_user).delete()
        return super().get_queryset()


    def post(self, request, *args, **kwargs):
        answer_id = request.POST.get('answer')
        question_id = request.POST.get('question_id') 
        answer = Answer.objects.get(id=answer_id) 
        user = request.user
        test = self.get_object().test 
        test_result, correct = TestResult.objects.get_or_create(user=user, test=test)
        if answer.is_correct:
            test_result.correct_answers += 1
        test_result.total_questions += 1
        test_result.percent_answers = (test_result.correct_answers / test_result.total_questions) * 100
        test_result.save()
        
        next_question = Question.objects.filter(test=test, id__gt=question_id).first()
        if next_question:
            return redirect('questions', pk=next_question.pk)
        else:
            return redirect('test_result', pk=test_result.pk)
        
    
    
class TestResultDetailView(LoginRequiredMixin, DetailView):
    model = TestResult
    template_name = 'app/test_result.html'
    context_object_name = 'test_result'
    login_url = '/login/'


def logout_user(request):
    logout(request)
    return redirect('home')