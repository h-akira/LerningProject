from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import CustomUser as User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from .models import PageTable, PrivateDictionaryTable, SentenceTable, PublicEn2JpDictionaryTable
from .forms import PageForm, PageSettingsFormSet
import random
from django.conf import settings
# from django.views.generic import TemplateView
# 独自ライブラリ
from tree import Tree, gen_tree_htmls, gen_pages_ordered_by_tree
from language.english import text2SentenceTable, sentence2html
from urllib.parse import quote

def index(request):
  if request.user.is_authenticated:
    pages = PageTable.objects.filter(Q(user__is_superuser=True) | Q(user=request.user)).order_by("-last_updated")
  else:
    pages = PageTable.objects.filter(user__is_superuser=True).order_by("-last_updated")
  context = {
    "tree_htmls":gen_tree_htmls(request, User, PageTable, a_white=False),
    "nav_tree_htmls":gen_tree_htmls(request, User, PageTable, a_white=True),
    "pages": pages
  }
  return render(request, 'english/index.html', context)

def share_detail(request, share_code):
  try:
    page = PageTable.objects.get(share_code=share_code)
  except PageTable.DoesNotExist:
    return not_found(request)
  return detail(request, page.user.username, page.slug, share=True)

def detail_by_id(request, id):
  page = get_object_or_404(PageTable, pk=id)
  return detail(request, page.user.username, page.slug)

def detail(request, username, slug, share=False):
  try:
    user = User.objects.get(username=username)
    page = PageTable.objects.get(user=user, slug=slug)
  except User.objects.model.DoesNotExist:
    return not_found(request)
  except PageTable.DoesNotExist:
    if request.user.is_authenticated:
      if user == request.user:
        return redirect("english:create_with_slug",slug=slug)
      else:
        print("user != request.user")
        return not_found(request)
    else:
      print("not request.user.is_authenticated")
      return not_found(request)
  if not share and page.user != request.user and not user.is_superuser:
    print("not share and page.user != request.user and not user.is_superuser")
    return not_found(request)
  if page.user == request.user:
    edit = True
  else:
    edit = False
  if page.share:
    share_url = f"{settings.DOMAIN}{reverse('english:share_detail', args=[page.share_code])}"
  else:
    share_url = None
  sentence = SentenceTable.objects.filter(page=page)
  if request.user.is_authenticated:
    sentence_html = sentence2html(sentence, reverse, new_tab= user.dic_new_tab)
  else:
    sentence_html = sentence2html(sentence, reverse, new_tab=True)
  # print("--------------------")
  # print(sentence_html)
  # print("--------------------")
  context = {
    "page": page,
    "username": username,
    "slug": slug,
    "share": share,
    "share_url": share_url,
    "share_code": page.share_code,
    "edit": edit,
    "sentence_html": sentence_html,
    "nav_tree_htmls":gen_tree_htmls(request, User, PageTable, a_white=True),
  }
  return render(request, 'english/detail.html', context)

@login_required
def create(request, slug=None):
  if request.method == 'POST':
    form = PageForm(request.POST)
    if form.is_valid():
      print("valid")
      instance = form.save(commit=False)  # まだDBには保存しない
      instance.user = request.user  # userをセット
      instance.save()  # DBに保存
      sentence = form.cleaned_data['sentence']
      text2SentenceTable(sentence, instance, SentenceTable)
      if request.POST['action'] == 'update':
        return redirect("english:update",instance.user.username,instance.slug)
      elif request.POST['action'] == 'detail':
        return redirect("english:detail",instance.user.username,instance.slug)
      else:
        raise Exception
    else:
      print("invalid")
      raise Exception
  else:
    allow="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    length=32
    share_code = ''.join(random.choice(allow) for i in range(length))
    form = PageForm(
      initial={
        'slug': slug,
        'share_code': share_code,
      }
    )
    context = {
      "form": form,
      "type": "create",
      "author": True,
      "nav_tree_htmls":gen_tree_htmls(request, User, PageTable, a_white=True)
    }
    return render(request, 'english/edit.html', context)

def share_update(request, share_code):
  page = PageTable.objects.get(share_code=share_code)
  return update(request, page.user.username, page.slug, share=True)

def not_found(request, message="ページが見つかりません"):
  context = {
    "message": message,
  }
  return render(request, 'english/not_found.html', context)

