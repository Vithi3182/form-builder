# Generated by Django 5.1.5 on 2025-02-12 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("formbuilder", "0004_question_conditional_option"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="answer_options",
            field=models.TextField(blank=True, default=""),
        ),
    ]
