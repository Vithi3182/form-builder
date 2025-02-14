
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Form, Question, FormSubmission, Answer

# def form_builder_view(request):
#     forms = Form.objects.all()

#     if request.method == "POST":
#         action = request.POST.get("action")

#         if action == "add_question":
#             question_text = request.POST.get("question_text")
#             answer_type = request.POST.get("answer_type")
#             answer_options = request.POST.get("answer_options", "")
#             main_question_id = request.POST.get("main_question")

#             if question_text and answer_type:
#                 question_data = {
#                     "question_text": question_text,
#                     "answer_type": answer_type,
#                     "answer_options": answer_options if answer_type in ['radio', 'checkbox'] else "",
#                     "main_question": main_question_id
#                 }
#                 request.session['current_questions'].append(question_data)
#                 request.session.modified = True

#             return JsonResponse({"status": "success", "questions": request.session["current_questions"]})

#         elif action == "create_form":
#             title = request.POST.get("title")
#             if title:
#                 form = Form.objects.create(title=title)
#                 for q in request.session["current_questions"]:
#                     Question.objects.create(
#                         form=form,
#                         question_text=q["question_text"],
#                         answer_type=q["answer_type"],
#                         answer_options=q["answer_options"],
#                         main_question_id=q["main_question"] if q["main_question"] else None
#                     )
#                 request.session["current_questions"] = []
#                 request.session.modified = True
#                 return JsonResponse({"status": "form_created", "redirect_url": f"/view_form/{form.id}/"})

#         elif action == "refresh_form":
#             request.session["current_questions"] = []
#             request.session.modified = True
#             return JsonResponse({"status": "refreshed"})

#     return render(request, 'home.html', {"forms": forms, "questions": request.session.get("current_questions", [])})

def form_builder_view(request):
    forms = Form.objects.all()

    # Ensure session key 'current_questions' exists
    if "current_questions" not in request.session:
        request.session["current_questions"] = []

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add_question":
            question_text = request.POST.get("question_text")
            answer_type = request.POST.get("answer_type")
            answer_options = request.POST.get("answer_options", "")
            main_question_id = request.POST.get("main_question")

            if question_text and answer_type:
                question_data = {
                    "question_text": question_text,
                    "answer_type": answer_type,
                    "answer_options": answer_options if answer_type in ['radio', 'checkbox'] else "",
                    "main_question": main_question_id
                }

                # Append the question to the session list
                request.session["current_questions"].append(question_data)
                request.session.modified = True  # Ensure session updates

            return JsonResponse({"status": "success", "questions": request.session["current_questions"]})

        elif action == "create_form":
            title = request.POST.get("title")
            if title:
                form = Form.objects.create(title=title)

                # Ensure 'current_questions' is initialized before iterating
                for q in request.session.get("current_questions", []):
                    Question.objects.create(
                        form=form,
                        question_text=q["question_text"],
                        answer_type=q["answer_type"],
                        answer_options=q["answer_options"],
                        main_question_id=q["main_question"] if q["main_question"] else None
                    )

                # Reset the session after creating the form
                request.session["current_questions"] = []
                request.session.modified = True
                return JsonResponse({"status": "form_created", "redirect_url": f"/view_form/{form.id}/"})

        elif action == "refresh_form":
            request.session["current_questions"] = []
            request.session.modified = True
            return JsonResponse({"status": "refreshed"})

    return render(request, 'home.html', {"forms": forms, "questions": request.session.get("current_questions", [])})


