# from django.contrib import admin
# from .models import User, Referral
#
#
# # Регистрируем модели нашего приложения в Django админке


# @admin.register(Referral)
# class SubcategoryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'subcategory_category', 'name', 'created_at']
#     list_display_links = ['id', 'name']
#     search_fields = ['id', 'subcategory_category', 'name']
#
#
# @admin.register(User)
# class TelegramUserAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user_login', 'registered_at', 'is_registered']
#     list_display_links = ['id', 'user_login']
#     search_fields = ['id', 'user_login', 'registered_at']
#     readonly_fields = ['chat_id', 'user_login', 'user_password', 'is_registered']
