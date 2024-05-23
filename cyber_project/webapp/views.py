from django.http import Http404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
#from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'webapp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

resultslist = []

@login_required
def indexView(request):
    question = get_object_or_404(Question, pk=4)
    context = {
        'question' : question,
    }
    return render(request, 'webapp/index.html', context)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'webapp/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'webapp/results.html'

#@login_required
def resultsView(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    next_question = Question.objects.filter(id__gt=question_id).order_by('id').first()

    context = {
        'question': question,
        'next_question':next_question,
    }

    return render(request, 'webapp/results.html', context)

#@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        resultslist.append(selected_choice)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'webapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('webapp:results', args=(question.id,)))

#@login_required
def lastView(request):
    latest_question_list = Question.objects.all()
    combined_list = []
    for question, answer in zip(latest_question_list, resultslist):
        combined_list.append((question, answer))

    context = {
        'combined_list' : combined_list,
    }
    return render(request, 'webapp/last.html', context)

#class PasswordsChangeView(LoginRequiredMixin, PasswordChangeView):
class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('webapp:login')


#class UsernameChangeForm(LoginRequiredMixin, forms.ModelForm):
class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

#@login_required
def cleanUsername(self):
    username = self.cleaned_data.get('username')
    if User.objects.filter(username=username).exists():
        raise forms.ValidationError("This username is already taken.")
    return username

#@login_required
def changeUsername(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('webapp:login') 
    else:
        form = UsernameChangeForm(instance=request.user)
    return render(request, 'webapp/username.html', {'form': form})
