from django.contrib import admin
from .models import (
    CustomUser,
    Place,
    BusOperator,
    Bus,
    Rating,
    Banner,
    Booking,
    Payment,
)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "dob", "age", "phone")
    search_fields = ("email", "name")


class PlaceAdmin(admin.ModelAdmin):
    list_display = ("place_name",)
    search_fields = ("place_name",)


class BusOperatorAdmin(admin.ModelAdmin):
    list_display = ("operator_name", "operator_contact")
    search_fields = ("operator_name",)


class BusAdmin(admin.ModelAdmin):
    list_display = (
        "bus_name",
        "source",
        "destination",
        "bus_type",
        "fare",
        "starting_time",
        "arrival_time",
        "seats",
        "is_available",
        "bus_Operator",
    )
    list_filter = ("bus_type", "is_available", "source", "destination")
    search_fields = ("bus_name", "bus_Operator__operator_name")


class RatingAdmin(admin.ModelAdmin):
    list_display = ("rating_value", "bus", "user", "review")
    list_filter = ("rating_value",)
    search_fields = ("bus__bus_name", "user__email", "review")


class BannerAdmin(admin.ModelAdmin):
    list_display = ("banner_title",)
    search_fields = ("banner_title",)


class BookingAdmin(admin.ModelAdmin):
    list_display = ("booking_id", "bus", "booking_date", "seats", "user")
    list_filter = ("booking_date",)
    search_fields = ("bus__bus_name", "user__email")


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payment_id",
        "booking",
        "payment_date",
        "amount",
        "payment_method",
        "payment_status",
    )
    list_filter = ("payment_date", "payment_status")
    search_fields = ("payment_method",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(BusOperator, BusOperatorAdmin)
admin.site.register(Bus, BusAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Payment, PaymentAdmin)
