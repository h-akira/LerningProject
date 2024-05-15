from django.urls import reverse_lazy
from django.views import generic
from .models import CustomUser
from .forms import CustomUserCreationForm

class SignUpView(generic.CreateView):
  form_class = CustomUserCreationForm
  success_url = reverse_lazy('login')
  template_name = 'accounts/signup.html'

class CannotSignUpView(generic.TemplateView):
  template_name = 'accounts/cannot_signup.html'
