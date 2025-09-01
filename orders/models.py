from phonenumber_field.modelfields import PhoneNumberField
from django.db import models


class RealizationType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    dishes = models.ManyToManyField(Dish, related_name="category", blank=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name="menus")

    def __str__(self):
        return self.name


class Address(models.Model):
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house = models.CharField(max_length=5)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.city + " " + self.street + " " + self.house


class Company(models.Model):
    name = models.CharField(max_length=50)
    address = models.ManyToManyField(Address, related_name="companies")
    nip = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_num = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    pesel = models.CharField(max_length=11, unique=True)
    companies = models.ManyToManyField(Company, related_name="clients")

    def __str__(self):
        return self.first_name + " " + self.last_name


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class Order(models.Model):
    order_date = models.DateTimeField(null=True, blank=True)
    order_created = models.DateTimeField(auto_now_add=True)
    realization_type = models.ForeignKey(RealizationType, on_delete=models.PROTECT)
    people_num = models.PositiveIntegerField()
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True, related_name="orders"
    )
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders"
    )
    dishes = models.ManyToManyField(Dish, related_name="orders", blank=True)
    inventories = models.ManyToManyField(Inventory, related_name="orders", blank=True)
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    cancel_reason = models.TextField(blank=True, null=True)

    def mark_completed(self):
        self.status = OrderStatus.COMPLETED
        self.save()

    def mark_cancelled(self, reason: str):
        self.status = OrderStatus.CANCELLED
        self.cancel_reason = reason
        self.save()

    def mark_pending(self):
        self.status = OrderStatus.PENDING
        self.cancel_reason = None
        self.save()
