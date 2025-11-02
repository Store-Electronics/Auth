from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Product

User = get_user_model()



class ProductTests(APITestCase):
    def setUp(self):
        self.product_list_url = reverse("product-list")
        self.product_detail_url = lambda pk: reverse("product-detail", kwargs={"id": pk})

        self.product_data = {
            "name": "Phone",
            "price": 100,
            "price_business": 80,
            "stock": 1,
            "brand": "Apple",
            "model": "Iphone 11"
        }

        self.admin_user = User.objects.create_user(username="admin", email="admin@admin.com", password="admin", is_admin=True)
        self.business_user = User.objects.create_user(username="business", email="business@business.com", password="business", is_business=True)
        self.user = User.objects.create_user(username="user", email="user@user.com", password="user", is_business=True)

        refresh = RefreshToken.for_user(self.admin_user)
        self.admin_access_token = str(refresh.access_token)

        refresh_business = RefreshToken.for_user(self.business_user)
        self.business_access_token = str(refresh_business.access_token)

        refresh_regular = RefreshToken.for_user(self.user)
        self.regular_access_token = str(refresh_regular.access_token)

        self.product = Product.objects.create(**self.product_data)

    # --- READ ---
    def test_get_all_products(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.product.id)
        self.assertEqual(response.data[0]["name"], self.product.name)
        self.assertEqual(response.data[0]["price"], self.product.price)
        self.assertEqual(response.data[0]["stock"], self.product.stock)
        self.assertEqual(response.data[0]["brand"], self.product.brand)

    def test_get_product_by_id(self):
        response = self.client.get(self.product_detail_url(self.product.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.product.id)
        self.assertEqual(response.data["name"], self.product.name)
        self.assertEqual(response.data["price"], self.product.price)
        self.assertEqual(response.data["stock"], self.product.stock)
        self.assertEqual(response.data["brand"], self.product.brand)

    def test_get_product_not_found(self):
        response = self.client.get(self.product_detail_url(999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # --- CREATE ---
    def test_create_product(self):
        new_product = {
            "name": "New Phone",
            "price": 100,
            "price_business": 80,
            "stock": 1,
            "brand": "Bear",
            "model": "BearPhone"
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_access_token}")
        response = self.client.post(self.product_list_url, new_product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(self.product_list_url)
        self.assertEqual(len(response.json()), 2)

    def test_create_product_without_permissions(self):
        new_product = {
            "name": "New Phone",
            "price": 100,
            "price_business": 80,
            "stock": 1,
            "brand": "Bear",
            "model": "BearPhone"
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.regular_access_token}")
        response = self.client.post(self.product_list_url, new_product)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get(self.product_list_url)
        self.assertEqual(len(response.json()), 1)

    def test_create_product_bad_data(self):
        new_product = {
            "name": "New Phone",
            "price": 100,
            "price_business": 80,
            "stock": -1,
            "brand": "Bear",
            "model": "BearPhone"
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_access_token}")
        response = self.client.post(self.product_list_url, new_product)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- UPDATE ---
    def test_update_product_without_permissions(self):
        update_data = {"price": 899.99, "stock": 5}
        response = self.client.patch(
            self.product_detail_url(self.product.id),
            update_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, 100.0)
        self.assertEqual(self.product.stock, 1)

    def test_update_product(self):
        update_data = {"price": 899.99, "stock": 5}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_access_token}")
        response = self.client.patch(
            self.product_detail_url(self.product.id),
            update_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, 899.99)
        self.assertEqual(self.product.stock, 5)

    # --- DELETE ---
    def test_delete_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_access_token}")
        response = self.client.delete(self.product_detail_url(self.product.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_delete_product_without_permissions(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.regular_access_token}")
        response = self.client.delete(self.product_detail_url(self.product.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.count(), 1)

    def test_delete_product_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_access_token}")
        response = self.client.delete(self.product_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)