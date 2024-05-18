from django.db import models
from django.conf import settings
from accounts.models import CustomUser as User
# from django.utils.safestring import mark_safe
# from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from language.english import POS_CHOICES, POS_DICTIONARY

class PageTable(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  last_updated = models.DateTimeField(auto_now=True)
  slug = models.CharField(max_length=127)
  priority = models.FloatField(default=0)
  title = models.CharField(max_length=127)
  description = models.TextField(blank=True)
  share = models.BooleanField(default=False)
  share_code = models.CharField(
    max_length=127,
    null=True,
    blank=True,
    validators=[RegexValidator(r'^[a-zA-Z0-9]+$')],
    unique=True
  )
  def __str__(self):
    return self.title
  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=["user", "slug"],
        name="slug_unique"
      )
    ]

class PublicEn2JpDictionaryTable(models.Model):
  word = models.CharField(max_length=31, unique=True) 
  mean = models.CharField(max_length=255)

class SentenceTable(models.Model):
  page = models.ForeignKey(PageTable, on_delete=models.CASCADE)
  word = models.CharField(max_length=31)  # 文中の単語がそのまま入る
  lemma = models.CharField(max_length=31)  # 文中の単語の原型が入る
  pos = models.CharField(max_length=15, choices=POS_CHOICES)  # part of speech=品詞
  def pos_jp(self):
    return POS_DICTIONARY[self.pos]

class PrivateDictionaryTable(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  word = models.CharField(max_length=127)  # 原則は原型, 小文字
  pos = models.CharField(max_length=31, choices=POS_CHOICES)  # part of speech=品詞
  star = models.BooleanField(default=False)
  mean_jp = models.TextField(blank=True)  # 初期値は辞書を参照するがユーザーが編集できる
  # memo = models.TextField(blank=True)
  last_access = models.DateTimeField(auto_now=True)  # 更新も含む
  last_source = models.ForeignKey(SentenceTable, on_delete=models.SET_NULL, null=True, blank=True)
  access_counter = models.IntegerField(default=0)
  # public_en2jp_dictionary = models.ForeignKey(PublicEn2JpDictionaryTable, on_delete=models.CASCADE, null=True, blank=True)
  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=["user", "word", "pos"],
        name="word_unique"
      )
    ]
  def pos_jp(self):
    return POS_DICTIONARY[self.pos]



