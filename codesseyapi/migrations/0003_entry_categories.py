# Generated by Django 4.2.5 on 2023-09-11 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codesseyapi', '0002_category_entry_entrycategory_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='categories',
            field=models.ManyToManyField(related_name='entries', through='codesseyapi.EntryCategory', to='codesseyapi.category'),
        ),
    ]
