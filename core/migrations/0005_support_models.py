"""Migration to add EmergencySupport and RegularSupport models."""
from django.db import migrations, models


class Migration(migrations.Migration):
    """Replace SiteContent support entries with dedicated support models."""

    dependencies = [
        ("core", "0004_sitecontent_support"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmergencySupport",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("phone", models.CharField(default="+7 (XXX) XXX-XX-XX", max_length=50, verbose_name="Телефон")),
                ("email", models.EmailField(default="emergency@company.com", verbose_name="Email")),
                ("hours", models.CharField(default="24/7", max_length=100, verbose_name="Время работы")),
            ],
            options={
                "verbose_name": "Экстренная поддержка",
                "verbose_name_plural": "Экстренная поддержка",
            },
        ),
        migrations.CreateModel(
            name="RegularSupport",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("phone", models.CharField(default="+7 (XXX) XXX-XX-XX", max_length=50, verbose_name="Телефон")),
                ("email", models.EmailField(default="support@company.com", verbose_name="Email")),
                ("hours", models.CharField(default="Пн-Пт 9:00-18:00", max_length=100, verbose_name="Время работы")),
            ],
            options={
                "verbose_name": "Обычная поддержка",
                "verbose_name_plural": "Обычная поддержка",
            },
        ),
        # Удаляем записи поддержки из SiteContent — они теперь в отдельных моделях
        migrations.RunSQL(
            sql="DELETE FROM core_sitecontent WHERE key LIKE 'support_%';",
            reverse_sql="",
        ),
    ]
