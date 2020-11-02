# Generated by Django 3.0.4 on 2020-05-23 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, default='+7**********', max_length=100)),
                ('telegram', models.CharField(blank=True, default='-', max_length=100)),
                ('id_for_bot', models.IntegerField(blank=True, null=True)),
                ('id_for_matrix', models.CharField(blank=True, default='-', max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('slow_mode_delivery_rule', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FilterModeDeliveryRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule', models.TextField()),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipient.Recipient')),
            ],
        ),
        migrations.CreateModel(
            name='ExceptModeDeliveryRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule', models.TextField()),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipient.Recipient')),
            ],
        ),
    ]
