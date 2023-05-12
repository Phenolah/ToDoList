from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import List
from .forms import MyForm
# Create your views here.
class TaskList(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = List
    context_object_name= 'tasks'
    fields ='__all__'

    def get_queryset(self):
        return List.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ""
        if search_input:
            context['tasks'] = context['tasks'].filter(tittle__icontains = search_input)
            context['search_input'] = search_input
        return context
class TaskDetail(LoginRequiredMixin, DetailView):
    model = List
    template_name = 'taskdetail.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = List
    fields = ['tittle', 'description', 'complete']
    success_url = reverse_lazy("tasklist")
    template_name = 'taskform.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(self.success_url)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = List
    fields = ['tittle', 'description', 'complete']
    success_url = reverse_lazy("tasklist")
    template_name = 'taskform.html'

class TaskDelete(LoginRequiredMixin,  DeleteView):
    model = List
    success_url = reverse_lazy("tasklist")
    template_name = "confirmdelete.html"

class TaskLoginView(LoginView):
    template_name = "login.html"
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy("tasklist")

class TaskRegister(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasklist')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(TaskRegister,self).form_valid(form)
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasklist')
        return super().get(*args, **kwargs)

