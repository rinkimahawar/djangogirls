# Generated by Django 4.1.6 on 2023-04-06 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_image_alter_post_thumbimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
