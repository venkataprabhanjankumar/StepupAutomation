# Generated by Django 3.2.8 on 2021-11-15 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stepautomationapp', '0013_documents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='description',
            field=models.CharField(max_length=225),
        ),
    ]