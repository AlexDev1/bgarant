# Generated by Django 2.2.2 on 2019-06-17 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20190613_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='youtube',
            field=models.URLField(default='', verbose_name='Ссылка на Youtube-video'),
            preserve_default=False,
        ),
    ]
