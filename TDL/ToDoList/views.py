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



class TaskList(LoginRequiredMixin, ListView):
    # Template name for rendering the view
    template_name = 'index.html'
    # Model representing the data to be displayed
    model = List
    # Name used for the list of objects in the template context
    context_object_name = 'tasks'
    # Fields to be included in the view
    fields ='__all__'

    def get_queryset(self):
        """
        Returns the queryset for the view.
        Retrieves all objects from the List model.
        """
        return List.objects.all()

    def get_context_data(self, **kwargs):
        """
        Adds additional context variables to the view.
        Filters tasks by the logged-in user.
        Counts the number of incomplete tasks.
        Handles a search input to filter tasks by title.
        """
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ""
        if search_input:
            context['tasks'] = context['tasks'].filter(tittle__icontains=search_input)
            context['search_input'] = search_input

        return context
class TaskDetail(LoginRequiredMixin, DetailView):
    # Model representing the data to be displayed
    model = List
    # Template name for rendering the view
    template_name = 'taskdetail.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    # Model representing the data to be created
    model = List
    # Fields to be included in the form
    fields = ['tittle', 'description', 'complete']
    # URL to redirect to upon successful form submission
    success_url = reverse_lazy("tasklist")
    # Template name for rendering the form
    template_name = 'taskform.html'

    def form_valid(self, form):
        """
        Handles the validation and saving of the form.
        Sets the user of the form instance to the logged-in user.
        """
        form.instance.user = self.request.user
        form.save()
        return redirect(self.success_url)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    # Model representing the data to be updated
    model = List
    # Fields to be included in the form
    fields = ['tittle', 'description', 'complete']
    # URL to redirect to upon successful form submission
    success_url = reverse_lazy("tasklist")
    # Template name for rendering the form
    template_name = 'taskform.html'
 
class TaskDelete(LoginRequiredMixin, DeleteView):
    # Model representing the data to be deleted
    model = List
    # URL to redirect to upon successful deletion
    success_url = reverse_lazy("tasklist")
    # Template name for rendering the confirmation page
    template_name = "confirmdelete.html"

class TaskLoginView(LoginView):
    # Template name for rendering the login page
    template_name = "login.html"
    # Fields to be included in the login form
    fields = "__all__"
    # Setting to False to prevent redirecting authenticated users
    redirect_authenticated_user = False

    def get_success_url(self):
        """
        Returns the URL to redirect to upon successful login.
        """
        return reverse_lazy("tasklist")

class TaskRegister(FormView):
    # Template name for rendering the registration page
    template_name = 'register.html'
    # Form class for the registration form
    form_class = UserCreationForm
    # Setting to True to redirect authenticated users
    redirect_authenticated_user = True
    # URL to redirect to upon successful registration
    success_url = reverse_lazy('tasklist')

    def form_valid(self, form):
        """
        Handles the validation and saving of the registration form.
        Logs in the newly registered user.
        """
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(TaskRegister, self).form_valid(form)

    def get(self, *args, **kwargs):
        """
        Handles GET requests for the registration view.
        Redirects authenticated users to the tasklist.
        """
        if self.request.user.is_authenticated:
            return redirect('tasklist')
        return super().get(*args, **kwargs)
