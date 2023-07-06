# Generated by Django 4.2.3 on 2023-07-05 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_usercreation_approved_usercreation_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('timeline', models.DateTimeField()),
                ('winners', models.CharField(max_length=100)),
                ('photos', models.ImageField(upload_to='event_photos')),
            ],
        ),
    ]