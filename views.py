from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required


from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

# Create your views here.

def home(request):
    '''render the home page'''
    return render(request, 'first_app/home.html')

# def questionhub(request):
#     '''show all questions in order of the date added'''
#     topics = Topic.objects.order_by('-date_added')
#     context = {'topics': topics}
#     return render(request, 'first_app/questionhub.html', context)

class QuestionhubView(generic.ListView):
    template_name = 'first_app/questionhub.html'
    context_object_name = 'questions'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-date_added')

def question(request, question_id):
    '''show a single question with its topic and explaination'''
    question = Question.objects.get(id=question_id)
    answer = question.answer_set.order_by('-date_added') 
    context = {'question': question, 'answer': answer}
    return render(request, 'first_app/question.html', context)

# class Questionview(generic.ListView):
#     '''generic view of view function question'''
#     template_name = 'first_app/question.html'

@login_required
def newquestion(request):
    '''adding a new question'''
    if request.method != 'POST':
        #if no data is submitted, create a blank for
        form = QuestionForm()
    else:
        # POST data is submitted; process date_added
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('first_app:questionhub'))

    context = {'form': form}
    return render(request, 'first_app/newquestion.html', context)

@login_required
def newanswer(request, question_id):
    '''add a new answer for a particular question'''
    question = Question.objects.get(id=question_id)

    if request.method != 'POST':
        #no data submitted; create a blank form
        form = AnswerForm()
    else:
        #POST data submitted; proccessing data
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            newanswer = form.save(commit=False)
            newanswer.question = question
            newanswer.save()
            return HttpResponseRedirect(reverse('first_app:question', args=[question_id]))

    context = {'question': question, 'form': form}
    return render(request, 'first_app/newanswer.html', context)

@login_required
def editanswer(request, answer_id):
    '''editing an answer'''
    answer = Answer.objects.get(id=answer_id)
    question = answer.question

    if request.method != 'POST':
        #when first start editing, pre-fill form with the current answer
        form = AnswerForm(instance=answer)
    else:
        #POST data submitted, proccesing date_added
        form = AnswerForm(instance=answer, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('first_app:question', args=[question.id]))

    context = {'answer': answer, 'question': question, 'form': form}
    return render(request, 'first_app/editanswer.html', context)

@login_required
def deleteanswer(request, answer_id):
    '''deleting an answer'''
    answer = Answer.objects.get(id=answer_id)
    question = answer.question

    if request.method == 'POST':
        answer.delete()
        return HttpResponseRedirect(reverse('first_app:question', args=[question.id]))

    context = {'answer':answer, 'question':question}
    return render(request, 'first_app/deleteanswer.html', context)
