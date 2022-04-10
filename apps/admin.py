from django.contrib import admin
from .models import ApplicationConfig, ApplicationPlatform, ApplicationKind


@admin.register(ApplicationConfig)
class ApplicationConfigAdmin(admin.ModelAdmin):
    pass

@admin.register(ApplicationPlatform)
class ApplicationPlatformAdmin(admin.ModelAdmin):
    pass

@admin.register(ApplicationKind)
class ApplicationKindAdmin(admin.ModelAdmin):
    pass