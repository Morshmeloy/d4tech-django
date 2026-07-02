"""Models for the core application."""
from django.db import models
from django.utils import timezone


class ContactInfo(models.Model):
    """Контактная информация и реквизиты компании (в т.ч. для соответствия Приказу Минцифры №511)."""

    # --- Основные контакты ---
    phone = models.CharField("Телефон", max_length=50, default="+7 (495) 123-45-67")
    email = models.EmailField("Email", default="info@d4tech.ru")
    address = models.CharField("Адрес", max_length=200, default="г. Москва, ул. D4, д. 1")
    website = models.CharField("Сайт", max_length=100, default="d4tech.ru")

    # --- Реквизиты для соответствия Приказу Минцифры №511 ---
    full_name = models.CharField(
        "Полное наименование организации",
        max_length=255,
        default="Общество с ограниченной ответственностью «Д4 Технологии»"
    )
    inn = models.CharField("ИНН", max_length=12, default="9723116807")
    ogrn = models.CharField("ОГРН", max_length=13, default="1217700245916")
    okved = models.CharField(
        "Основной код ОКВЭД",
        max_length=10,
        default="62.01",
        help_text="Например, 62.01 — Разработка компьютерного программного обеспечения"
    )
    it_activity_codes = models.TextField(
        "Коды видов деятельности в области ИТ (через запятую)",
        default="1.1, 1.2, 1.3",
        help_text="Коды из приказа Минцифры №449 (например: 1.1, 1.2, 1.3)"
    )

    # --- Дополнительная информация, требуемая приказом ---
    pricing_info = models.TextField(
        "Информация о стоимости товаров/услуг",
        blank=True,
        default="Цены уточняйте по запросу. Стоимость зависит от состава работ и объёма услуг."
    )
    rights_info = models.TextField(
        "Информация о правах на ПО и способах предоставления",
        blank=True,
        default="Компания является правообладателем исключительных прав на разработанное ПО. " \
                "Предоставление прав осуществляется на основании лицензионных договоров."
    )
    tech_stack = models.TextField(
        "Используемые технологии (языки, фреймворки, инструменты)",
        blank=True,
        default="Python, Django, PostgreSQL, Docker, Nginx, Tailwind CSS, JavaScript"
    )
    registry_info = models.TextField(
        "Информация о ПО в реестре российского ПО",
        blank=True,
        default="Сведения о регистрации в реестре российского ПО: запись №XXXX от XX.XX.XXXX (при наличии)."
    )

    # --- Дополнительное описание деятельности (для страницы "О компании") ---
    activity_description = models.TextField(
        "Описание деятельности",
        blank=True,
        default="Комплексная автоматизация и цифровизация объектов электроэнергетики. " \
                "Разработка и внедрение систем телемеханики, SCADA, промышленных сетей связи."
    )

    class Meta:
        verbose_name = "Контактная информация и реквизиты"
        verbose_name_plural = "Контактная информация и реквизиты"

    def __str__(self) -> str:
        return f"Контакты: {self.phone}"

    @classmethod
    def get(cls) -> "ContactInfo":
        """Возвращает единственную запись контактов (или создаёт дефолтную)."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteContent(models.Model):
    """Текстовые блоки сайта, редактируемые через админку."""

    key = models.CharField("Ключ", max_length=100, unique=True)
    label = models.CharField("Название", max_length=200)
    text = models.TextField("Текст")

    class Meta:
        verbose_name = "Текстовый блок"
        verbose_name_plural = "Текстовые блоки"
        ordering = ["key"]

    def __str__(self) -> str:
        return self.label

    @classmethod
    def get_text(cls, key: str, default: str = "") -> str:
        """Возвращает текст блока по ключу или default если не найден."""
        try:
            return cls.objects.get(key=key).text
        except cls.DoesNotExist:
            return default


class EmergencySupport(models.Model):
    """Контакты экстренной поддержки."""

    description = models.CharField("Описание", max_length=200, default="Для критических проблем, требующих немедленного решения")
    phone = models.CharField("Телефон", max_length=50, default="+7 (XXX) XXX-XX-XX")
    email = models.EmailField("Email", default="emergency@company.com")
    hours = models.CharField("Время работы", max_length=100, default="24/7")

    class Meta:
        verbose_name = "Экстренная поддержка"
        verbose_name_plural = "Экстренная поддержка"

    def __str__(self) -> str:
        return "Экстренная поддержка"

    @classmethod
    def get(cls) -> "EmergencySupport":
        """Возвращает единственную запись (или создаёт дефолтную)."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class RegularSupport(models.Model):
    """Контакты обычной поддержки."""

    description = models.CharField("Описание", max_length=200, default="Для общих вопросов и консультаций")
    phone = models.CharField("Телефон", max_length=50, default="+7 (XXX) XXX-XX-XX")
    email = models.EmailField("Email", default="support@company.com")
    hours = models.CharField("Время работы", max_length=100, default="Пн-Пт 9:00-18:00")

    class Meta:
        verbose_name = "Обычная поддержка"
        verbose_name_plural = "Обычная поддержка"

    def __str__(self) -> str:
        return "Обычная поддержка"

    @classmethod
    def get(cls) -> "RegularSupport":
        """Возвращает единственную запись (или создаёт дефолтную)."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ContactMessage(models.Model):
    """Сообщение из контактной формы."""

    name = models.CharField("Имя", max_length=100)
    email = models.EmailField("Email")
    subject = models.CharField("Тема", max_length=200)
    message = models.TextField("Сообщение")
    created_at = models.DateTimeField("Дата отправки", default=timezone.now)
    is_read = models.BooleanField("Прочитано", default=False)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.subject} — {self.email}"