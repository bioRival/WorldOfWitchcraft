# Generated by Django 4.2.4 on 2023-08-25 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_postreply_post_alter_postreply_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postreply',
            name='publication_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
