# Generated by Django 2.1.2 on 2018-11-08 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finplanner', '0004_remove_account_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='payment_mode',
        ),
        migrations.AddField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('Accomodation', 'Accomodation'), ('Food', 'Food'), ('Groceries', 'Groceries'), ('Transportation', 'Transportation'), ('Entertainment', 'Entertainment')], default='', max_length=80),
        ),
    ]
