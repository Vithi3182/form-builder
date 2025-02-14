from django.urls import path
from . import views

urlpatterns = [
    path('', views.form_builder_view, name='form-builder'),
    path('view_form/<int:form_id>/',views.view_form,name='view_form'),
    path('edit_form/<int:form_id>/', views.edit_form, name='edit_form'),
    path('delete_form/<int:form_id>/', views.delete_form, name='delete_form'),

]
