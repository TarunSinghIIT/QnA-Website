from xml.etree.ElementTree import Comment
from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import User

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    question_title = models.CharField(max_length=200)
    question_text = models.TextField(null=True)
    asked_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(null=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    answer_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.answer_text

class CommentOnAnswer(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    comment_text = models.TextField(null=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    comment_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_text
