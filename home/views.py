from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from core import settings
from .forms import StudentsForm, UpdateStudentForm
from .models import Students

from .constants import (ERROR_STUDENT_NOT_UPDATED, HOME_PAGE_TEMPLATE,
                        INDEX_TEMPLATE,
                        ADD_STUDENTS_TEMPLATE,
                        UPDATE_STUDENTS_TEMPLATE,
                        UPDATE_STUDENT_TEMPLATE,
                        ERROR_STUDENT_EXISTS,
                        SUCCESS_STUDENT_ADDED,
                        ERROR_STUDENT_NOT_REGISTERED,
                        SUCCESS_STUDENT_DELETED,
                        SUCCESS_STUDENT_UPDATED,
                        ADD_STUDENTS_URL, UPDATE_STUDENTS_URL, )


@login_required
def homePage(request):
    return render(request, HOME_PAGE_TEMPLATE, )


@login_required
def students(request):
    data = Students.objects.all()
    return render(request, INDEX_TEMPLATE, {"data": data})


@login_required
def addStudents(request):
    if request.method == "POST":
        form = StudentsForm(request.POST)
        email = request.POST["email"]

        if form.is_valid():
            # Check if a student with the same email already exists below check is not working now, chcking email
            # exist above email = form.cleaned_data['email']
            try:
                Students.objects.get(email=email)
                messages.error(
                    request, ERROR_STUDENT_EXISTS
                )
            except ObjectDoesNotExist:
                form.save()
                messages.success(request, SUCCESS_STUDENT_ADDED)
            return redirect(ADD_STUDENTS_URL)
        else:
            messages.error(
                request, ERROR_STUDENT_NOT_REGISTERED
            )

    else:
        form = StudentsForm()
    return render(request, ADD_STUDENTS_TEMPLATE, {"form": form})


@login_required
def updateStudentsPage(request):
    data = Students.objects.all()
    return render(request, UPDATE_STUDENTS_TEMPLATE, {"data": data})


def delete_student(request, student_email, ):
    try:
        student = Students.objects.get(email=student_email)
        student_name = student.name
        student.delete()
        messages.success(request, f"{student_name} {SUCCESS_STUDENT_DELETED}")
        return redirect(UPDATE_STUDENTS_URL)
    except Students.DoesNotExist:
        return HttpResponse("Student not found", status=404)


@login_required
def update_student(request, student_email):
    student = Students.objects.get(email=student_email)
    student_name = student.name
    updated = False
    if request.method == "POST":
        form = UpdateStudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            updated = True
            messages.success(request, f"{student_name} {SUCCESS_STUDENT_UPDATED}")
            return render(
                request,
                UPDATE_STUDENT_TEMPLATE,
                {"form": form, "student": student, "updated": updated},
            )
    else:
        messages.error(request, ERROR_STUDENT_NOT_UPDATED)
        form = UpdateStudentForm(instance=student, initial={})
    return render(request, UPDATE_STUDENT_TEMPLATE, {"form": form, "student": student, "updated": updated}, )


@login_required
def students_pagination(request):
    page_start = request.GET.get('page', 1)
    items_per_page = 5 

    student_list = Students.objects.all()
    paginator = Paginator(student_list, items_per_page)

    try:
        paginated_data = paginator.page(page_start)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)

    return render(request, 'student_pagination.html', {'paginated_data': paginated_data})
