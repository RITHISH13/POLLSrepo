from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question
from django.template import loader
from django.http import Http404
from. import views
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# Create your views here.
class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='latest_question_list'
    
    def get_queryset(self):
     return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')   
class DetailView(generic.DetailView):
    model=Question
    template_name='polls/details.html' 
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
class ResultsView(generic.DetailView):
       model=Question
       template_name ='polls/results.html'

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except(KeyError,Choice.DoesNotExist):
            return render(request,'polls/details.html',{'question':question,'error_message':"you didn't select a choice.",})
    else:
            selected_choice.votes+=1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))

def test(request):
    return HttpResponse("test")