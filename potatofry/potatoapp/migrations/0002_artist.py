# Generated by Django 4.2.4 on 2023-09-17 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('potatoapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
    ]
