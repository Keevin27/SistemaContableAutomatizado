# Generated by Django 4.2.16 on 2024-10-24 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_empleado_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]