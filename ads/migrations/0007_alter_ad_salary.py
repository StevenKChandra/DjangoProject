# Generated by Django 4.2.6 on 2023-10-27 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0006_rename_text_ad_description_rename_price_ad_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='salary',
            field=models.PositiveIntegerField(null=True),
        ),
    ]