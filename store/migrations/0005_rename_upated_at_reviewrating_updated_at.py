# Generated by Django 4.2.5 on 2023-10-17 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_reviewrating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewrating',
            old_name='upated_at',
            new_name='updated_at',
        ),
    ]
