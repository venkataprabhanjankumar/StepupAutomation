# Generated by Django 3.2.8 on 2021-11-26 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stepautomationapp', '0016_customers'),
    ]

    operations = [
        migrations.AddField(
            model_name='customers',
            name='customer_added_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
