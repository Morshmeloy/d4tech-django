"""Views for the core application."""
import logging

from django.db import connection
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .forms import ContactForm
from .models import ContactInfo, ContactMessage, EmergencySupport, RegularSupport, SiteContent

logger = logging.getLogger(__name__)


def _get_context() -> dict:
    """Базовый контекст с контактами для всех страниц."""
    return {"contacts": ContactInfo.get()}


def home(request: HttpRequest) -> HttpResponse:
    """Render the home page."""
    context = _get_context()
    context["hero_title"] = SiteContent.get_text("hero_title", "Комплексная автоматизация и цифровизация объектов электроэнергетики")
    context["info_quote"] = SiteContent.get_text("info_quote", "«Д4 технологии» — это синоним надежности, инноваций и глубокой экспертизы в создании цифрового будущего энергетики России.")
    return render(request, "pages/home.html", context)


def contacts(request: HttpRequest) -> HttpResponse:
    """Render the contacts page with form handling."""
    context = _get_context()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(**form.cleaned_data)
            logger.info("Contact form submitted by %s", form.cleaned_data["email"])
            context.update({"form": ContactForm(), "success": True})
            return render(request, "pages/contacts.html", context)
    else:
        form = ContactForm()
    context["form"] = form
    return render(request, "pages/contacts.html", context)


def support(request: HttpRequest) -> HttpResponse:
    """Render the support page."""
    context = _get_context()
    context["emergency"] = EmergencySupport.get()
    context["regular"] = RegularSupport.get()
    return render(request, "pages/support.html", context)


def information(request: HttpRequest) -> HttpResponse:
    """Render the information page."""
    return render(request, "pages/information.html", _get_context())


def compliance(request: HttpRequest) -> HttpResponse:
    """
    Страница с правовой информацией и реквизитами (для соответствия Приказу Минцифры №511).
    Отображает полное наименование, ИНН, ОГРН, ОКВЭД, коды видов деятельности,
    информацию о стоимости, правах на ПО, технологиях и реестре.
    """
    context = _get_context()
    return render(request, "pages/compliance.html", context)

def solutions(request: HttpRequest) -> HttpResponse:
    """Страница с решениями и услугами (соответствует структуре сайта)."""
    context = _get_context()
    return render(request, "pages/solutions.html", context)


def software(request: HttpRequest) -> HttpResponse:
    """Страница с программным обеспечением (D4NMS, лицензии, права)."""
    context = _get_context()
    return render(request, "pages/software.html", context)

@require_GET
def health(request: HttpRequest) -> JsonResponse:
    """Health check endpoint для мониторинга и Docker healthcheck."""
    try:
        connection.ensure_connection()
        return JsonResponse({"status": "ok"})
    except Exception:
        logger.exception("Health check failed: database unavailable")
        return JsonResponse({"status": "error"}, status=503)


@require_GET
def robots_txt(request: HttpRequest) -> HttpResponse:
    """Serve robots.txt для поисковых роботов."""
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /health/",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


@require_GET
def sitemap_xml(request: HttpRequest) -> HttpResponse:
    """Serve sitemap.xml для SEO."""
    base = f"{request.scheme}://{request.get_host()}"
    urls = [
        ("", "1.0", "monthly"),
        ("/contacts/", "0.8", "monthly"),
        ("/support/", "0.7", "monthly"),
        ("/information/", "0.5", "yearly"),
        ("/compliance/", "0.5", "yearly"),  # добавили страницу правовой информации
    ]
    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, priority, freq in urls:
        xml_parts.append(
            f"  <url><loc>{base}{path}</loc>"
            f"<priority>{priority}</priority>"
            f"<changefreq>{freq}</changefreq></url>"
        )
    xml_parts.append("</urlset>")
    return HttpResponse("\n".join(xml_parts), content_type="application/xml; charset=utf-8")