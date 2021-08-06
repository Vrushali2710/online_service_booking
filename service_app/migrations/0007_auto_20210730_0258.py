# Generated by Django 3.0.4 on 2021-07-29 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0006_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipping_address',
        ),
        migrations.AddField(
            model_name='order',
            name='Time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='type',
            field=models.CharField(choices=[('Self Pick up and Drop', 'Self Pick up and Drop'), (' Pick up and Drop by Mechanic', 'Pick up and Drop by Mechanic')], default='', max_length=50),
        ),
    ]
