from django.http import JsonResponse
from .models import Bus
from django.utils.dateparse import parse_datetime
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from .models import Bus, Rating, Booking, Payment, Passenger
from django.db.models import Prefetch


def bus_list_api(request):
    if "payment_success" in request.session:
        del request.session["payment_success"]
        
    source_id = request.GET.get("from")
    destination_id = request.GET.get("to")
    journey_date = request.GET.get("journey_date")

    now = timezone.localtime()
    print(f"Current time: {now}")

    # Filter buses based on starting time and arrival time
    buses = Bus.objects.filter(starting_time__gte=now)
    
    #For type filter 
    filter_on_bus_type = Bus.objects.filter(bus_type='Ac')
    
    for i in filter_on_bus_type :
        print(i.bus_name,'<>',i.starting_time)

    if source_id:
        buses = buses.filter(source_id=source_id)
        print(f"Filtering by source: {source_id}") 
    if destination_id:
        buses = buses.filter(destination_id=destination_id)
        print(f"Filtering by destination: {destination_id}")
    if journey_date:
        journey_datetime = timezone.datetime.strptime(journey_date, "%Y-%m-%d").date()
        buses = buses.filter(starting_time__date=journey_datetime)
        print(f"Filtering by journey date: {journey_date}")

    print(f"Number of buses found: {buses.count()}")

    if buses.count() == 0:
        return JsonResponse({"message": "No buses found"}, status=404)

    buses_data = [
        {
            "bus_id": str(bus.bus_id),
            "bus_name": bus.bus_name,
            "source": bus.source.place_name,
            "destination": bus.destination.place_name,
            "bus_type": bus.bus_type,
            "fare": bus.fare,
            "starting_time": bus.starting_time.strftime("%Y-%m-%d %H:%M:%S"),
            "arrival_time": bus.arrival_time.strftime("%Y-%m-%d %H:%M:%S"),
            "seats": bus.seats,
            "is_available": bus.is_available,
            "bus_operator": bus.bus_Operator.operator_name,
            "bus_operator_contact": bus.bus_Operator.operator_contact,
            "cancel_policy": bus.cancel_policy,
        }
        for bus in buses
    ]
    return JsonResponse(buses_data, safe=False)


def bus_detail(request, bus_id):
    bus = get_object_or_404(Bus, pk=bus_id)
    average_rating = Rating.objects.filter(bus=bus).aggregate(Avg("rating_value"))[
        "rating_value__avg"
    ]
    average_rating = round(average_rating, 1) if average_rating else "No ratings yet"
    return render(
        request, "bus_detail.html", {"bus": bus, "average_rating": average_rating}
    )


def book_bus(request, bus_id):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("login")
        
        bus = get_object_or_404(Bus, pk=bus_id)
        seats = int(request.POST.get("seats", 1))
        total_fare = bus.fare * seats

        # Store booking details in session
        temp_booking = {
            "bus_id": str(bus_id),
            "seats": seats,
            "total_fare": total_fare,
            "passengers": []
        }

        # Collect passenger details from the form
        for i in range(1, seats + 1):
            passenger = {
                "name": request.POST.get(f"passenger_name_{i}"),
                "age": request.POST.get(f"passenger_age_{i}"),
                "gender": request.POST.get(f"passenger_gender_{i}"),
            }
            temp_booking["passengers"].append(passenger)

        # Save the booking and passenger details to the session
        request.session["temp_booking"] = temp_booking

        # Redirect to the payment page
        return redirect("payment_page")

    return redirect("bus_detail", bus_id=bus_id)


def show_my_ticket(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    
    ratings_prefetch = Prefetch('rating_set', queryset=Rating.objects.select_related('bus'))

    bookings = Booking.objects.select_related(
        "bus", "bus__source", "bus__destination", "bus__bus_Operator"
    ).prefetch_related(ratings_prefetch).filter(user_id=user_id)
    bookings_array = []
    for booking in bookings:
        if 'rating_set' in booking._prefetched_objects_cache:
            ratings = booking._prefetched_objects_cache['rating_set']
            for rating in ratings:
                booking.rating = rating.rating_value
                booking.review = rating.review
        bookings_array.append(booking)

        now = timezone.now()
        rating_choices = Rating.RATING_CHOICES
    return render(
        request,
        "show_my_ticket.html",
        {"bookings": bookings_array, "now": now, "rating_choices": rating_choices, },
    )


def cancel_booking(request, booking_id):
    if request.method == "POST":
        booking = get_object_or_404(
            Booking, pk=booking_id, user=request.session.get("user_id")
        )
        booking.delete()
        messages.success(request, "Booking cancelled successfully.")
        return redirect("show_my_ticket")


def payment_page(request):
    booking_details = request.session.get("temp_booking")
    if not booking_details:
        return redirect("home")
    return render(request, "payment_page.html", booking_details)


def process_payment(request):
    if request.method == "POST":
        booking_details = request.session.pop("temp_booking", None)
        if not booking_details:
            return redirect("home")

        bus = Bus.objects.get(bus_id=booking_details["bus_id"])

        # Create the booking
        booking = Booking.objects.create(
            bus_id=booking_details["bus_id"],
            seats=booking_details["seats"],
            user_id=request.session.get("user_id"),
            booking_date=timezone.now().date(),
            starting_time=bus.starting_time,
            arrival_time=bus.arrival_time,
        )

        # Add passengers to the booking
        for passenger_info in booking_details["passengers"]:
            Passenger.objects.create(
                booking=booking,
                name=passenger_info["name"],
                age=passenger_info["age"],
                gender=passenger_info["gender"],
            )

        # Process the payment
        Payment.objects.create(
            booking=booking,
            payment_date=timezone.now().date(),
            amount=request.POST["amount"],
            payment_method=request.POST["payment_method"],
            payment_status="Completed",  # This should be updated based on actual payment gateway response
        )

        # Set a session variable for the popup
        request.session["payment_success"] = True
        return redirect("home")
    
    return redirect("payment_page")


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

def add_rating(request, booking_id):
    if request.method == "POST":
        print('booking_id', booking_id)
        booking = get_object_or_404(Booking, pk=booking_id, user=request.session.get("user_id"))
        rating_value = request.POST.get("rating_value")
        review = request.POST.get("review")
        

        existing_rating = Rating.objects.filter(booking=booking).first()

        if existing_rating:
            existing_rating.rating_value = rating_value
            existing_rating.review = review
            existing_rating.save()
        else:
            # Create a new rating
            Rating.objects.create(
                bus=booking.bus,
                user=booking.user,
                booking=booking,
                rating_value=rating_value,
                review=review,
            )

        messages.success(request, "Thank you for your feedback!")
        return redirect("show_my_ticket")
