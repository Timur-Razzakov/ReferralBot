from django.contrib import admin
from .models import User, Referral, PaymentRequest


# Регистрируем модели нашего приложения в Django админке


@admin.register(Referral)
class SubcategoryAdmin(admin.ModelAdmin):
    # list_display = ['id', 'subcategory_category', 'name', 'created_at']
    # list_display_links = ['id', 'name']
    # search_fields = ['id', 'subcategory_category', 'name']
    list_display = ['id', 'user', 'referral']
    list_display_links = ['id']
    search_fields = ['id']


@admin.register(User)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'referrer_id', 'referrer_id', 'user_id', 'number_payments', 'registered_at', 'is_registered', 'is_active']
    list_display_links = ['id', 'user_name']
    search_fields = ['id', 'user_name', 'registered_at']
    # readonly_fields = ['user_id', 'user_name', 'user_password', 'is_registered']


@admin.register(PaymentRequest)
class PaymentRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'status']
    list_display_links = ['id', 'user_id']
    search_fields = ['id', 'user_id']
