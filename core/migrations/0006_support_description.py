"""Migration to add description field to support models."""
from django.db import migrations, models


class Migration(migrations.Migration):
    """Add description field to EmergencySupport and RegularSupport."""

    dependencies = [
        ("core", "0005_support_models"),
    ]

    operations = [
        migrations.AddField(
            model_name="emergencysupport",
            name="description",
            field=models.CharField(default="Для критических проблем, требующих немедленного решения", max_length=200, verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="regularsupport",
            name="description",
            field=models.CharField(default="Для общих вопросов и консультаций", max_length=200, verbose_name="Описание"),
        ),
    ]
