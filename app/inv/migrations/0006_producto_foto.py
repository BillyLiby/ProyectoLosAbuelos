# Generated by Django 5.1.6 on 2025-06-24 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0005_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
