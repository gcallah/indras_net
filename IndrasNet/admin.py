from django.contrib import admin

# Register your models here.
from .models import AdminEmail, Site, Model, ModelType, ModelParam

admin.site.register(AdminEmail)
admin.site.register(Site)
admin.site.register(Model)
admin.site.register(ModelType)
admin.site.register(ModelParam)
