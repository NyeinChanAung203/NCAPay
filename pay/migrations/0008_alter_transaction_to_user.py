# Generated by Django 3.2.8 on 2021-10-16 03:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pay', '0007_alter_transaction_to_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='to_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL),
        ),
    ]
