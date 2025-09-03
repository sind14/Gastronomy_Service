from typing import Optional
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models


class RealizationType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.name}"


class BaseItem(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.name}: {self.price}"


class Dish(BaseItem):
    pass


class Inventory(BaseItem):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50)
    dishes = models.ManyToManyField(Dish, related_name="category", blank=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Menu(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name="menus")

    def __str__(self) -> str:
        return f"{self.name}: {self.price}"


class Address(models.Model):
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    apartment = models.CharField(max_length=10, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        parts = [self.city, self.street, self.house_number]
        if self.apartment:
            parts.append(f"apt. {self.apartment}")
        return ", ".join(parts)


class Company(models.Model):
    name = models.CharField(max_length=50)
    address = models.ManyToManyField(Address, related_name="companies")
    nip = models.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_num = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    companies = models.ManyToManyField(Company, related_name="clients")
    document_id = models.CharField(max_length=50)
    document_type = models.CharField(
        max_length=20,
        choices=[
            ("pesel", "PESEL"),
            ("passport", "Passport"),
            ("id_card", "ID Card"),
            ("other", "Other"),
        ],
        default="pesel"
    )

    class Meta:
        unique_together = ("document_id", "document_type")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class Order(models.Model):
    order_date = models.DateTimeField(null=True, blank=True)
    order_created = models.DateTimeField(auto_now_add=True)
    realization_type = models.ForeignKey(RealizationType, on_delete=models.PROTECT)
    people_num = models.PositiveIntegerField()
    cancel_reason = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True, default=0)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True, related_name="orders")
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True, related_name="orders")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True, related_name="orders")
    dishes = models.ManyToManyField(Dish, related_name="orders", blank=True)
    inventories = models.ManyToManyField(Inventory, related_name="orders", blank=True)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    def set_selected_dishes(self, selected_dish_ids) -> None:
        selected_dishes = Dish.objects.filter(id__in=selected_dish_ids)
        self.dishes.set(selected_dishes)

    def calculate_total_price(self, menu_price: float = None):
        if menu_price is not None:
            return menu_price * self.people_num
        else:
            dishes_sum = sum(dish.price for dish in self.dishes.all())
            inventories_sum = sum(inv.price for inv in self.inventories.all())
            return dishes_sum + inventories_sum

    def _order_to_saved_order(self, status: str, cancel_reason: Optional[str] = None) -> "SavedOrder":
        saved_order = SavedOrder.objects.create(
            order_date=self.order_date,
            order_created=self.order_created,
            realization_type=self.realization_type,
            people_num=self.people_num,
            address=self.address,
            company=self.company,
            client=self.client,
            status=status,
            cancel_reason=cancel_reason,
            total_price=self.calculate_total_price()
        )

        self._items_to_saved_items(saved_order)

        return saved_order

    def _items_to_saved_items(self, saved_order: "SavedOrder"):
        for dish in self.dishes.all():
            saved_dish, _ = SavedDish.objects.get_or_create(
                name=dish.name,
                price=dish.price
            )
            saved_order.dishes.add(saved_dish)

        for inventory in self.inventories.all():
            saved_inventory, _ = SavedInventory.objects.get_or_create(
                name=inventory.name,
                price=inventory.price
            )
            saved_order.inventories.add(saved_inventory)

    def mark_completed(self) -> None:
        self._order_to_saved_order(status=OrderStatus.COMPLETED)
        self.delete()

    def mark_cancelled(self, reason: str) -> None:
        self._order_to_saved_order(status=OrderStatus.CANCELLED, cancel_reason=reason)
        self.delete()


class SavedInventory(BaseItem):
    pass


class SavedDish(BaseItem):
    pass


class SavedOrder(models.Model):
    order_date = models.DateTimeField(null=True, blank=True)
    order_created = models.DateTimeField()
    realization_type = models.ForeignKey(RealizationType, on_delete=models.PROTECT)
    people_num = models.PositiveIntegerField()
    menu = models.ForeignKey(Menu, related_name="orders", on_delete=models.PROTECT, null=True, blank=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True, default=0)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True, related_name="saved_orders")
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True, related_name="saved_orders")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True, related_name="saved_orders")
    dishes = models.ManyToManyField(SavedDish, related_name="saved_orders", blank=True)
    inventories = models.ManyToManyField(SavedInventory, related_name="saved_orders", blank=True)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    cancel_reason = models.TextField(blank=True, null=True)
