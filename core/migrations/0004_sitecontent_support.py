"""Migration to add support page content blocks."""
from django.db import migrations


class Migration(migrations.Migration):
    """Add editable content blocks for the support page contact cards."""

    dependencies = [
        ("core", "0003_sitecontent"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                INSERT INTO core_sitecontent (key, label, text) VALUES
                ('support_emergency_phone',   'Поддержка — Экстренный телефон',          '+7 (XXX) XXX-XX-XX'),
                ('support_emergency_email',   'Поддержка — Экстренный Email',             'emergency@company.com'),
                ('support_emergency_hours',   'Поддержка — Время работы (экстренная)',    '24/7'),
                ('support_regular_phone',     'Поддержка — Обычный телефон',              '+7 (XXX) XXX-XX-XX'),
                ('support_regular_email',     'Поддержка — Обычный Email',                'support@company.com'),
                ('support_regular_hours',     'Поддержка — Время работы (обычная)',       'Пн-Пт 9:00-18:00');
            """,
            reverse_sql="DELETE FROM core_sitecontent WHERE key LIKE 'support_%';",
        ),
    ]
