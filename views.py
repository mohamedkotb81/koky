from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from .models import Todo

# Create your views here.

# ************* Old method of creating Views **********

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:6]
#     context = {'latest_question_list': latest_question_list,}
#     return render(request, "poll/index.html", context)
 
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'poll/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'poll/results.html', {'question': question})


# ***************** Generic Code of Views ************
class IndexView(generic.ListView):
    template_name = 'poll/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last nine published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:15]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'poll/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'poll/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'poll/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))


# def home(request):
#     todo_items = Todo.objects.all().order_by("-added_date")
#     return render(request. '/index.html', {'todo_items': todo_items})

# @csrf_exempt
# def add_todo(request):
#     current_date = timezone.now()
#     content = request.Post["content"]
#     created_obj = Todo.objects.creat(added_date = current_date, text = content)
#     length_of_todos = Todo.objects.all().count()
#     return HttpResponseRedirect("/")
