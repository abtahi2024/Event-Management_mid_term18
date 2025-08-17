from django.contrib import admin
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.
@admin.register(CustomUser)

class CustomUserAdmin(UserAdmin):
    model=CustomUser

    fieldsets = (
        (None, {"fields": ('username','password'),}),
        ('personal info',{'fields':('first_name', 'last_name', 'email','profile_image','phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None,{
            'classes': ('wide',),
            'fields':('username','password', 'password2', 'first_name', 'last_name', 'email', 'profile_image', 'phone', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')})
            )
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined')
    search_fields =('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)