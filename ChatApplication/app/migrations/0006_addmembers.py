# Generated by Django 2.2.13 on 2021-07-21 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_group_groupmessages'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.CharField(max_length=100)),
                ('group_id', models.CharField(max_length=100)),
            ],
        ),
    ]