@login_required
def update(request, username, slug, share=False):
  user = User.objects.get(username=username)
  try:
    page = PageTable.objects.get(user=user, slug=slug)
  except PageTable.DoesNotExist:
    return redirect("english:create_with_slug",slug=slug)
  if page.user == request.user or page.edit_permission:
    if request.method == 'POST':
      form = PageForm(request.POST, instance=page)
      if form.is_valid():
        instance = form.save(commit=False)  # まだDBには保存しない
        # instance.user = request.user  # userをセット
        instance.save()  # DBに保存
        sentence = form.cleaned_data['sentence']
        text2SentenceTable(sentence, instance, SentenceTable)
        if request.POST['action'] == 'update':
          if share:
            return redirect("english:share_update",page.share_code)
          else:
            return redirect("english:update",username,form.instance.slug)
        elif request.POST['action'] == 'detail':
          if share:
            return redirect("english:share_detail",page.share_code)
          else:
            return redirect("english:detail",username,form.instance.slug)
        else:
          raise Exception
    else:
      if page.user == request.user:
        author = True
      else:
        author = False
      form = PageForm(instance=page)
      sentence = SentenceTable.objects.filter(page=page)
      sentence_init = sentence2html(sentence, reverse, no_html=True)
      # sentence_init = ""
      # for s in sentence:
      #   sentence_init += f"{s.word} "
      form.fields['sentence'].initial = sentence_init
      context = {
        "id": page.id,
        "username": username,
        "slug": slug,
        "form": form,
        "type": "update",
        "author": author,
        "share": share,
        "share_code": page.share_code,
        "nav_tree_htmls":gen_tree_htmls(request, User, PageTable, a_white=True)
      }
      return render(request, 'english/edit.html', context)
  else:
    return redirect("english:index")

@login_required
def delete(request, id):
  page = get_object_or_404(PageTable, pk=id)
  if request.user == page.user or page.edit_permission:
    page.delete()
  return redirect("english:index")

@login_required
def page_settings(request):
  if request.method == "POST":
    pages = PageTable.objects.filter(user=request.user)
    formset = PageSettingsFormSet(request.POST, queryset=pages)
    if formset.is_valid():
      formset.save()
      if request.POST['action'] == 'continue':
        return redirect("english:page_settings")
      elif request.POST['action'] == 'end':
        return redirect("english:index")
      else:
        raise Exception
    else:
      print("---- Error ----")
      print("formset.errors:")
      print(formset.errors)
      print("formset.management_form.erros:")
      print(formset.management_form.errors)
      print("---------------")
      raise Exception
  else:
    # 階層図の並び順に並び替えられたQuerSet
    pages = gen_pages_ordered_by_tree(request, User, PageTable)
    # 一つのフォームにする
    formset = PageSettingsFormSet(queryset=pages)
    context = {
      "formset": formset,
      "pages": pages,
      "nav_tree_htmls":gen_tree_htmls(request, User, PageTable, a_white=True)
    }
    return render(request, 'english/page_settings.html', context)

def _get_mean_jp(word):
  public_en2jp_dic = PublicEn2JpDictionaryTable.objects.filter(word__iexact=word)
  if public_en2jp_dic.exists():
    if public_en2jp_dic.count() == 1:
      mean = public_en2jp_dic.first().mean
    else:
      mean = ""
      for i, d in enumerate(public_en2jp_dic):
        mean += f"{i+1}. {d.mean}\n"
      mean = mean[:-1]
  else:
    mean = "<未登録>"
  return mean

def s2dic(request, id):
  # ログインユーザーごとに辞書ページに移動（存在しなければ作成）
  s = get_object_or_404(SentenceTable, pk=id)
  if request.user.is_authenticated:
    if request.user.dic_link == "weblio":
      return redirect(f"https://ejje.weblio.jp/content/{s.lemma.lower()}")
    try:
      private_dic = PrivateDictionaryTable.objects.get(user=request.user, word=s.lemma, pos=s.pos)
    except PrivateDictionaryTable.DoesNotExist:
      mean_jp = _get_mean_jp(s.lemma)
      private_dic = PrivateDictionaryTable(
        user=request.user,
        word=s.lemma.lower(),  # 小文字に統一
        pos=s.pos,
        mean_jp=mean_jp,
        memo=""
      )
      private_dic.save()
    return redirect("english:private_dic_page_with_source", pk=private_dic.id,source_id=id)
  else:
    return redirect(f"https://ejje.weblio.jp/content/{s.lemma.lower()}")
    # public_dicを作るべき
  #   mean_jp = _get_mean_jp(s.lemma)
  #   private_dic=None
  # context = {
  #   "word": s.word,
  #   "lemma": s.lemma,
  #   "pos": s.pos,
  #   "private_dic": private_dic,
  #   "nav_tree_htmls":gen_tree_htmls(request, User, PageTable, a_white=True)
  # }
  # # return render(request, 'english/test_s2dic.html', context)
  # return redirect(f"https://ejje.weblio.jp/content/{s.lemma}")

@login_required
def private_dic_page(request, pk, source_id=None):
  private_dic = get_object_or_404(PrivateDictionaryTable, pk=pk)
  if private_dic.user != request.user:
    return redirect("english:index")
  if source_id:
    source = SentenceTable.objects.get(pk=source_id)
    private_dic.last_source = source
  private_dic.access_counter += 1
  private_dic.save()
  context = {
    "private_dic": private_dic,
    # "source": source,
    "nav_tree_htmls":gen_tree_htmls(request, User, PageTable, a_white=True)
  }
  print(private_dic.last_source.word)
  return render(request, 'english/private_dic.html', context)

class PrivateDictionaryEditView(LoginRequiredMixin, UpdateView):
  model = PrivateDictionaryTable
  fields = ('word','pos','star','mean_jp','memo')
  template_name = 'english/private_edit.html'
  def get_success_url(self):
    return reverse_lazy('english:private_dic_page', kwargs={'pk': self.object.pk})




