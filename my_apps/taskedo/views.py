from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from my_apps.taskedo.forms import TaskForm
from my_apps.taskedo.models import Task
from django.contrib import messages

# Create your views here.


class TasksHomeView(TemplateView):
    template_name = 'taskedo/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Taskedo - Home'
        return context
    
    
    
class ListTasksView(ListView):
    model = Task
    template_name = 'taskedo/dashboard/list.html'
    context_object_name = 'tasks'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Taskedo - Listado de tareas'
        return context
    
    
class CreateTaskView(CreateView):
    model = Task
    template_name = 'taskedo/dashboard/create.html'
    form_class = TaskForm
    success_url = reverse_lazy('taskedo:list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "✅ Tarea creada correctamente.")
        return response
    
    def form_invalid(self, form):
        # Mostrar errores arriba con messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return self.render_to_response(self.get_context_data(form=form))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Taskedo - Crear nueva tarea'
        return context