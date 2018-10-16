"""
This is where we register models so that they are available
for data entry in Django's admin interface.
"""

from django.contrib import admin

# Register your models here.
from .models import AdminEmail, Site, ABMModel, ModelType, ModelParam

admin.site.register(AdminEmail)
admin.site.register(Site)
admin.site.register(ABMModel)
admin.site.register(ModelType)
admin.site.register(ModelParam)
