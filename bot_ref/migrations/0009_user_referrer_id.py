# Generated by Django 4.2.6 on 2023-11-02 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_ref', '0008_alter_user_number_payments'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='referrer_id',
            field=models.IntegerField(default=0, verbose_name='Кто пригласил'),
        ),
    ]
