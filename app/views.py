from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.db.models import Sum
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib import auth

from .models import Question, Answer, LikeToQuestion, LikeToAnswer, Profile, Tag, User
from .forms import *


def paginate(content_list, request):
    paginator = Paginator(content_list, 10)

    page = request.GET.get("page")
    content_list = paginator.get_page(page)

    return content_list


def index(request):
    questions = Question.objects.new()
    content = paginate(questions, request)

    tags = Tag.objects.hot()
    tags_list = list(tags)

    users = User.objects.all().order_by('-last_login')[:5]
    users_list = list(users)

    return render(request, "index.html", {"content": content, "tags": tags_list, "users": users_list})


@login_required
def ask(request):
    tags = Tag.objects.hot()
    tags_list = list(tags)

    users = User.objects.all().order_by('-last_login')[:5]
    users_list = list(users)

    if request.method == "GET":
        form = AskForm()

    if request.method == "POST":
        form = AskForm(data=request.POST)
        if form.is_valid():
            tags = form.save()
            profile = Profile.objects.filter(user=request.user).values("id")
            question = Question.objects.create(author_id=profile,
                                               title=form.cleaned_data["title"],
                                               text=form.cleaned_data["text"],
                                               date=datetime.today())
            for tag in tags:
                question.tags.add(tag)
                question.save()
            return redirect("question", pk=question.id)
    return render(request, "ask.html", {"tags": tags_list, "users": users_list, "form": form})


def login(request):
    next_p = request.GET.get("next", default="/")
    if request.user.is_authenticated:
        return redirect(next_p)

    tags = Tag.objects.hot()
    tags_list = list(tags)

    users = User.objects.all().order_by('-last_login')[:5]
    users_list = list(users)

    if request.method == "GET":
        form = LoginForm()

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(next_p)
            else:
                form.add_error(None, 'Sorry, wrong password or login!')
    return render(request, "login.html", {"tags": tags_list, "users": users_list, "form": form})


@login_required
def logout(request):
    auth.logout(request)
    next_p = request.GET.get("next", default="/")
    return redirect(next_p)


def question(request, pk):
    tags = Tag.objects.hot()
    tags_list = list(tags)

    users = User.objects.all().order_by('-last_login')[:5]
    users_list = list(users)

    _question = Question.objects.one_question(pk)
    answers = Answer.objects.filter(question=_question)
    content = paginate(answers, request)

    if request.method == "GET":
        form = AnswerForm()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % ('/login/', request.path))
        form = AnswerForm(data=request.POST)
        profile = Profile.objects.filter(user=request.user).values("id")
        if form.is_valid():
            answer = Answer.objects.create(question_id=_question.id,
                                           author_id=profile,
                                           text=form.cleaned_data["text"])
            return redirect(reverse("question", kwargs={"pk": _question.id}) + "?page="
                            + str(content.paginator.num_pages)+"#"+str(answer.id))

    return render(request, "question.html",
                  {"question": _question, "content": content, "tags": tags_list, "users": users_list, "form": form})


@login_required
def settings(request):
    tags = Tag.objects.hot()
    tags_list = list(tags)

    users = User.objects.all().order_by('-last_login')[:5]
    users_list = list(users)

    if request.method == "GET":
        user = request.user
        form = SettingsForm()
        if not user.is_authenticated:
            return HttpResponseForbidden()

    if request.method == "POST":
        form = SettingsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = request.user
            if user.is_authenticated:
                if form.cleaned_data["username"] != user.username and form.cleaned_data["username"] != "":
                    user.username = form.cleaned_data["username"]
                    user.save()
                    auth.login(request, user)
                    Profile.objects.filter(user=user).update(login=user.username)
                if form.cleaned_data["email"] != user.email and form.cleaned_data["email"] != "":
                    user.email = form.cleaned_data["email"]
                    user.save()
                    auth.login(request, user)
                if form.files.get("avatar"):
                    user.profile.avatar = form.files.get("avatar")
                    user.profile.save()
    return render(request, "settings.html", {"tags": tags_list, "users": users_list, "form": form})


def signup(request):
    tags = Tag.objects.hot()
    tags_list = list(tags)

    users = User.objects.all().order_by('-last_login')[:5]
    users_list = list(users)

    if request.method == "GET":
        form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            if user is not None:
                if form.files.get("avatar"):
                    user.profile.avatar = form.files.get("avatar")
                    user.profile.save()
                auth.login(request, user)
                return redirect("index")
    return render(request, "signup.html", {"tags": tags_list, "users": users_list, "form": form})


def tag(request, tag_name):
    tags = Tag.objects.hot()
    tags_list = list(tags)

    users = User.objects.all().order_by('-last_login')[:5]
    users_list = list(users)

    questions = Question.objects.all().filter(tags__name=tag_name)
    content = paginate(questions, request)

    return render(request, "tag.html", {"tag": tag_name, "content": content, "tags": tags_list, "users": users_list})


def hotquestions(request):
    tags = Tag.objects.hot()
    tags_list = list(tags)

    users = User.objects.all().order_by('-last_login')[:5]
    users_list = list(users)

    questions = Question.objects.hot()
    content = paginate(questions, request)

    return render(request, "hotquestions.html", {"content": content, "tags": tags_list, "users": users_list})


@require_POST
@login_required
def vote(request):
    data = request.POST
    action = data['action']

    if data['model'] == "question":
        question = Question.objects.get(id=data['id'])
        inc = LikeToQuestion.actions[action]

        q = LikeToQuestion.objects.values('question', 'user').filter(question=question, user=request.user.profile).count()
        if q >= 1:
            LikeToQuestion.objects.filter(question=question, user=request.user.profile).delete()
        else:
            LikeToQuestion.objects.create(question=question, user=request.user.profile, is_liked=inc)
        s = LikeToQuestion.objects.filter(question=question).aggregate(Sum('is_liked'))['is_liked__sum']
        question.rating = s
        question.save()
        return JsonResponse({'rating': Question.objects.get(id=data['id']).rating})
    if data['model'] == "answer":
        answer = Answer.objects.get(id=data['id'])
        inc = LikeToAnswer.actions[action]

        a = LikeToAnswer.objects.values('answer', 'user').filter(answer=answer, user=request.user.profile).count()
        if a >= 1:
            LikeToAnswer.objects.filter(answer=answer, user=request.user.profile).delete()
        else:
            LikeToAnswer.objects.create(answer=answer, user=request.user.profile, is_liked=inc)
        s = LikeToAnswer.objects.filter(answer=answer).aggregate(Sum('is_liked'))['is_liked__sum']
        answer.rating = s
        answer.save()
        return JsonResponse({'rating': Answer.objects.get(id=data['id']).rating})


@require_POST
@login_required
def correct(request):
    data = request.POST
    answer = Answer.objects.get(id=data['id'])
    if request.user.profile == Question.objects.get(id=data['qid']).author:
        if data['correct'] == 'true':
            answer.correct = True
        else:
            answer.correct = False
        answer.save()
    return JsonResponse({'correct': Answer.objects.get(id=data['id']).correct})


def test(request):
    return render(request, "sample.html")
