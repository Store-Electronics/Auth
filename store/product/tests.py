from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from .models import Product

class ProductTests(APITestCase):
    def setUp(self):
        self.product_list_url = reverse("product-list")
        self.product_detail_url = lambda pk: reverse("product-detail", kwargs={"id": pk})

        self.product_data = {
            "name": "Phone",
            "price": 100,
            "stock": 1,
            "brand": "Apple",
            "model": "Iphone 11"
        }

        self.product = Product.objects.create(**self.product_data)

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

    def test_create_product(self):
        new_product = {
            "name": "New Phone",
            "price": 100,
            "stock": 1,
            "brand": "Bear",
            "model": "BearPhone"
        }
        response = self.client.post(self.product_list_url, new_product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(self.product_list_url)
        self.assertEqual(len(response.json()), 2)

    def test_create_product_bad_data(self):
        new_product = {
            "name": "New Phone",
            "price": 100,
            "stock": -1,
            "brand": "Bear",
            "model": "BearPhone"
        }

        response = self.client.post(self.product_list_url, new_product)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product(self):
        update_data = {"price": 899.99, "stock": 5}
        response = self.client.patch(
            self.product_detail_url(self.product.id),
            update_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, 899.99)
        self.assertEqual(self.product.stock, 5)

    def test_delete_product(self):
        response = self.client.delete(self.product_detail_url(self.product.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_delete_product_not_found(self):
        response = self.client.delete(self.product_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)