# Generated by Django 4.1 on 2022-08-27 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0005_slot_userbooking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(default='item.jpg', upload_to='item_pics')),
                ('number', models.PositiveIntegerField()),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports.sport')),
            ],
        ),
    ]
