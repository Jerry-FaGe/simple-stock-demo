# Generated by Django 5.2.1 on 2025-05-13 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='good',
            options={'ordering': ['-created_at'], 'verbose_name': 'good'},
        ),
        migrations.AlterField(
            model_name='good',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddConstraint(
            model_name='good',
            constraint=models.CheckConstraint(condition=models.Q(('reserved__lte', models.F('stock'))), name='reserved_le_stock'),
        ),
    ]
