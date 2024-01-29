from django.contrib import admin
from .models import ModelCard, ModelPermission, ModelList

admin.site.register(ModelPermission)
admin.site.register(ModelCard)
admin.site.register(ModelList)

