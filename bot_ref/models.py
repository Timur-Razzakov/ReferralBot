from asgiref.sync import sync_to_async
from django.db import models
from django.db.models.signals import post_save
from smart_selects.db_fields import ChainedForeignKey


# Создаем модели нашего приложения
class User(models.Model):
    # Telegram user id
    user_id = models.IntegerField(verbose_name='ID пользователя', unique=True, null=True)
    user_name = models.CharField(verbose_name='Имя пользователя', max_length=255)
    binance_id = models.CharField(verbose_name='Pay id (binance)', max_length=15, unique=True)
    phone_number = models.CharField(verbose_name='Номер телефона',
                                    max_length=11, unique=True, null=False, blank=False)
    invite_link = models.URLField(null=True, blank=True, unique=True)
    user_password = models.CharField(verbose_name='Пароль', max_length=255)
    is_active = models.BooleanField(verbose_name='Отправил деньги', default=False)
    is_registered = models.BooleanField(verbose_name='Зарегистрирован', default=False)
    registered_at = models.DateTimeField(verbose_name='Время регистрации', auto_now_add=True)
    number_payments = models.PositiveIntegerField(verbose_name='Количество выплат', default=0)
    referrer_id = models.IntegerField(verbose_name='Кто пригласил', default=0)

    def __str__(self):
        # return str(self.user_id)
        return f'{self.user_id}: {self.user_name}'

    class Meta:
        verbose_name = 'Телеграмм Пользователь'
        verbose_name_plural = 'Телеграмм Пользователи'
        db_table = 'telegram_users'
        ordering = ['-registered_at']


class Referral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    referral = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral')

    def __str__(self):
        return str(self.user)

    class Meta:
        unique_together = ['user', 'referral']
