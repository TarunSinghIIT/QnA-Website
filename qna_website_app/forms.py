from django import forms

class AnswerForm(forms.Form):
    answer_text = forms.CharField(label = 'answer')
