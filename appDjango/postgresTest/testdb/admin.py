from django.contrib import admin

from . import models

class QuestAdmin(admin.ModelAdmin):
    list_display = ("pk", "quest", "answer")
    list_editable = ("quest", "answer")

admin.site.register(models.question, QuestAdmin)
