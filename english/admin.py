from django.contrib import admin
from .models import PageTable, SentenceTable, PublicEn2JpDictionaryTable, PrivateDictionaryTable

admin.site.register(PageTable)
admin.site.register(SentenceTable)
admin.site.register(PublicEn2JpDictionaryTable)
admin.site.register(PrivateDictionaryTable)
