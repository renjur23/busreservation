from django.db import models
import uuid


class CustomUser(models.Model):
    name = models.CharField(max_length=255)
    dob = models.DateField()
    age = models.PositiveIntegerField()
    email = models.EmailField(max_length=255, unique=True)
    phone = models.PositiveIntegerField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email


class Place(models.Model):
    place_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    place_name = models.CharField(max_length=100)

    def __str__(self):
        return self.place_name


class BusOperator(models.Model):
    operator_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operator_name = models.CharField(max_length=100)
    operator_contact = models.PositiveIntegerField()

    def __str__(self):
        return self.operator_name


class Bus(models.Model):
    bus_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bus_name = models.CharField(max_length=100)
    source = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="source")
    destination = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name="destination"
    )
    bus_type = models.CharField(max_length=100)
    fare = models.PositiveIntegerField()
    starting_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    seats = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    bus_Operator = models.ForeignKey(BusOperator, on_delete=models.CASCADE)
    cancel_policy = models.CharField(max_length=100)


class Banner(models.Model):
    banner_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    banner_title = models.CharField(max_length=100)
    banner_image = models.ImageField(upload_to="banner_images/")

    def __str__(self):
        return self.banner_title


class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    booking_date = models.DateField()
    seats = models.PositiveIntegerField()
    starting_time = models.DateTimeField(null=True)
    arrival_time = models.DateTimeField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Booking ID: {self.booking_id}"


class Rating(models.Model):
    RATING_CHOICES = [
        (1, "1 - Very Poor"),
        (2, "2 - Poor"),
        (3, "3 - Average"),
        (4, "4 - Good"),
        (5, "5 - Excellent"),
    ]
    rating_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    rating_value = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)
    review = models.TextField()

    def __str__(self):
        return f"Rating: {self.rating_value} for Bus: {self.bus.bus_name}"


class Payment(models.Model):
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)

    def __str__(self):
        return f"Payment ID: {self.payment_id}"


class Passenger(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Passenger"
        verbose_name_plural = "Passengers"
        ordering = ["name"]