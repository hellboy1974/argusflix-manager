# Generated manually
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_default', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='AppPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_type', models.CharField(choices=[('home', 'Home Screen'), ('movies', 'Movies'), ('series', 'Series'), ('live_tv', 'Live TV')], max_length=20)),
                ('title', models.CharField(max_length=100)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='appbuilder.appprofile')),
            ],
            options={
                'unique_together': {('profile', 'page_type')},
            },
        ),
        migrations.CreateModel(
            name='AppWidget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('widget_type', models.CharField(choices=[('hero', 'Hero Banner'), ('continue_watching', 'Continue Watching'), ('category_row', 'Category Row'), ('trending', 'Trending / Popular'), ('recent_live_tv', 'Recent Live TV'), ('recently_added', 'Recently Added (Per Server)'), ('now_playing', 'Now Playing / EPG Live'), ('favorites', 'Favorites'), ('custom_banner', 'Custom Banner / Announcement')], max_length=30)),
                ('order', models.PositiveIntegerField(default=0)),
                ('settings', models.JSONField(blank=True, default=dict, help_text='Specific settings for this widget, e.g., category ID, server ID, or banner text.')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='widgets', to='appbuilder.apppage')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
