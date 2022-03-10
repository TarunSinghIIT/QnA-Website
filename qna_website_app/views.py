from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import Answer, Question
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.template import loader
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import AnswerForm

def questionlist(request):
    question_list = Question.objects.all()
    template = loader.get_template('qna_website_app/all_questions.html')
    context = {'question_list': question_list}
    return HttpResponse(template.render(context, request))

class QuestionList(LoginRequiredMixin, ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'qna_website_app/questionslist.html'
    def get_success_url(self):
        return reverse_lazy('questions')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = context['questions'].filter(user=self.request.user)
        return context

class AllQuestions(LoginRequiredMixin, ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'qna_website_app/all_questions.html'
    def get_success_url(self):
        return reverse_lazy('questions')

class LogIn(LoginView):
    template_name = 'qna_website_app/loginpage.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('questions')

class NewUser(FormView):
    template_name = 'qna_website_app/newuser.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('questions')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(NewUser, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('questions')
        return super(NewUser, self).get(*args, **kwargs)

def answeradd(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method=='POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer=Answer()
            answer.answer_text = form.cleaned_data.get('answer_text')
            answer.question = question
            answer.save()
    else:
        form = AnswerForm()
    return render(request, 'qna_website_app/answer_form.html', {'form':form})

class QuestionAdd(LoginRequiredMixin,CreateView):
    model = Question
    fields = ['question_title', 'question_text']
    success_url = reverse_lazy('questions')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(QuestionAdd, self).form_valid(form)

def questioninfo(request, question_id):
    question = Question.objects.get(id=question_id)
    answer = question.answer_set.all()
    return render(request, 'qna_website_app/answer_detail.html', {'question': question, 'answer': answer})

class QuestionChange(LoginRequiredMixin,UpdateView):
    model = Question
    fields = ['question_title', 'question_text']
    success_url = reverse_lazy('questions')

class QuestionDelete(LoginRequiredMixin,DeleteView):
    model = Question
    context_object_name = 'question'
    success_url = reverse_lazy('questions')

class AllAnswers(LoginRequiredMixin, ListView):
    model = Answer
    context_object_name = 'answers'
    template_name = 'qna_website_app/all_answers.html'
    def get_success_url(self):
        return reverse_lazy('answers')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answers'] = context['answers'].filter(question_id=2)
        return context

def answerinfo(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    return render(request, 'qna_website_app/answer_info.html', {'answer': answer})
