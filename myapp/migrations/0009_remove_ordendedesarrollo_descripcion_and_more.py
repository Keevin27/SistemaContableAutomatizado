# Generated by Django 4.2.16 on 2024-11-04 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_empleado_costo_mensual'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordendedesarrollo',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='ordendedesarrollo',
            name='nombre',
        ),
        migrations.AddField(
            model_name='ordendedesarrollo',
            name='cif',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='ordendedesarrollo',
            name='costo_por_linea',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='ordendedesarrollo',
            name='costo_producto',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='ordendedesarrollo',
            name='lineas_mes',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='ordendedesarrollo',
            name='mod',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='ordendedesarrollo',
            name='moh',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='ordendedesarrollo',
            name='moi',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='ordendedesarrollo',
            name='precio_venta',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='ordendedesarrollo',
            name='tasa_cif',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='ordendedesarrollo',
            name='tiempo_estimado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='ordendedesarrollo',
            name='total_cif',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='ordendedesarrollo',
            name='total_loc',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_modulo', models.CharField(default='', max_length=100)),
                ('descripcion', models.CharField(default='', max_length=100)),
                ('optimista', models.IntegerField()),
                ('probable', models.IntegerField()),
                ('pesimista', models.IntegerField()),
                ('lineas_esperadas', models.IntegerField()),
                ('costo_modulo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('orden_desarrollo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.ordendedesarrollo')),
            ],
        ),
    ]
