from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Discipline, Theme, Question, Answer, History


def get_disc_themes_for_menu():
    disciplines = Discipline.objects.all()
    lst_for_menu = []
    for discipline in disciplines:
        dict_for_manu = {
            'discipline': discipline,
            'themes': Theme.objects.filter(discipline=discipline)
        }

        lst_for_menu.append(dict_for_manu)

    return lst_for_menu


def index(request):
    context = {
        'lst_for_menu': get_disc_themes_for_menu()
    }

    return render(request, 'testApp/index.html', context)


def test_detail(request, id):
    theme = Theme.objects.get(id=id)
    questions_cnt = len(Question.objects.filter(topic=theme.id))

    context = {
        'theme': theme,
        'questions_cnt': questions_cnt,
        'lst_for_menu': get_disc_themes_for_menu()
    }

    return render(request, 'testApp/test_detail.html', context)


def testing(request, ids):
    if '-' in ids:
        id, history_id = ids.split('-')
        id, history_id = int(id), int(history_id)
        history = History.objects.get(id=history_id)
    else:
        id, history_id = int(ids), None

    if request.method == 'POST':
        if request.POST['next_page'] != 'last':
            if len(request.POST) == 3:
                messages.error(request, "Отметьте хотябы 1 ответ")
                return redirect(f'/testing/{id}-{history_id}/?page={int(request.POST["next_page"]) - 1}')
            else:
                if len(request.POST) >= len(Answer.objects.filter(question=request.POST['question_id']))+3:
                    messages.error(request, "Нельзя отмечать все варианты!")
                    return redirect(f'/testing/{id}-{history_id}/?page={int(request.POST["next_page"]) - 1}')
                else:
                    students_answers = []
                    for i in range(1, len(request.POST) - 2):
                        students_answers.append(int(list(request.POST)[i]))

                    correct_answers = []
                    for i in Answer.objects.filter(question=request.POST['question_id']):
                        if i.is_correct:
                            correct_answers.append(i.id)

                    if sorted(students_answers) == sorted(correct_answers):
                        history.cnt_of_correct_answers += 1
                        history.save()

            return redirect(f'/testing/{id}-{history_id}/?page={request.POST["next_page"]}')
        else:
            students_answers = []
            for i in range(1, len(request.POST) - 2):
                students_answers.append(int(list(request.POST)[i]))

            correct_answers = []
            for i in Answer.objects.filter(question=request.POST['question_id']):
                if i.is_correct:
                    correct_answers.append(i.id)

            if sorted(students_answers) == sorted(correct_answers):
                history.cnt_of_correct_answers += 1
                history.save()

            return redirect('result', history.id)

    if 'page' not in str(request.build_absolute_uri()):
        history = History.objects.create(
            user=request.user,
            theme=Theme.objects.get(id=id),
            cnt_questions=len(Question.objects.filter(topic=id)),
            percent_of_correct_ans=0
        )

        history.save()

    questions = Question.objects.filter(topic=id)

    test = []
    for question in questions:
        test_with_variants = {
            'question': question,
            'variants': Answer.objects.filter(question=question.id)
        }

        test.append(test_with_variants)

    paginator = Paginator(test, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'history': history,
        'theme': id,
        'test': page_obj
    }

    return render(request, 'testApp/testing.html', context)


def result(request, id):
    history = History.objects.get(id=id)
    history.percent_of_correct_ans = (history.cnt_of_correct_answers * 100) / history.cnt_questions
    history.save()

    context = {
        'history': history
    }

    return render(request,'testApp/result.html', context)
