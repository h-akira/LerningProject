from django import forms
from django.forms import modelformset_factory
from .models import PageTable

class PageForm(forms.ModelForm):
  # sentence = forms.TextInput()
  # sentenceは必須ではない
  sentence = forms.CharField(
    widget=forms.Textarea(
      attrs={
        'style': 'width: 100%; height: auto;'
      }
    ) 
  )
  class Meta:
    model = PageTable
    fields = (
      "slug",
      "priority",
      "title",
      "description",
      "share",
      "share_code",
    )
    widgets = {
      'title': forms.TextInput(
        attrs={
          'style': 'width: 100%; height: auto; font-size: 2rem;'
        }
      ),
      'slug': forms.TextInput(
        attrs={
          'style': 'width: 500px;'
        }
      ),
      'share_code': forms.TextInput(
        attrs={
          'style': 'width: 500px;'
        }
      ),
      # 'description': forms.Textarea(
      'description': forms.TextInput(
        attrs={
          'style': 'width: 100%; height: auto;'
        }
      ),
    }

class PageSettingsForm(forms.ModelForm):
  class Meta:
    model = PageTable
    fields = ["title", "slug", "priority"]
    widgets = {
      'title': forms.TextInput(attrs={'style': 'width: 300px;'}),
      'slug': forms.TextInput(attrs={'style': 'width: 220px;'}),
      'priority': forms.NumberInput(attrs={"step":"0.1", "style": "width:70px;"}),
    }

PageSettingsFormSet = modelformset_factory(
  PageTable, 
  form=PageSettingsForm,
  extra=0
)
