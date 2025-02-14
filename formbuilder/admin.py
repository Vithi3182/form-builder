from django.contrib import admin
from .models import Form,Question,FormSubmission,Answer

# Register your models here.
admin.site.register(Form)
admin.site.register(Question)
admin.site.register(FormSubmission)
admin.site.register(Answer)