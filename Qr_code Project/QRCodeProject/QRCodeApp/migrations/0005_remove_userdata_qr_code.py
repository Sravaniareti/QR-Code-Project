# Generated by Django 4.2.7 on 2024-01-21 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QRCodeApp', '0004_userdata_qr_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='qr_code',
        ),
    ]
