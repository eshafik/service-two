# Generated by Django 4.1.4 on 2024-03-02 08:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('twitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPostServingHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_seen', to='twitter.feedpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_seen', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
