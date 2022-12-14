# Generated by Django 3.2.6 on 2022-12-15 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skills', models.CharField(blank=True, max_length=100)),
                ('bio', models.CharField(blank=True, max_length=400)),
                ('profile_pic', django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format='JPEG', keep_meta=True, quality=100, scale=0.5, size=[500, 500], upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
