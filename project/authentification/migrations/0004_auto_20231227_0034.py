# Generated by Django 2.2.28 on 2023-12-26 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0003_remove_client_name_client_client_fname_client_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Client',
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
        migrations.DeleteModel(
            name='Creneau',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.DeleteModel(
            name='Events',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]
