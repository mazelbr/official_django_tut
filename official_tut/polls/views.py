from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Question, Choice
from django.urls import reverse


def index(request):
    question_list = Question.objects.order_by("-pub_date")
    context = {"latest_question_list" : question_list}
    return render( request, "polls/index.html", context)

def details(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    return render(request,  "polls/details.html", {"question": q})
    

def results(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    choices = question.choice_set.all()
    return render(request, "polls/vote.html", {"question": question, "choices" : choices})
    
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice= question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls:detail", {"question_id": question.id, "error_message": "You did not take choice"})
    else:
        choice.votes += 1
        choice.save()
        return  HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
