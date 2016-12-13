from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		#Return teh last 5 published ?s
		return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'
	

def vote(request, question_id):
	question = get_object_or_404(Question, pk = question_id)
	try:
		#request.POST is a dictionary-like object that lets you access submitted data by key name
		#returns the ID of the selected choice, as a string
		selected_choice = question.choice_set.get(pk =request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		#Redisplay the question voting form
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		#Always return an HttpResponse Redirect acter successfully dealing 
		#with POST data. This prevents data from being posted twice if a 
		#user hits the back button
		return HttpResponseRedirect(reverse('polls:results', args = (question.id,)))
