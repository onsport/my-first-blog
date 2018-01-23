from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:10]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # отобразить форму голосования заново
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "Вы не выбрали ответ. Пожалуйста, выберите один из вариантов.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # всегда выполняйте возврат HttpResponseRedirect после успешной обработки POST
        # Это предотвращает двойное использование данных
        # если пользователь нажимает кнопку Назад
        return HttpResponseRedirect(reverse('index'))
