from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from user import  models

# Register your models here.
# @admin.register(models.user_ktp, models.user_props)
class UserAdmin(BaseUserAdmin):
    """ define user page for admin """
    # model = models.user
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login', ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'is_active', 'is_staff', 'is_superuser')
        }),
    )

# class UserPropsAdmin(models.user_props):
#     """ define user page for admin """
#     model = models.user_props


# class UserKtpAdmin():
#     """ define user ktp page for admin """
#     ordering = ['id']
#     list_display = ['ktp_number', 'user_id']
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('ktp_number',)
#         }),
#     )


admin.site.register(models.user, UserAdmin)
# admin.site.register(models.user_props, UserPropsAdmin)
# admin.site.register(models.user_ktp, UserKtpAdmin)