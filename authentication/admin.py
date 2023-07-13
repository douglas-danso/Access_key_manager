from django.contrib import admin
from authentication.models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(CustomUser)
