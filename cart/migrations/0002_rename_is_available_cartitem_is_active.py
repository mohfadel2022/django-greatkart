# Generated by Django 4.2.5 on 2023-10-03 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='is_available',
            new_name='is_active',
        ),
    ]