from django.urls import path, re_path
from .views import index, detail, create, update, delete, page_settings, share_detail, not_found, s2dic, private_dic_page, PrivateDictionaryEditView, detail_by_id, public_en2jp_dic_page, public_en2jp_dic_page_from_sentence, private_history

app_name = "english"

urlpatterns = [
  path('',index, name='index'),
  path('create/',create, name='create'),
  path('not_found/',not_found, name='not_found'),
  path('share/<str:share_code>/', share_detail, name='share_detail'),
  path('detail_by_id/<int:id>/', detail_by_id, name='detail_by_id'),
  re_path(r'^create/(?P<slug>.+)/$', create, name='create_with_slug'),
  path('settings/',page_settings, name='page_settings'),
  re_path(r'^detail/(?P<username>[^/]+)/(?P<slug>.+)/$', detail, name='detail'),
  re_path(r'^update/(?P<username>[^/]+)/(?P<slug>.+)/$', update, name='update'),
  path('delete/<int:id>/', delete, name='delete'),
  path('s/<int:id>/', s2dic, name='s2dic'),
  path('private/detail/<int:pk>/', private_dic_page, name='private_dic_page'),
  # path('private/detail/<int:pk>/<str:source_id>/', private_dic_page, name='private_dic_page_with_source'),
  path('private/edit/<int:pk>/', PrivateDictionaryEditView.as_view(), name='private_dic_edit'),
  path('public/en2jp/<str:word>/', public_en2jp_dic_page, name='public_en2jp'),
  path('s/<int:source_id>/public/', public_en2jp_dic_page_from_sentence, name='public_en2jp_from_sentence'),
  path('private/history/', private_history, name='private_history'),
]
