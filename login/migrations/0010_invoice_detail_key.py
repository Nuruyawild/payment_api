# Generated by Django 3.0.6 on 2023-05-12 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_auto_20230512_0439'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice_detail',
            name='key',
            field=models.CharField(default='', max_length=100),
        ),
    ]
