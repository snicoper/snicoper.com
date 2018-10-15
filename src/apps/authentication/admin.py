from django.contrib import admin

from .forms import RegisterUserForm
from .models import RegisterUser, UserEmailUpdate


@admin.register(RegisterUser)
class RegisterUserAdmin(admin.ModelAdmin):
    """Admin para RegisterUser."""
    form = RegisterUserForm
    list_display = ('email', 'username', 'date_joined')


@admin.register(UserEmailUpdate)
class UserEmailUpdateAdmin(admin.ModelAdmin):
    pass
