from django.urls import path
from django.conf import settings
from . import views

app_name = 'accounts'

if settings.SIGNUP:
  urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
  ]
else:
  urlpatterns = [
    path('signup/', views.CannotSignUpView.as_view(), name='signup'),
  ]
urlpatterns.append(path('settings/<int:pk>/', views.PrivateSettingsView.as_view(), name='private_settings'))
