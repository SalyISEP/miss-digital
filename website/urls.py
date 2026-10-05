from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("tech/", views.tech, name="tech"),
    path("com/", views.com, name="com"),
    path("print/", views.print_services, name="print"),
    path("media/", views.media, name="media"),
    path("academy/", views.academy, name="academy"),
    path("equip/", views.equip, name="equip"),

    path("portfolio/", views.portfolio, name="portfolio"),
    path("fondatrice/", views.founder, name="founder"),
    path("contact/", views.contact, name="contact"),
    path("reserver/", views.reservation, name="reserver"),
]