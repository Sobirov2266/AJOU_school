from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_teacherprofile_photo"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="profile_photo",
            field=models.ImageField(blank=True, null=True, upload_to="users/profile_photos/"),
        ),
    ]
