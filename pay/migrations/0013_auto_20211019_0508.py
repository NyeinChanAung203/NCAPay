# Generated by Django 3.2.8 on 2021-10-19 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0012_auto_20211016_0750'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-created']},
        ),
        migrations.AlterField(
            model_name='notification',
            name='noti_type',
            field=models.CharField(choices=[('Unread', 'Unread'), ('Read', 'Read')], default='Unread', max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='transfer_type',
            field=models.CharField(choices=[('Expense', 'Expense'), ('Income', 'Income')], max_length=8, null=True),
        ),
    ]