from django.contrib import admin
from . import models

admin.site.register(models.ClubInfo)
admin.site.register(models.ClubConfig)
admin.site.register(models.Transaction)