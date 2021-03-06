# Generated by Django 3.0.8 on 2020-08-01 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('SAVINGS', 'Savings'), ('CHECKING', 'Checking')], max_length=100)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CustomerProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('WITHDRAWAL', 'Withdrawal'), ('DEPOSIT', 'Deposit')], max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.CustomerAccount')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CustomerProfile')),
            ],
        ),
    ]
