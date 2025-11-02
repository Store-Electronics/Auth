from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "stock", "brand", "model"]

    def create(self, validated_data):
        product = Product(**validated_data)
        if product.price <= 0:
            raise serializers.ValidationError("Price must be a positive number")
        if product.stock < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        product.save()
        return product