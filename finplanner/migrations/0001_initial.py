# Generated by Django 2.1.2 on 2018-11-05 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
                ('budget', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finplanner.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='finplanner.Account')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finplanner.Category')),
            ],
            options={
                'ordering': ('-amount',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('contact', models.CharField(blank=True, max_length=60)),
                ('timestamp', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='bank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='finplanner.Bank'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
