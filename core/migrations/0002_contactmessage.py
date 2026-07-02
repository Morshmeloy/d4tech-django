"""Migration for ContactMessage model."""
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    """Add ContactMessage model for storing contact form submissions."""

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="Имя")),
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                ("subject", models.CharField(max_length=200, verbose_name="Тема")),
                ("message", models.TextField(verbose_name="Сообщение")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, verbose_name="Дата отправки")),
                ("is_read", models.BooleanField(default=False, verbose_name="Прочитано")),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
                "ordering": ["-created_at"],
            },
        ),
    ]
