
from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('app/tasks', TasksView.as_view(), name='main'),
    path('app/tasks/overdue', OverdueTasksView.as_view(), name='overdue'),



]
