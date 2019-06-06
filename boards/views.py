from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import CreateView
from .forms import NewUserForm
from .models import Board, Topic, Post


def index(request):
    context = {
        'boards': Board.objects.all(),
    }
    return render(request, 'index.html', context)


def board(request, name):
    context = {
        'board': Board.objects.get(name=name),
    }
    return render(request, 'board.html', context)


def thread(request, name):
    context = {
        'thread': Topic.objects.get(title=name)
    }
    return render(request, 'thread.html', context)


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'New account created: {username}')
            login(request, user)
            return redirect('/')
        else:
            for msg in form.error_messages:
                messages.error(request, f'{msg}: {form.error_messages[msg]}')

            context = {
                'form': form
            }
            return render(request, 'register.html', context)

    form = NewUserForm()
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


def logout_request(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('/')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}')
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')

    form = AuthenticationForm()
    context = {
        "form": form
    }
    return render(request, 'login.html', context)


@method_decorator(staff_member_required, name='dispatch')
class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    template_name = 'topic_form.html'
    fields = ['board', 'title']
    success_url = '/topic/{title}'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.add_message(self.request, messages.SUCCESS, 'Thread created successfully!')
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['topic', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.add_message(self.request, messages.SUCCESS, 'Post added successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')
