# Generated by Django 4.2.16 on 2024-10-24 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_empleado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
