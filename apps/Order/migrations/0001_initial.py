# Generated by Django 2.0.1 on 2018-02-22 16:10

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
        ('Address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('products', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('status', models.CharField(default='Order Received', max_length=50)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Address.Address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.User')),
            ],
        ),
    ]
