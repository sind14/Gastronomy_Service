from rest_framework import serializers
from orders.models import (
    RealizationType,
    Inventory,
    Dish,
    SavedDish,
    SavedInventory,
    Category,
    Menu,
    Address,
    Company,
    Client,
    Order,
    SavedOrder,
)


class BaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name", "price"]


class BaseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "dishes"]


class BaseMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "name", "price", "categories"]


class BaseCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "address", "nip"]


class RealizationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealizationType
        fields = ["id", "name"]


class InventorySerializer(BaseItemSerializer):
    class Meta(BaseItemSerializer.Meta):
        model = Inventory


class DishSerializer(BaseItemSerializer):
    class Meta(BaseItemSerializer.Meta):
        model = Dish


class SavedDishSerializer(BaseItemSerializer):
    class Meta(BaseItemSerializer.Meta):
        model = SavedDish


class SavedInventorySerializer(BaseItemSerializer):
    class Meta(BaseItemSerializer.Meta):
        model = SavedInventory


class CategoryReadSerializer(BaseCategorySerializer):
    dishes = DishSerializer(many=True, read_only=True)


class CategoryCreateSerializer(BaseCategorySerializer):
    dishes = serializers.PrimaryKeyRelatedField(many=True, queryset=Dish.objects.all())


class MenuReadSerializer(BaseMenuSerializer):
    categories = CategoryReadSerializer(many=True, read_only=True)


class MenuCreateSerializer(BaseMenuSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
    )


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "city",
            "postal_code",
            "street",
            "house_number",
            "apartment",
            "note",
        ]


class CompanyReadSerializer(BaseCompanySerializer):
    address = AddressSerializer(read_only=True, many=True)


class CompanyCreateSerializer(BaseCompanySerializer):
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), many=True)


class BaseClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_num",
            "email",
            "document_id",
            "document_type",
            "companies",
        ]


class ClientReadSerializer(BaseClientSerializer):
    companies = CompanyReadSerializer(many=True, read_only=True)


class ClientCreateSerializer(BaseClientSerializer):
    companies = serializers.PrimaryKeyRelatedField(many=True, queryset=Company.objects.all())


class OrderReadSerializer(serializers.ModelSerializer):
    client = ClientReadSerializer(read_only=True)
    company = CompanyReadSerializer(read_only=True)
    realization_type = RealizationTypeSerializer(read_only=True)
    address = AddressSerializer(read_only=True)
    dishes = DishSerializer(many=True, read_only=True)
    inventories = InventorySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_date",
            "order_created",
            "realization_type",
            "people_num",
            "address",
            "company",
            "client",
            "dishes",
            "inventories",
            "status",
            "cancel_reason",
            "total_price",
        ]
        read_only_fields = ["order_created", "total_price"]


class OrderCreateSerializer(OrderReadSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False, allow_null=True)
    realization_type = serializers.PrimaryKeyRelatedField(queryset=RealizationType.objects.all())
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), required=False, allow_null=True)
    dishes = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), many=True, required=False)
    inventories = serializers.PrimaryKeyRelatedField(queryset=Inventory.objects.all(), many=True, required=False)


class SavedOrderReadSerializer(OrderReadSerializer):
    dishes = SavedDishSerializer(many=True, read_only=True)
    inventories = SavedInventorySerializer(many=True, read_only=True)

    class Meta(OrderReadSerializer.Meta):
        model = SavedOrder
        fields = "__all__"
        read_only_fields = "__all__"
