from django.urls import path
from . import views
from .views import AllAnswers, AnswerInfo, LogIn, NewUser, QuestionList, QuestionAdd, QuestionInfo, QuestionChange, QuestionDelete, AllQuestions
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', QuestionList.as_view(), name='questions'),
    path('login/', LogIn.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('new_user/', NewUser.as_view(), name='newuser'),
    path('question_add/', QuestionAdd.as_view(), name='question_add'),
    path('question/<int:question_id>/', views.questioninfo, name='question'),
    path('question_change/<int:pk>/', QuestionChange.as_view(), name='question_change'),
    path('task-delete/<int:pk>/', QuestionDelete.as_view(), name='question_delete'),
    path('all_questions/', views.questionlist, name='all_questions'),
    path('all_answers/', AllAnswers.as_view(), name='all_answers'),
    path('answer/<int:answer_id>/', AnswerInfo.as_view(), name='answer'),
]
