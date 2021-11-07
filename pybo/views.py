from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import QuestionForm, AnswerForm, CommentForm
from .models import Question, Answer, Comment


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


@login_required(login_url='common:login')
def answer_create(request, question_id):
    '''
    Answer
    :param request:
    :param question_id:
    :return:
    '''
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'question_detail.html', context)


@login_required(login_url='common:login')
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
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')

    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    '''
    modify question function
    :param request:
    :param question_id:
    :return:
    '''

    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "No Auth to Modify")
        return redirect('pybo:detail', question_id=question_id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question_id)

    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    pybo 답변수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    '''
    pybo answer delete
    :param request:
    :param answer_id:
    :return:
    '''
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "No Auth to Delete")
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)


@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    '''
    Add answer question
    :param request:
    :param question_id:
    :return:
    '''
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('pybo:detail', question_id=question_id)

    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    '''
    pybo comment modify
    :param request:
    :param comment_id:
    :return:
    '''
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "No Auth to Modify")
        return redirect('pybo:detail', question_id=comment.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment)

    context = {'form': form}
    return render(request, 'comment_form.html', context)


def comment_delete_question(request, comment_id):
    pass
