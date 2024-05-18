from django.urls import reverse_lazy
from django.views import generic
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

class SignUpView(generic.CreateView):
  form_class = CustomUserCreationForm
  success_url = reverse_lazy('login')
  template_name = 'accounts/signup.html'

class CannotSignUpView(generic.TemplateView):
  template_name = 'accounts/cannot_signup.html'

class PrivateSettingsView(LoginRequiredMixin, UpdateView):
  model = CustomUser
  fields = ('dic_new_tab','dic_link')
  template_name = 'accounts/private_settings.html'
  success_url = reverse_lazy('english:index')
  # def get_context_data(self):
  #   context = super().get_context_data()
  #   context["edit_type"] = "update"
  #   return context
