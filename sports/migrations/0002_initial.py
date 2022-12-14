# Generated by Django 4.1 on 2022-09-03 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbooking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='slot',
            name='court',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports.court'),
        ),
        migrations.AddField(
            model_name='item',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports.sport'),
        ),
        migrations.AddField(
            model_name='court',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports.sport'),
        ),
    ]
