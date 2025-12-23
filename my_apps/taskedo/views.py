from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView

# Create your views here.




class TasksHomeView(TemplateView):
    template_name = 'taskedo/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Taskedo - Home'
        return context