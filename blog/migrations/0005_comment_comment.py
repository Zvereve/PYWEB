# Generated by Django 4.0.4 on 2022-05-28 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_note_options_note_author_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.TextField(default='', verbose_name='Комментарий'),
        ),
    ]