# Generated by Django 4.2.5 on 2023-10-02 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_alter_category_slug'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Product',
            new_name='Store',
        ),
    ]
