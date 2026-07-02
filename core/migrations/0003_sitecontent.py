"""Migration for SiteContent model."""
from django.db import migrations, models


class Migration(migrations.Migration):
    """Add SiteContent model for managing editable text blocks via admin."""

    dependencies = [
        ("core", "0002_contactmessage"),
    ]

    operations = [
        migrations.CreateModel(
            name="SiteContent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.CharField(max_length=100, unique=True, verbose_name="Ключ")),
                ("label", models.CharField(max_length=200, verbose_name="Название")),
                ("text", models.TextField(verbose_name="Текст")),
            ],
            options={
                "verbose_name": "Текстовый блок",
                "verbose_name_plural": "Текстовые блоки",
                "ordering": ["key"],
            },
        ),
        migrations.RunSQL(
            sql="""
                INSERT INTO core_sitecontent (key, label, text) VALUES
                ('hero_title', 'Главный заголовок (Hero)', 'Комплексная автоматизация и цифровизация объектов электроэнергетики'),
                ('info_quote', 'Цитата на главной странице', '«Д4 технологии» — это синоним надежности, инноваций и глубокой экспертизы в создании цифрового будущего энергетики России.');
            """,
            reverse_sql="DELETE FROM core_sitecontent WHERE key IN ('hero_title', 'info_quote');",
        ),
    ]
