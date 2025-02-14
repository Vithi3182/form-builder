
from django import forms
from .models import Form, Question

class FormBuilderForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['title']

class QuestionForm(forms.ModelForm):
    main_question = forms.ModelChoiceField(
        queryset=Question.objects.all(),
        required=False,
        label='Main Question (if this question is hidden under another question)'
    )

    class Meta:
        model = Question
        fields = ['question_text', 'answer_type', 'main_question']
