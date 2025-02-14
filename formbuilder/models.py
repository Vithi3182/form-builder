# from django.db import models

# class Form(models.Model):
#     title = models.CharField(max_length=255)

# class Question(models.Model):
#     form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='questions')
#     question_text = models.CharField(max_length=500)
#     answer_type = models.CharField(max_length=20)
#     answer_options = models.TextField(blank=True, null=True)  # Comma-separated options for radio/checkbox
#     condition_trigger = models.BooleanField(default=False)  # Mark if this question reveals hidden questions
#     hidden_questions = models.ManyToManyField("self", blank=True, symmetrical=False)


#     def get_options(self):
#         return self.answer_options.split(",") if self.answer_options else []

# class FormSubmission(models.Model):
#     form = models.ForeignKey(Form, on_delete=models.CASCADE)
#     email = models.EmailField()
#     submitted_at = models.DateTimeField(auto_now_add=True)

# class Answer(models.Model):
#     submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE, related_name='answers')
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     answer_text = models.TextField()








from django.db import models

class Form(models.Model):
    title = models.CharField(max_length=255)

class Question(models.Model):
    ANSWER_TYPES = [
        ('text', 'Short Answer'),
        ('textarea', 'Paragraph'),
        ('radio', 'Multiple Choice (Radio)'),
        ('checkbox', 'Checkboxes'),
        ('integer', 'Integer'),  
    ]
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)
    answer_type = models.CharField(max_length=20,choices=ANSWER_TYPES)
    answer_options = models.TextField(blank=True, default="")  # Comma-separated options
    main_question = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, related_name='hidden_questions')
    conditional_option = models.CharField(max_length=255, blank=True, null=True) 

    def get_options(self):
        return self.answer_options.split(",") if self.answer_options else []

class FormSubmission(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    email = models.EmailField()
    submitted_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
