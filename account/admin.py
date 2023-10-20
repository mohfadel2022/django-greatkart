from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import Account, UserProfile

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username','last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly = ('last_login', 'date_joined')
    ordering = ('date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.profile_picture:
            return format_html('<img src="{}" width="30" style="border-radius:50%">'.format(object.profile_picture.url))
        else:
            return format_html('<img src="{picture}" width="30" style="border-radius:50%">', picture = settings.STATIC_ROOT /'images/no_image.jpg')
        
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)