from django.contrib import admin
from .models import Words,UserWords

class UserWordsAdmin(admin.ModelAdmin):
    list_display = ('word', 'translation', 'user', 'date_added')

class WordsAdmin(admin.ModelAdmin):
    list_display = ('word', 'translation', 'date_added')

admin.site.register(Words, WordsAdmin)
admin.site.register(UserWords, UserWordsAdmin)

