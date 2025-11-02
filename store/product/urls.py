from django.urls import path
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('product/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
]