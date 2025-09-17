from django.urls import path, include
from rest_framework import routers
from orders.views import (
    RealizationTypeViewSet,
    DishViewSet,
    InventoryViewSet,
    CategoryViewSet,
    MenuViewSet,
    AddressViewSet,
    CompanyViewSet,
    ClientViewSet,
    OrderViewSet,
    SavedDishViewSet,
    SavedInventoryViewSet,
    SavedOrderViewSet,
)

router = routers.DefaultRouter()
router.register("realization-types", RealizationTypeViewSet)
router.register("dishes", DishViewSet)
router.register("inventories", InventoryViewSet)
router.register("categories", CategoryViewSet)
router.register("menus", MenuViewSet)
router.register("addresses", AddressViewSet)
router.register("companies", CompanyViewSet)
router.register("clients", ClientViewSet)
router.register("orders", OrderViewSet)
router.register("saved-dishes", SavedDishViewSet)
router.register("saved-inventories", SavedInventoryViewSet)
router.register("saved-orders", SavedOrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "orders"
