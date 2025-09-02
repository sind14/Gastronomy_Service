from typing import Type
from rest_framework import viewsets
from rest_framework.serializers import BaseSerializer
from orders.models import (
    RealizationType,
    Dish,
    Inventory,
    Category,
    Menu,
    Address,
    Company,
    Client,
    Order,
    SavedDish,
    SavedInventory,
    SavedOrder,
)
from orders.serializers import (
    RealizationTypeSerializer,
    DishSerializer,
    InventorySerializer,
    CategoryReadSerializer,
    CategoryCreateSerializer,
    MenuReadSerializer,
    MenuCreateSerializer,
    AddressSerializer,
    CompanyReadSerializer,
    CompanyCreateSerializer,
    ClientReadSerializer,
    ClientCreateSerializer,
    OrderReadSerializer,
    OrderCreateSerializer,
    SavedDishSerializer,
    SavedInventorySerializer,
    SavedOrderReadSerializer,
)


class BaseModelViewSet(viewsets.ModelViewSet):
    create_serializer_class = None
    read_serializer_class = None

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action in ['create', 'update', 'partial_update'] and self.create_serializer_class:
            return self.create_serializer_class
        elif self.read_serializer_class:
            return self.read_serializer_class
        elif self.serializer_class:
            return self.serializer_class
        else:
            raise Exception("Serializer class is not defined")


class RealizationTypeViewSet(viewsets.ModelViewSet):
    queryset = RealizationType.objects.all()
    serializer_class = RealizationTypeSerializer


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class CategoryViewSet(BaseModelViewSet):
    queryset = Category.objects.all()
    create_serializer_class = CategoryCreateSerializer
    read_serializer_class = CategoryReadSerializer


class MenuViewSet(BaseModelViewSet):
    queryset = Menu.objects.all()
    create_serializer_class = MenuCreateSerializer
    read_serializer_class = MenuReadSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class CompanyViewSet(BaseModelViewSet):
    queryset = Company.objects.all()
    create_serializer_class = CompanyCreateSerializer
    read_serializer_class = CompanyReadSerializer


class ClientViewSet(BaseModelViewSet):
    queryset = Client.objects.all()
    create_serializer_class = ClientCreateSerializer
    read_serializer_class = ClientReadSerializer


class OrderViewSet(BaseModelViewSet):
    queryset = Order.objects.all()
    create_serializer_class = OrderCreateSerializer
    read_serializer_class = OrderReadSerializer


class SavedDishViewSet(viewsets.ModelViewSet):
    queryset = SavedDish.objects.all()
    serializer_class = SavedDishSerializer


class SavedInventoryViewSet(viewsets.ModelViewSet):
    queryset = SavedInventory.objects.all()
    serializer_class = SavedInventorySerializer


class SavedOrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SavedOrder.objects.all()
    serializer_class = SavedOrderReadSerializer
