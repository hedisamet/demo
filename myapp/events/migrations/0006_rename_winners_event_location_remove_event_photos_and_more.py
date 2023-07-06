# Generated by Django 4.2.3 on 2023-07-05 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_event'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='winners',
            new_name='location',
        ),
        migrations.RemoveField(
            model_name='event',
            name='photos',
        ),
        migrations.AlterField(
            model_name='event',
            name='timeline',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='EventPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='event_photos')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_photos', to='events.event')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='photos',
            field=models.ManyToManyField(related_name='events', to='events.eventphoto'),
        ),
    ]