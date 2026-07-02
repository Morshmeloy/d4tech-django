"""Admin configuration for the core application."""
from django.contrib import admin
from django.http import HttpRequest

from .models import ContactInfo, ContactMessage, EmergencySupport, RegularSupport, SiteContent


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """Админ-панель для контактной информации и реквизитов (в т.ч. для Приказа №511)."""

    list_display = ("phone", "email", "full_name", "inn", "ogrn", "okved")
    search_fields = ("phone", "email", "full_name", "inn", "ogrn")

    fieldsets = (
        ("Основные контакты", {
            "fields": ("phone", "email", "address", "website")
        }),
        ("Реквизиты для Минцифры (Приказ №511)", {
            "fields": ("full_name", "inn", "ogrn", "okved", "it_activity_codes"),
            "description": "Информация, обязательная для размещения на сайте согласно Приказу №511"
        }),
        ("Информация о деятельности и стоимости", {
            "fields": ("pricing_info", "activity_description"),
        }),
        ("Интеллектуальная собственность и технологии", {
            "fields": ("rights_info", "tech_stack", "registry_info"),
        }),
    )

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        extra_context["show_save_and_continue"] = False
        return super().changeform_view(request, object_id, form_url, extra_context)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Разрешаем добавление только если записей нет."""
        return not ContactInfo.objects.exists()

    def has_delete_permission(
        self, request: HttpRequest, obj: ContactInfo | None = None
    ) -> bool:
        """Запрещаем удаление — запись должна быть всегда одна."""
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Админ-панель для сообщений из контактной формы.

    Сообщения создаются только через форму на сайте.
    Доступно только чтение и отметка «Прочитано».
    """

    list_display = ("subject", "email", "name", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")
    list_per_page = 25

    # Оставляем только кнопку "Сохранить" (убираем "добавить другой" и "продолжить")
    def response_change(self, request: HttpRequest, obj: ContactMessage):
        """После сохранения возвращаемся к списку сообщений."""
        obj.save()
        return super().response_change(request, obj)

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        extra_context["show_save_and_continue"] = False
        return super().changeform_view(request, object_id, form_url, extra_context)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Сообщения создаются только через форму на сайте."""
        return False


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    """Админ-панель для текстовых блоков сайта."""

    list_display = ("label", "key")
    readonly_fields = ("key",)

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        extra_context["show_save_and_continue"] = False
        return super().changeform_view(request, object_id, form_url, extra_context)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Блоки создаются только через миграции."""
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: SiteContent | None = None
    ) -> bool:
        return False


@admin.register(EmergencySupport)
class EmergencySupportAdmin(admin.ModelAdmin):
    """Админ-панель для экстренной поддержки."""

    list_display = ("description", "phone", "email", "hours")

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        extra_context["show_save_and_continue"] = False
        return super().changeform_view(request, object_id, form_url, extra_context)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return not EmergencySupport.objects.exists()

    def has_delete_permission(
        self, request: HttpRequest, obj: EmergencySupport | None = None
    ) -> bool:
        return False


@admin.register(RegularSupport)
class RegularSupportAdmin(admin.ModelAdmin):
    """Админ-панель для обычной поддержки."""

    list_display = ("description", "phone", "email", "hours")

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        extra_context["show_save_and_continue"] = False
        return super().changeform_view(request, object_id, form_url, extra_context)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return not RegularSupport.objects.exists()

    def has_delete_permission(
        self, request: HttpRequest, obj: RegularSupport | None = None
    ) -> bool:
        return False