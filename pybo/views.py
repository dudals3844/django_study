from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator

from .forms import QuestionForm
from .models import Question

# Create your views here.

def index(request):
    '''
    print pybo list
    :param request:
    :return:
    '''
    # Input parameter
    page = request.GET.get('page', '1')

    # Reference
    question_list = Question.objects.order_by('-create_date')

    # Paging
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'question_detail.html', context)


def answer_create(request, question_id):
    '''
    Answer
    :param request:
    :param question_id:
    :return:
    '''
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('pybo:detail', question_id=question.id)

def question_create(request):
    '''
    Add pybo quesion
    :param request:
    :return:
    '''
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')

    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'question_form.html', context)