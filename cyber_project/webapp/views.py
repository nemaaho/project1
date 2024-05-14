from django.http import Http404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


#class IndexView(generic.ListView):
    #template_name = 'webapp/index.html'
    #context_object_name = 'latest_question_list'

    #def get_queryset(self):
        #"""Return the last five published questions."""
        #return Question.objects.order_by('-pub_date')[:5]

@login_required
def indexView(request):
    question = get_object_or_404(Question, pk=1)
    context = {
        'question' : question,
    }
    return render(request, 'webapp/index.html', context)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'webapp/detail.html'


#class ResultsView(generic.DetailView):
    #model = Question
    #template_name = 'webapp/results.html'

@login_required
def resultsView(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    next_question = Question.objects.filter(id__gt=question_id).order_by('id').first()

    context = {
        'question': question,
        'next_question':next_question,
    }

    return render(request, 'webapp/results.html', context)

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'webapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('webapp:results', args=(question.id,)))

@login_required
def lastView(request):
    return render(request, 'webapp/last.html')
