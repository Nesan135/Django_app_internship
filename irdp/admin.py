from django.contrib import admin

from .models import Ahli

class AhliAdmin(admin.ModelAdmin):
    list_display = ("name", "state",)

admin.site.register(Ahli, AhliAdmin)