"""URL patterns for the core application."""
from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
    path("support/", views.support, name="support"),
    path("information/", views.information, name="information"),
    path("compliance/", views.compliance, name="compliance"),
    path("solutions/", views.solutions, name="solutions"),
    path("software/", views.software, name="software"),
    path("health/", views.health, name="health"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap_xml"),
]