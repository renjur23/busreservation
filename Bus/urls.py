from django.urls import path

from .banner import banner_carousel_api
from .place import place_list_api
from .bus import (
    bus_list_api,
    bus_detail,
    book_bus,
    show_my_ticket,
    cancel_booking,
    payment_page,
    process_payment,
    add_rating,
)
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout, name="logout"),
    path("about_us/", about_us, name="about_us"),
    path("contact_us/", contact_us, name="contact_us"),
    path("banners/", banner_carousel_api, name="banner_carousel_api"),
    path("places/", place_list_api, name="place_list_api"),
    path("buses/", bus_list_api, name="bus_list_api"),
    path("buses/<uuid:bus_id>/", bus_detail, name="bus_detail"),
    path("book-bus/<uuid:bus_id>/", book_bus, name="book_bus"),
    path("show-my-ticket/", show_my_ticket, name="show_my_ticket"),
    path("cancel-booking/<uuid:booking_id>/", cancel_booking, name="cancel_booking"),
    path("payment/", payment_page, name="payment_page"),
    path("process-payment/", process_payment, name="process_payment"),
    path("add_rating/<uuid:booking_id>/", add_rating, name="add_rating"),
]
