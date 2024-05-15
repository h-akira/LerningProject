from django.db import models
from django.conf import settings
from accounts.models import CustomUser as User
# from django.utils.safestring import mark_safe
# from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from language.english import POS_CHOICES

class PageTable(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  last_updated = models.DateTimeField(auto_now=True)
  slug = models.CharField(max_length=127)
  priority = models.FloatField(default=0)
  title = models.CharField(max_length=127)
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

class PrivateDictionaryTable(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  word = models.CharField(max_length=127)  # 原則は原型
  pos = models.CharField(max_length=31)  # part of speech=品詞
  star = models.BooleanField(default=False)
  memo = models.TextField()
  last_access = models.DateTimeField(auto_now=True)  # 更新も含む
  access_counter = models.IntegerField(default=0)
  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=["user", "word", "pos"],
        name="word_unique"
      )
    ]

class SentenceTable(models.Model):
  page = models.ForeignKey(PageTable, on_delete=models.CASCADE)
  word = models.CharField(max_length=31)  # 文中の単語がそのまま入る
  lemma = models.CharField(max_length=31)  # 文中の単語の原型が入る
  pos = models.CharField(max_length=15, choices=POS_CHOICES)  # part of speech=品詞
  # 逆引きを可能にするためにはProvateDictionaryTableもForeignKeyで持つ必要があるがどうしよう


