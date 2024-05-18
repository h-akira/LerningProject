from django.db import models
from django.contrib.auth.models import AbstractUser

DIC_LINK_CHOICES = (
  ('private dictionary', 'Private Dictionary'),
  ('weblio', 'Weblio'),
)

class CustomUser(AbstractUser):
  dic_new_tab = models.BooleanField(default=True)
  dic_link  = models.CharField(max_length=31, choices=DIC_LINK_CHOICES, default='private dictionary')
