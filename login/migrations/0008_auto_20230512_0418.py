# Generated by Django 3.0.6 on 2023-05-12 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_auto_20230512_0318'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='confirmstring',
            options={'ordering': ['-c_time'], 'verbose_name': 'confirm', 'verbose_name_plural': 'confirm'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-c_time'], 'verbose_name': 'user', 'verbose_name_plural': 'user'},
        ),
        migrations.AddField(
            model_name='user',
            name='realname',
            field=models.CharField(default='NULL', max_length=256),
        ),
        migrations.AddField(
            model_name='user',
            name='user_id_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='user_phone',
            field=models.IntegerField(default=0),
        ),
    ]
