from collections import defaultdict
from datetime import timedelta, date

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView, ListView
from rest_framework.response import Response

from tasks.forms import RegisterForm

from tasks.models import Task

from tasks.mixins import RedirectIfAuthenticatedMixin


class HomeView(TemplateView, RedirectIfAuthenticatedMixin):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/app/tasks')
        return super().get(request, *args, **kwargs)



class RegisterView(CreateView, RedirectIfAuthenticatedMixin):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/app/tasks'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/app/tasks')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class LoginView(FormView, RedirectIfAuthenticatedMixin):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = '../app/tasks'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            return redirect('/app/tasks')
            
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class TasksView(ListView, LoginRequiredMixin):
    model = Task
    template_name = 'task_page.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(user=self.request.user)

        today = date.today()

        tomorrow = date.today() + timedelta(days=1)
        tasks = Task.objects.filter(due_date__gte=today)
        tasks_separated = defaultdict(list)
        for task in tasks:
            if task.due_date == today:
                tasks_separated['today'].append(task)
            elif task.due_date == tomorrow:
                tasks_separated['tomorrow'].append(task)
            else:
                tasks_separated['upcoming'].append(task)

        context['tasks_separated'] = tasks_separated

        return context

class OverdueTasksView(ListView, LoginRequiredMixin):
    model = Task
    template_name = 'overdue.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(user=self.request.user)

        today = date.today()

        tasks = Task.objects.filter(due_date__gte=today)
        tasks_separated = defaultdict(list)
        for task in tasks:
            if task.due_date < today:
                tasks_separated['overdue'].append(task)


        context['tasks_separated'] = tasks_separated

        return context
