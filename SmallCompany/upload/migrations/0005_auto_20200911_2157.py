# Generated by Django 3.0.8 on 2020-09-11 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0004_auto_20200911_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaserecord',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
