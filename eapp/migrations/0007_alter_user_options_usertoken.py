# Generated by Django 4.1.7 on 2023-03-28 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0006_alter_user_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户信息表', 'verbose_name_plural': '用户信息表'},
        ),
        migrations.CreateModel(
            name='userToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=60)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='eapp.user')),
            ],
            options={
                'verbose_name': '用户token表',
                'verbose_name_plural': '用户token表',
                'db_table': 'user_token',
            },
        ),
    ]