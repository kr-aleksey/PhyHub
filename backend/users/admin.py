from rest_framework.authtoken.admin import TokenAdmin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User

# TokenAdmin.raw_id_fields = ['user']

admin.site.register(User, BaseUserAdmin)
