# Generated by Django 4.1.7 on 2023-03-28 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0008_rename_name_user_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='passwored',
            new_name='password',
        ),
    ]