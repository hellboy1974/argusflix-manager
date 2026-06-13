from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_favorite_watchhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pin',
            field=models.CharField(blank=True, db_index=True, max_length=4, null=True),
        ),
    ]
