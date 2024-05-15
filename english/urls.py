from django.urls import path, re_path
from .views import index, detail, create, update, delete, page_settings, share_detail, not_found, word2dic

app_name = "english"

urlpatterns = [
  path('',index, name='index'),
  path('create/',create, name='create'),
  path('not_found/',not_found, name='not_found'),
  path('share/<str:share_code>/', share_detail, name='share_detail'),
  re_path(r'^create/(?P<slug>.+)/$', create, name='create_with_slug'),
  path('settings/',page_settings, name='page_settings'),
  re_path(r'^detail/(?P<username>[^/]+)/(?P<slug>.+)/$', detail, name='detail'),
  re_path(r'^update/(?P<username>[^/]+)/(?P<slug>.+)/$', update, name='update'),
  path('delete/<int:id>/', delete, name='delete'),
  path('word/<str:word>/<str:lemma>/<str:pos>/', word2dic, name='word2dic'),
]
