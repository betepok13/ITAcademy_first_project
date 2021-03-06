from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Choice, Question

__all__ = {'index', 'detail', 'vote'}


def index(request: HttpRequest) -> HttpResponse:
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = dict(latest_question_list=latest_question_list)
    return render(request, 'polls/index.html', context)


def detail(request: HttpRequest, question_id: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', dict(question=question))


def results(request: HttpRequest, question_id: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', dict(question=question))


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    if 'choice' not in request.POST:
        return render(request, 'polls/detail.html', dict(
            question=question,
            error_message="You didn't select a choice.",
        ))

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', dict(
            question=question,
            error_message="You didn't select a choice.",
        ))

    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
