# Generated by Django 3.2.6 on 2022-05-05 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isay', '0003_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='static/img/teaMember.png', upload_to='profile_images'),
        ),
    ]