def view_form(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    questions = Question.objects.filter(form=form)

    for question in questions:
        # Ensure options are properly formatted for radio & checkbox fields
        if question.answer_type in ['radio', 'checkbox']:
            question.options = question.answer_options.split(",") if question.answer_options else []

        # Ensure child questions are mapped correctly
        question.hidden_question_ids = [
            q.id for q in questions if q.main_question_id == question.id
        ]

    if request.method == "POST":
        email = request.POST.get("email")
        submission = FormSubmission.objects.create(form=form, email=email)

        for question in questions:
            answer_value = request.POST.getlist(f"question_{question.id}")
            Answer.objects.create(
                submission=submission,
                question=question,
                answer_text=", ".join(answer_value)
            )
        return JsonResponse({"status": "success", "message": "Form successfully submitted!"})

    return render(request, "form.html", {"form": form, "questions": questions})


# def edit_form(request, form_id):
#     form = get_object_or_404(Form, id=form_id)
#     questions = Question.objects.filter(form=form)

#     if request.method == "POST":
#         action = request.POST.get("action")

#         if action == "update_question":
#             question_id = request.POST.get("question_id")
#             question_text = request.POST.get("question_text")
#             answer_type = request.POST.get("answer_type")
#             answer_options = request.POST.get("answer_options", "").strip()
#             main_question_id = request.POST.get("main_question")
#             conditional_option = request.POST.get("conditional_option")

#             # Debugging prints
#             print("Updating Question ID:", question_id)
#             print("Received Answer Options:", answer_options)

#             question = get_object_or_404(Question, id=question_id)
#             question.question_text = question_text
#             question.answer_type = answer_type
            
#             if answer_type in ['radio', 'checkbox']:
#                 question.answer_options = answer_options
#             else:
#                 question.answer_options = ""

#             question.main_question_id = int(main_question_id) if main_question_id else None
#             question.conditional_option = conditional_option
#             question.save()

#             return JsonResponse({"status": "success"})

#         elif action == "add_question":  # ✅ Handling Add New Question Action
#             question_text = request.POST.get("question_text")
#             answer_type = request.POST.get("answer_type")
#             answer_options = request.POST.get("answer_options", "").strip()
#             main_question_id = request.POST.get("main_question")
#             conditional_option = request.POST.get("conditional_option")

#             # Debugging prints
#             print("Adding New Question:", question_text)
#             print("Answer Type:", answer_type)
#             print("Answer Options:", answer_options)
#             print("Main Question ID:", main_question_id)
#             print("Conditional Option:", conditional_option)

#             new_question = Question.objects.create(
#                 form=form,
#                 question_text=question_text,
#                 answer_type=answer_type,
#                 answer_options=answer_options if answer_type in ['radio', 'checkbox'] else "",
#                 main_question_id=int(main_question_id) if main_question_id else None,
#                 conditional_option=conditional_option
#             )

#             return JsonResponse({"status": "success", "question_id": new_question.id})

#     return render(request, "edit_form.html", {"form": form, "questions": questions})


def edit_form(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    questions = Question.objects.filter(form=form)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_question":
            question_id = request.POST.get("question_id")
            question_text = request.POST.get("question_text")
            answer_type = request.POST.get("answer_type")
            answer_options = request.POST.get("answer_options", "").strip()
            main_question_id = request.POST.get("main_question")
            conditional_option = request.POST.get("conditional_option")

            # Debugging
            print(f"Updating Question {question_id}: {question_text} ({answer_type})")
            print(f"Answer Options: {answer_options}")

            question = get_object_or_404(Question, id=question_id)
            question.question_text = question_text
            question.answer_type = answer_type
            
            if answer_type in ['radio', 'checkbox']:
                question.answer_options = answer_options  # ✅ Ensure options are stored
            else:
                question.answer_options = ""

            question.main_question_id = int(main_question_id) if main_question_id else None
            question.conditional_option = conditional_option
            question.save()

            return JsonResponse({"status": "success"})

        elif action == "delete_question":
            question_id = request.POST.get("question_id")
            question = get_object_or_404(Question, id=question_id)
            question.delete()
            return JsonResponse({"status": "success"})

    return render(request, "edit_form.html", {"form": form, "questions": questions})


def delete_form(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    form.delete()
    return redirect('form-builder')

